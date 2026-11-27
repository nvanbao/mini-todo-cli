import contextlib
import io
import tempfile
import unittest
from pathlib import Path

import todo


class TodoTestCase(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self.tmp.cleanup)
        old_file = todo.DATA_FILE
        todo.DATA_FILE = Path(self.tmp.name) / "tasks.json"
        self.addCleanup(setattr, todo, "DATA_FILE", old_file)

    def run_cli(self, *args):
        buffer = io.StringIO()
        with contextlib.redirect_stdout(buffer):
            code = todo.run(list(args))
        return code, buffer.getvalue()
