import json
import sys
from pathlib import Path

DATA_FILE = Path("tasks.json")


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

def main():
    if len(sys.argv) < 2:
        print("Cách dùng:")
        print("  python todo.py add <nội dung>")
        print("  python todo.py list")
        print("  python todo.py done <id>")
        print("  python todo.py delete <id>")
        return

    command = sys.argv[1]

    if command == "add":
        if len(sys.argv) < 3:
            print("Thiếu nội dung task.")
            return
        add_task(" ".join(sys.argv[2:]))
    elif command == "list":
        list_tasks()
    elif command == "done":
        if len(sys.argv) < 3 or not sys.argv[2].isdigit():
            print("Cách dùng: python todo.py done <id>")
            return
        mark_done(int(sys.argv[2]))
    elif command == "delete":
        if len(sys.argv) < 3 or not sys.argv[2].isdigit():
            print("Cách dùng: python todo.py delete <id>")
            return
        delete_task(int(sys.argv[2]))
    elif command == "clear":
        clear_done()
    elif command == "edit":
        if len(sys.argv) < 4 or not sys.argv[2].isdigit():
            print("Cách dùng: python todo.py edit <id> <nội dung mới>")
            return
        edit_task(int(sys.argv[2]), " ".join(sys.argv[3:]))
    elif command == "edit":
        if len(sys.argv) < 4 or not sys.argv[2].isdigit():
            print("Cách dùng: python todo.py edit <id> <nội dung mới>")
            return
        edit_task(int(sys.argv[2]), " ".join(sys.argv[3:]))
    else:
        print(f"Lệnh không hợp lệ: {command}")


if __name__ == "__main__":
    main()