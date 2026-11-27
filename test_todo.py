import todo
from helpers import TodoTestCase


class TestBasicCommands(TodoTestCase):
    def test_add_creates_task(self):
        code, out = self.run_cli("add", "Học", "bài")
        self.assertEqual(code, 0)
        self.assertIn("Đã thêm task #1: Học bài", out)
        self.assertEqual(todo.load_tasks()[0]["title"], "Học bài")
        self.assertFalse(todo.load_tasks()[0]["done"])

    def test_ids_increment(self):
        self.run_cli("add", "A")
        self.run_cli("add", "B")
        self.assertEqual([t["id"] for t in todo.load_tasks()], [1, 2])

    def test_add_without_title_fails(self):
        code, out = self.run_cli("add")
        self.assertEqual(code, 1)
        self.assertIn("Thiếu nội dung task.", out)

    def test_list_empty(self):
        _, out = self.run_cli("list")
        self.assertIn("Chưa có task nào.", out)

    def test_list_shows_done_mark(self):
        self.run_cli("add", "A")
        self.run_cli("add", "B")
        self.run_cli("done", "1")
        _, out = self.run_cli("list")
        self.assertIn("[x] 1. A", out)
        self.assertIn("[ ] 2. B", out)

    def test_done_marks_task(self):
        self.run_cli("add", "A")
        _, out = self.run_cli("done", "1")
        self.assertIn("Đã hoàn thành task #1", out)
        self.assertTrue(todo.load_tasks()[0]["done"])

    def test_done_missing_id(self):
        _, out = self.run_cli("done", "9")
        self.assertIn("Không tìm thấy task #9", out)

    def test_done_requires_numeric_id(self):
        code, _ = self.run_cli("done", "abc")
        self.assertEqual(code, 1)

    def test_delete_removes_task(self):
        self.run_cli("add", "A")
        self.run_cli("add", "B")
        self.run_cli("delete", "1")
        self.assertEqual([t["title"] for t in todo.load_tasks()], ["B"])

    def test_delete_missing_id(self):
        _, out = self.run_cli("delete", "5")
        self.assertIn("Không tìm thấy task #5", out)

    def test_clear_removes_only_done(self):
        self.run_cli("add", "A")
        self.run_cli("add", "B")
        self.run_cli("done", "1")
        _, out = self.run_cli("clear")
        self.assertIn("Đã xóa 1 task đã hoàn thành", out)
        self.assertEqual([t["title"] for t in todo.load_tasks()], ["B"])

    def test_clear_when_nothing_done(self):
        self.run_cli("add", "A")
        _, out = self.run_cli("clear")
        self.assertIn("Không có task nào đã hoàn thành.", out)
        self.assertEqual(len(todo.load_tasks()), 1)

    def test_edit_changes_title(self):
        self.run_cli("add", "Cũ")
        self.run_cli("edit", "1", "Nội", "dung", "mới")
        self.assertEqual(todo.load_tasks()[0]["title"], "Nội dung mới")

    def test_edit_requires_new_title(self):
        code, _ = self.run_cli("edit", "1")
        self.assertEqual(code, 1)

    def test_no_arguments_shows_usage(self):
        code, out = self.run_cli()
        self.assertEqual(code, 1)
        self.assertIn("Cách dùng:", out)

    def test_unknown_command(self):
        code, out = self.run_cli("bay")
        self.assertEqual(code, 1)
        self.assertIn("Lệnh không hợp lệ: bay", out)
