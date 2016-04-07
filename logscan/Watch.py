from os import path
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler


class Watcher(FileSystemEventHandler):
    def __init__(self, filename, matcher):
        self.filename = path.abspath(filename)
        self.matcher = matcher
        self.observer = Observer()
        self.fd = None
        self.offset = 0
        if path.isfile(self.filename):
            self.fd = open(self.filename)
            self.offset = path.getsize(self.filename)

    def on_deleted(self, event):
        if path.abspath(event.src_path) == self.filename:
            self.fd.close()

    def on_created(self, event):
        if path.abspath(event.src_path) == self.filename and path.isfile(self.filename):
            self.fd = open(self.filename)
            self.offset = path.getsize(self.filename)

    def on_moved(self, event):
        if path.abspath(event.dest_path) == self.filename and path.isfile(self.filename):
            self.fd = open(self.filename)
            self.offset = path.getsize(self.filename)
        elif path.abspath(event.src_path) == self.filename:
            self.fd.close()

    def on_modified(self, event):
        if path.abspath(event.src_path) == self.filename:
            self.fd.seek(self.offset, 0)
            match = getattr(self.matcher, 'match', lambda x: False)
            for line in self.fd:
                line = line.rsplit('\n')
                if match(line):
                    print('matched {0}'.format(line))
            self.offset = self.fd.tell()

    def start(self):
        self.observer.schedule(self, path.dirname(self.filename), recursive=False)
        self.observer.start()
        self.observer.join()

    def close(self):
        self.observer.stop()
        if self.fd is not None and not self.fd.closed:
            self.fd.close()

if __name__ == '__main__':
    filename = 'C:\\Users\\liubin\\Desktop\\123.txt'
    class Matcher:
        def match(self, line):
            return True
    w = Watcher(filename, Matcher())
    w.start()
