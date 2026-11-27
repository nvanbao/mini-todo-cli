from datetime import date
from unittest.mock import patch

import todo
from helpers import TodoTestCase


class TestDueDate(TodoTestCase):
    def test_add_with_due_date(self):
        code, _ = self.run_cli("add", "Nộp", "đồ", "án", "--due", "2026-12-15")
        self.assertEqual(code, 0)
        task = todo.load_tasks()[0]
        self.assertEqual(task["due"], "2026-12-15")
        self.assertEqual(task["title"], "Nộp đồ án")

    def test_task_without_due_has_no_due_field(self):
        self.run_cli("add", "A")
        self.assertNotIn("due", todo.load_tasks()[0])

    def test_invalid_date_rejected(self):
        code, out = self.run_cli("add", "A", "--due", "15/12/2026")
        self.assertEqual(code, 1)
        self.assertIn("YYYY-MM-DD", out)
        self.assertEqual(todo.load_tasks(), [])

    def test_missing_date_after_flag(self):
        code, out = self.run_cli("add", "A", "--due")
        self.assertEqual(code, 1)
        self.assertIn("Thiếu ngày sau --due", out)

    def test_list_shows_due_date(self):
        self.run_cli("add", "A", "--due", "2099-01-01")
        _, out = self.run_cli("list")
        self.assertIn("(hạn 2099-01-01)", out)
        self.assertNotIn("QUÁ HẠN", out)

    def test_overdue_marker(self):
        self.run_cli("add", "A", "--due", "2026-12-01")
        with patch.object(todo, "today", return_value=date(2026, 12, 2)):
            _, out = self.run_cli("list")
        self.assertIn("[QUÁ HẠN]", out)

    def test_due_today_is_not_overdue(self):
        self.run_cli("add", "A", "--due", "2026-12-01")
        with patch.object(todo, "today", return_value=date(2026, 12, 1)):
            _, out = self.run_cli("list")
        self.assertNotIn("QUÁ HẠN", out)

    def test_done_task_is_never_overdue(self):
        self.run_cli("add", "A", "--due", "2020-01-01")
        self.run_cli("done", "1")
        _, out = self.run_cli("list")
        self.assertNotIn("QUÁ HẠN", out)

    def test_combine_priority_and_due(self):
        self.run_cli("add", "Thi", "--high", "--due", "2026-12-20")
        _, out = self.run_cli("list")
        self.assertIn("(ưu tiên cao) (hạn 2026-12-20)", out)
