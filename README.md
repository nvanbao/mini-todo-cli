# mini-todo-cli

Ứng dụng to-do chạy trên terminal, viết bằng Python, lưu dữ liệu vào file JSON.

## Yêu cầu
- Python 3.8+

## Cách dùng

    python todo.py add Hoc bai                           # thêm task
    python todo.py add Nop bao cao --high --due 2026-12-20   # có ưu tiên và hạn chót
    python todo.py list                                  # xem tất cả
    python todo.py list --todo                           # chỉ task chưa xong
    python todo.py list --done                           # chỉ task đã xong
    python todo.py search python                         # tìm theo từ khóa
    python todo.py done 1                                # đánh dấu hoàn thành
    python todo.py edit 1 Noi dung moi                   # sửa nội dung
    python todo.py delete 1                              # xóa task
    python todo.py clear                                 # xóa mọi task đã hoàn thành

## Ví dụ

    [ ] 1. Nop bao cao (ưu tiên cao) (hạn 2026-12-20)
    [x] 2. Hoc bai
    [ ] 3. Doc sach (hạn 2026-01-05) [QUÁ HẠN]

## Cấu trúc
- `todo.py`: toàn bộ logic
- `helpers.py`: lớp dùng chung cho test (dùng file dữ liệu tạm)
- `test_*.py`: unit test
- `tasks.json`: dữ liệu (tự tạo khi chạy, không đưa lên git)

## Chạy test

    python -m unittest
