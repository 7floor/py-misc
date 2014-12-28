class Pin:
    path = ''
    file = None

    def __init__(self, path):
        self.path = path
        with open(self.path + '/direction', 'w') as dir:
            dir.write('out')
        self._fopen()
        self.set(0)

    def __del__(self):
        self._fclose()

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self._fclose()

    def _fopen(self):
        self.file = open(self.path + '/value', 'w')

    def _fclose(self):
        if self.file is not None:
            self.file.close()
            self.file = None

    def set(self, value):
        v = '0' if value else '1'
        self.file.seek(0)
        self.file.write(v)
        self.file.flush()