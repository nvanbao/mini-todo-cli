import todo
from helpers import TodoTestCase


class TestFilterAndSearch(TodoTestCase):
    def setUp(self):
        super().setUp()
        self.run_cli("add", "Học Python")
        self.run_cli("add", "Nộp báo cáo")
        self.run_cli("add", "Ôn thi Python nâng cao")
        self.run_cli("done", "2")

    def test_list_todo_only(self):
        _, out = self.run_cli("list", "--todo")
        self.assertIn("1. Học Python", out)
        self.assertIn("3. Ôn thi Python nâng cao", out)
        self.assertNotIn("Nộp báo cáo", out)

    def test_list_done_only(self):
        _, out = self.run_cli("list", "--done")
        self.assertIn("[x] 2. Nộp báo cáo", out)
        self.assertNotIn("Học Python", out)

    def test_list_done_when_none(self):
        self.run_cli("clear")
        _, out = self.run_cli("list", "--done")
        self.assertIn("Chưa có task nào.", out)

    def test_search_is_case_insensitive(self):
        _, out = self.run_cli("search", "python")
        self.assertIn("1. Học Python", out)
        self.assertIn("3. Ôn thi Python nâng cao", out)
        self.assertNotIn("Nộp báo cáo", out)

    def test_search_multiple_words(self):
        _, out = self.run_cli("search", "báo", "cáo")
        self.assertIn("2. Nộp báo cáo", out)

    def test_search_no_result(self):
        _, out = self.run_cli("search", "không-có")
        self.assertIn("Không tìm thấy task nào.", out)

    def test_search_requires_keyword(self):
        code, out = self.run_cli("search")
        self.assertEqual(code, 1)
        self.assertIn("python todo.py search", out)
