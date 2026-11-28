from datetime import date


def compute_stats(tasks, today):
    total = len(tasks)
    done = sum(1 for t in tasks if t["done"])
    high_open = sum(
        1 for t in tasks if not t["done"] and t.get("priority") == "high"
    )
    overdue = sum(
        1
        for t in tasks
        if not t["done"] and t.get("due") and date.fromisoformat(t["due"]) < today
    )
    percent = round(done * 100 / total) if total else 0
    return {
        "total": total,
        "done": done,
        "todo": total - done,
        "percent": percent,
        "high_open": high_open,
        "overdue": overdue,
    }
