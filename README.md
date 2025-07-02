# Tổng quan

**Abnormal Log Manager (ALM)** là một web app quản lý log lỗi, cho phép người dùng:

- Rút gọn các URL log lỗi dài dòng thành dạng ngắn gọn.
- Gắn nhãn cho mỗi log theo `Team` và `Mức độ lỗi (Level)` như: `Warn`, `Error`, `Fatal`.
- Theo dõi, tìm kiếm, và thống kê các lỗi theo từng nhóm/team và mức độ.
- Hiển thị dữ liệu qua giao diện biểu đồ (bar & pie charts).

Ứng dụng được xây dựng bằng:

- Backend: Python (Flask) kết nối đến một API dịch vụ .NET.
- Frontend: HTML/CSS sử dụng Jinja2 templating.
- API Backend: .NET Web API lưu trữ dữ liệu và xử lý ngắn URL.
# Document chi tiết
https://www.notion.so/Abnormal-Log-Manager-Documentation-22391f52357a80f5a1ccdbc302b87629?source=copy_link
## TODO

- ~~feat: thống kê mỗi team có các event level impact nào
e.g: Team TMS có 10 event ở level Warn, 6 ở level Error, 1 ở Level Fatal~~ (**done** 19/6)
- ~~feat: Thống kê theo tháng~~ (**done** 19/6)
- Điều chỉnh lại giao diện: e.g: https://comeout.netlify.app/demo/default/portfolio

---

## Source Code:

- Backend
    
    https://github.com/abnormal-log-manager/alm-backend
    
- Frontend
    
    https://github.com/abnormal-log-manager/alm-frontend
