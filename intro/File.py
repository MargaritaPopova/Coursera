import tempfile
from os import path


class File:

    def __init__(self, path_to_file):
        self.path_to_file = path_to_file
        self.current = 0
        if not path.exists(self.path_to_file):
            open(self.path_to_file, 'w').close()

    def __str__(self):
        return path.abspath(self.path_to_file)

    def __add__(self, other):
        name = tempfile.NamedTemporaryFile().name
        res = File(path.join(tempfile.gettempdir(), name))
        res.write(self.read() + other.read())
        return res

    def __iter__(self):
        return self

    def __next__(self):
        with open(self.path_to_file, 'r') as f:
            f.seek(self.current)
            line = f.readline()

            if not line:
                self.current = 0
                raise StopIteration

            self.current = f.tell()
            return line

    def read(self):
        with open(self.path_to_file, 'r') as f:
            return f.read()

    def write(self, data):
        with open(self.path_to_file, 'w') as f:
            return f.write(data)


f1 = File('one.txt')
f2 = File('two.txt')
f3 = f1 + f2
print(f3)
print(isinstance(f3, File))
