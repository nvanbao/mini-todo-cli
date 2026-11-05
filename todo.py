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

def main():
    if len(sys.argv) < 2:
        print("Cách dùng:")
        print("  python todo.py add <nội dung>")
        print("  python todo.py list")
        return

    command = sys.argv[1]

    if command == "add":
        if len(sys.argv) < 3:
            print("Thiếu nội dung task.")
            return
        add_task(" ".join(sys.argv[2:]))
    elif command == "list":
        list_tasks()
    else:
        print(f"Lệnh không hợp lệ: {command}")


if __name__ == "__main__":
    main()