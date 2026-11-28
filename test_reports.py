import unittest
from datetime import date

from reports import compute_stats

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
