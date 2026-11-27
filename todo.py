import json
import sys
from pathlib import Path

DATA_FILE = Path("tasks.json")

USAGE = """Cách dùng:
  python todo.py add <nội dung>
  python todo.py list
  python todo.py done <id>
  python todo.py delete <id>
  python todo.py edit <id> <nội dung mới>
  python todo.py clear"""


def load_tasks():
    if not DATA_FILE.exists():
        return []
    with open(DATA_FILE, "r", encoding="utf-8") as f:
        return json.load(f)


def save_tasks(tasks):
    with open(DATA_FILE, "w", encoding="utf-8") as f:
        json.dump(tasks, f, ensure_ascii=False, indent=2)


def add_task(title):
    tasks = load_tasks()
    new_id = max((t["id"] for t in tasks), default=0) + 1
    tasks.append({"id": new_id, "title": title, "done": False})
    save_tasks(tasks)
    print(f"Đã thêm task #{new_id}: {title}")


def list_tasks():
    tasks = load_tasks()
    if not tasks:
        print("Chưa có task nào.")
        return
    for t in tasks:
        mark = "x" if t["done"] else " "
        print(f"[{mark}] {t['id']}. {t['title']}")


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


def run(argv):
    if not argv:
        print(USAGE)
        return 1
    command, args = argv[0], argv[1:]

    if command == "add":
        if not args:
            print("Thiếu nội dung task.")
            return 1
        add_task(" ".join(args))
    elif command == "list":
        list_tasks()
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
