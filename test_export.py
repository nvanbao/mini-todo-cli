import csv
from pathlib import Path

from helpers import TodoTestCase


class TestExport(TodoTestCase):
    def test_export_default_filename(self):
        self.run_cli("add", "Học Python", "--high", "--due", "2026-12-25")
        csv_file = Path(self.tmp.name) / "exported.csv"
        code, out = self.run_cli("export", str(csv_file))
        self.assertEqual(code, 0)
        self.assertIn("Đã xuất 1 task", out)
        self.assertTrue(csv_file.exists())
        with open(csv_file, "r", encoding="utf-8") as f:
            rows = list(csv.reader(f))
        self.assertEqual(rows[0], ["id", "title", "done", "priority", "due"])
        self.assertEqual(rows[1], ["1", "Học Python", "False", "high", "2026-12-25"])
