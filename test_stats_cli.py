import csv
from datetime import date
from pathlib import Path
from unittest.mock import patch

import todo
from helpers import TodoTestCase


class TestStatsAndExportCli(TodoTestCase):
    def test_stats_with_no_tasks(self):
        code, out = self.run_cli("stats")
        self.assertEqual(code, 0)
        self.assertIn("Tổng: 0 | Đã xong: 0 (0%) | Còn lại: 0", out)

    def test_stats_with_tasks(self):
        self.run_cli("add", "A", "--high")
        self.run_cli("add", "B", "--due", "2026-11-01")
        self.run_cli("add", "C")
        self.run_cli("done", "3")
        with patch.object(todo, "today", return_value=date(2026, 12, 1)):
            _, out = self.run_cli("stats")
        self.assertIn("Tổng: 3 | Đã xong: 1 (33%) | Còn lại: 2", out)
        self.assertIn("Ưu tiên cao chưa xong: 1 | Quá hạn: 1", out)

    def test_export_writes_csv_file(self):
        self.run_cli("add", "Nộp", "bài", "--high")
        self.run_cli("add", "Học")
        path = Path(self.tmp.name) / "tasks.csv"
        code, out = self.run_cli("export", str(path))
        self.assertEqual(code, 0)
        self.assertIn("Đã xuất 2 task ra", out)
        with open(path, encoding="utf-8-sig", newline="") as f:
            rows = list(csv.DictReader(f))
        self.assertEqual([r["title"] for r in rows], ["Nộp bài", "Học"])
        self.assertEqual(rows[0]["priority"], "high")

    def test_export_requires_file_name(self):
        code, out = self.run_cli("export")
        self.assertEqual(code, 1)
        self.assertIn("python todo.py export", out)

    def test_usage_lists_new_commands(self):
        _, out = self.run_cli()
        self.assertIn("stats", out)
        self.assertIn("export", out)
