# mini-todo-cli

Ứng dụng to-do chạy trên terminal, viết bằng Python, lưu dữ liệu vào file JSON.

## Yêu cầu
- Python 3.8+

## Cách dùng

    python todo.py add Hoc bai          # thêm task
    python todo.py list                 # xem danh sách
    python todo.py done 1               # đánh dấu hoàn thành
    python todo.py edit 1 Noi dung moi  # sửa nội dung task
    python todo.py delete 1             # xóa task
    python todo.py clear                # xóa tất cả task đã hoàn thành

## Ví dụ

    [x] 1. Hoc bai
    [ ] 2. Nop bai SPQM

## Cấu trúc
- `todo.py`: toàn bộ logic
- `tasks.json`: dữ liệu (tự tạo khi chạy, không đưa lên git)