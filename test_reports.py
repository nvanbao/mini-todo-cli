import csv
import tempfile
import unittest
from datetime import date
from pathlib import Path

from reports import compute_stats, export_csv

TODAY = date(2026, 12, 1)


class TestComputeStats(unittest.TestCase):
    def test_empty_list(self):
        stats = compute_stats([], TODAY)
        self.assertEqual(stats["total"], 0)
        self.assertEqual(stats["percent"], 0)

    def test_counts_done_and_todo(self):
        tasks = [
            {"id": 1, "title": "A", "done": True},
            {"id": 2, "title": "B", "done": False},
            {"id": 3, "title": "C", "done": False},
        ]
        stats = compute_stats(tasks, TODAY)
        self.assertEqual(stats["total"], 3)
        self.assertEqual(stats["done"], 1)
        self.assertEqual(stats["todo"], 2)
        self.assertEqual(stats["percent"], 33)

    def test_all_done_is_100_percent(self):
        tasks = [{"id": 1, "title": "A", "done": True}]
        self.assertEqual(compute_stats(tasks, TODAY)["percent"], 100)

    def test_high_priority_open_only(self):
        tasks = [
            {"id": 1, "title": "A", "done": False, "priority": "high"},
            {"id": 2, "title": "B", "done": True, "priority": "high"},
            {"id": 3, "title": "C", "done": False, "priority": "low"},
        ]
        self.assertEqual(compute_stats(tasks, TODAY)["high_open"], 1)

    def test_overdue_counts_only_open_tasks_before_today(self):
        tasks = [
            {"id": 1, "title": "A", "done": False, "due": "2026-11-30"},
            {"id": 2, "title": "B", "done": False, "due": "2026-12-01"},
            {"id": 3, "title": "C", "done": True, "due": "2020-01-01"},
            {"id": 4, "title": "D", "done": False},
        ]
        self.assertEqual(compute_stats(tasks, TODAY)["overdue"], 1)

    def test_old_tasks_without_new_fields(self):
        tasks = [{"id": 1, "title": "Cũ", "done": False}]
        stats = compute_stats(tasks, TODAY)
        self.assertEqual(stats["high_open"], 0)
        self.assertEqual(stats["overdue"], 0)


class TestExportCsv(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self.tmp.cleanup)
        self.path = Path(self.tmp.name) / "out.csv"

    def read_rows(self):
        with open(self.path, encoding="utf-8-sig", newline="") as f:
            return list(csv.DictReader(f))

    def test_returns_number_of_tasks(self):
        tasks = [{"id": 1, "title": "A", "done": False}]
        self.assertEqual(export_csv(tasks, self.path), 1)

    def test_header_and_values(self):
        tasks = [
            {"id": 1, "title": "Nộp bài", "done": True, "priority": "high", "due": "2026-12-20"},
            {"id": 2, "title": "Học", "done": False},
        ]
        export_csv(tasks, self.path)
        rows = self.read_rows()
        self.assertEqual(list(rows[0].keys()), ["id", "title", "done", "priority", "due"])
        self.assertEqual(rows[0]["title"], "Nộp bài")
        self.assertEqual(rows[0]["done"], "yes")
        self.assertEqual(rows[0]["priority"], "high")
        self.assertEqual(rows[0]["due"], "2026-12-20")
        self.assertEqual(rows[1]["done"], "no")
        self.assertEqual(rows[1]["priority"], "normal")
        self.assertEqual(rows[1]["due"], "")

    def test_title_with_comma_and_quote(self):
        tasks = [{"id": 1, "title": 'Mua "sách", vở', "done": False}]
        export_csv(tasks, self.path)
        self.assertEqual(self.read_rows()[0]["title"], 'Mua "sách", vở')

    def test_empty_list_writes_header_only(self):
        self.assertEqual(export_csv([], self.path), 0)
        self.assertEqual(self.read_rows(), [])

    def test_file_has_bom_for_excel(self):
        export_csv([{"id": 1, "title": "A", "done": False}], self.path)
        self.assertEqual(self.path.read_bytes()[:3], b"\xef\xbb\xbf")
