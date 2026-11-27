import json
import sys
from datetime import date
from pathlib import Path

DATA_FILE = Path("tasks.json")

PRIORITIES = {"high": "cao", "normal": "", "low": "thấp"}

USAGE = """Cách dùng:
  python todo.py add <nội dung> [--high | --low] [--due YYYY-MM-DD]
  python todo.py list [--todo | --done]
  python todo.py search <từ khóa>
  python todo.py stats
  python todo.py done <id>
  python todo.py delete <id>
  python todo.py edit <id> <nội dung mới>
  python todo.py clear"""


def today():
    return date.today()


def load_tasks():
    if not DATA_FILE.exists():
        return []
    with open(DATA_FILE, "r", encoding="utf-8") as f:
        return json.load(f)


def save_tasks(tasks):
    with open(DATA_FILE, "w", encoding="utf-8") as f:
        json.dump(tasks, f, ensure_ascii=False, indent=2)


def add_task(title, priority="normal", due=None):
    tasks = load_tasks()
    new_id = max((t["id"] for t in tasks), default=0) + 1
    task = {"id": new_id, "title": title, "done": False, "priority": priority}
    if due:
        task["due"] = due
    tasks.append(task)
    save_tasks(tasks)
    print(f"Đã thêm task #{new_id}: {title}")


def format_task(t):
    mark = "x" if t["done"] else " "
    line = f"[{mark}] {t['id']}. {t['title']}"
    label = PRIORITIES.get(t.get("priority", "normal"), "")
    if label:
        line += f" (ưu tiên {label})"
    due = t.get("due")
    if due:
        line += f" (hạn {due})"
        if not t["done"] and date.fromisoformat(due) < today():
            line += " [QUÁ HẠN]"
    return line


def print_tasks(tasks, empty_message):
    if not tasks:
        print(empty_message)
        return
    for t in tasks:
        print(format_task(t))


def list_tasks(only=None):
    tasks = load_tasks()
    if only == "todo":
        tasks = [t for t in tasks if not t["done"]]
    elif only == "done":
        tasks = [t for t in tasks if t["done"]]
    print_tasks(tasks, "Chưa có task nào.")


def search_tasks(keyword):
    key = keyword.lower()
    found = [t for t in load_tasks() if key in t["title"].lower()]
    print_tasks(found, "Không tìm thấy task nào.")


def show_stats():
    tasks = load_tasks()
    total = len(tasks)
    if total == 0:
        print("Chưa có task nào để thống kê.")
        return
    done = sum(1 for t in tasks if t["done"])
    todo_count = total - done
    rate = (done / total) * 100
    high = sum(1 for t in tasks if t.get("priority") == "high")
    low = sum(1 for t in tasks if t.get("priority") == "low")
    overdue = sum(
        1 for t in tasks
        if not t["done"] and t.get("due") and date.fromisoformat(t["due"]) < today()
    )
    print(f"Tổng số task: {total}")
    print(f"Đã hoàn thành: {done} ({rate:.1f}%)")
    print(f"Chưa hoàn thành: {todo_count}")
    print(f"Ưu tiên: {high} cao, {low} thấp")
    print(f"Quá hạn: {overdue}")


def mark_done(task_id):
    tasks = load_tasks()
    for t in tasks:
        if t["id"] == task_id:
            t["done"] = True
            save_tasks(tasks)
            print(f"Đã hoàn thành task #{task_id}")
            return
    print(f"Không tìm thấy task #{task_id}")


def delete_task(task_id):
    tasks = load_tasks()
    new_tasks = [t for t in tasks if t["id"] != task_id]
    if len(new_tasks) == len(tasks):
        print(f"Không tìm thấy task #{task_id}")
        return
    save_tasks(new_tasks)
    print(f"Đã xóa task #{task_id}")


def clear_done():
    tasks = load_tasks()
    remaining = [t for t in tasks if not t["done"]]
    removed = len(tasks) - len(remaining)
    if removed == 0:
        print("Không có task nào đã hoàn thành.")
        return
    save_tasks(remaining)
    print(f"Đã xóa {removed} task đã hoàn thành")


def edit_task(task_id, new_title):
    tasks = load_tasks()
    for t in tasks:
        if t["id"] == task_id:
            t["title"] = new_title
            save_tasks(tasks)
            print(f"Đã sửa task #{task_id}: {new_title}")
            return
    print(f"Không tìm thấy task #{task_id}")


def parse_add_args(args):
    priority = "normal"
    due = None
    words = []
    i = 0
    while i < len(args):
        arg = args[i]
        if arg == "--high":
            priority = "high"
        elif arg == "--low":
            priority = "low"
        elif arg == "--due":
            if i + 1 >= len(args):
                raise ValueError("Thiếu ngày sau --due")
            due = args[i + 1]
            try:
                date.fromisoformat(due)
            except ValueError:
                raise ValueError("Ngày hạn phải có dạng YYYY-MM-DD")
            i += 1
        else:
            words.append(arg)
        i += 1
    title = " ".join(words).strip()
    if not title:
        raise ValueError("Thiếu nội dung task.")
    return title, priority, due


def run(argv):
    if not argv:
        print(USAGE)
        return 1
    command, args = argv[0], argv[1:]

    if command == "add":
        try:
            title, priority, due = parse_add_args(args)
        except ValueError as error:
            print(error)
            return 1
        add_task(title, priority, due)
    elif command == "list":
        only = None
        if "--todo" in args:
            only = "todo"
        elif "--done" in args:
            only = "done"
        list_tasks(only)
    elif command == "search":
        if not args:
            print("Cách dùng: python todo.py search <từ khóa>")
            return 1
        search_tasks(" ".join(args))
    elif command == "stats":
        show_stats()
    elif command in ("done", "delete"):
        if not args or not args[0].isdigit():
            print(f"Cách dùng: python todo.py {command} <id>")
            return 1
        if command == "done":
            mark_done(int(args[0]))
        else:
            delete_task(int(args[0]))
    elif command == "edit":
        if len(args) < 2 or not args[0].isdigit():
            print("Cách dùng: python todo.py edit <id> <nội dung mới>")
            return 1
        edit_task(int(args[0]), " ".join(args[1:]))
    elif command == "clear":
        clear_done()
    else:
        print(f"Lệnh không hợp lệ: {command}")
        print(USAGE)
        return 1
    return 0


def main():
    sys.exit(run(sys.argv[1:]))


if __name__ == "__main__":
    main()
