from datetime import date
from unittest.mock import patch

import todo
from helpers import TodoTestCase


class TestStats(TodoTestCase):
    def test_stats_empty(self):
        _, out = self.run_cli("stats")
        self.assertIn("Chưa có task nào để thống kê.", out)

    def test_stats_summary(self):
        self.run_cli("add", "Task 1", "--high")
        self.run_cli("add", "Task 2", "--low")
        self.run_cli("done", "1")
        _, out = self.run_cli("stats")
        self.assertIn("Tổng số task: 2", out)
        self.assertIn("Đã hoàn thành: 1 (50.0%)", out)
        self.assertIn("Chưa hoàn thành: 1", out)
        self.assertIn("Ưu tiên: 1 cao, 1 thấp", out)

    def test_stats_overdue(self):
        self.run_cli("add", "Task cũ", "--due", "2026-12-01")
        with patch.object(todo, "today", return_value=date(2026, 12, 5)):
            _, out = self.run_cli("stats")
        self.assertIn("Quá hạn: 1", out)
