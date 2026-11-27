import todo
from helpers import TodoTestCase


class TestPriority(TodoTestCase):
    def test_default_priority_is_normal(self):
        self.run_cli("add", "A")
        self.assertEqual(todo.load_tasks()[0]["priority"], "normal")

    def test_high_flag(self):
        self.run_cli("add", "Nộp", "bài", "--high")
        task = todo.load_tasks()[0]
        self.assertEqual(task["priority"], "high")
        self.assertEqual(task["title"], "Nộp bài")

    def test_low_flag_in_front(self):
        self.run_cli("add", "--low", "Dọn", "bàn")
        task = todo.load_tasks()[0]
        self.assertEqual(task["priority"], "low")
        self.assertEqual(task["title"], "Dọn bàn")

    def test_list_shows_priority_label(self):
        self.run_cli("add", "A", "--high")
        self.run_cli("add", "B", "--low")
        self.run_cli("add", "C")
        _, out = self.run_cli("list")
        self.assertIn("[ ] 1. A (ưu tiên cao)", out)
        self.assertIn("[ ] 2. B (ưu tiên thấp)", out)
        self.assertIn("[ ] 3. C\n", out)

    def test_only_flag_without_title_fails(self):
        code, out = self.run_cli("add", "--high")
        self.assertEqual(code, 1)
        self.assertIn("Thiếu nội dung task.", out)

    def test_old_tasks_without_priority_still_list(self):
        todo.save_tasks([{"id": 1, "title": "Task cũ", "done": False}])
        _, out = self.run_cli("list")
        self.assertIn("[ ] 1. Task cũ", out)
