# Abnormal Log Manager – Documentation
## 📚 Mục lục

- [Tổng quan](#tổng-quan)
- [Các chức năng chính](#các-chức-năng-chính)
  - [1. Tạo Short Link (Create)](#1-tạo-short-link-create)
  - [2. Quản lý URL Log (Dashboard)](#2-quản-lý-url-log-dashboard)
  - [3. Thống kê lỗi (Statistics)](#3-thống-kê-lỗi-statistics)
  - [4. Export & Import dữ liệu](#4-export--import-dữ-liệu)
- [Cấu trúc dữ liệu](#cấu-trúc-dữ-liệu)
- [Các route chính](#các-route-chính)
- [Giao diện & UX](#giao-diện--ux)
- [Công nghệ sử dụng](#công-nghệ-sử-dụng)
- [TODO](#todo)
- [Source Code](#source-code)
- [Document chi tiết](#document-chi-tiết)

---
# Tổng quan

**Abnormal Log Manager (ALM)** là một web app quản lý log lỗi, cho phép người dùng:

- Rút gọn các URL log lỗi dài dòng thành dạng ngắn gọn, sau đó lưu xuống database.
- Gắn nhãn cho mỗi log theo `Team` như: `OPS`, `OMS`, `TMS`, `WMS` và `Mức độ lỗi (Level)` như: `Warn`, `Error`, `Fatal`.
- Theo dõi, tìm kiếm, và thống kê các lỗi theo từng nhóm/team và mức độ.
- Hiển thị dữ liệu qua giao diện biểu đồ (bar & pie charts).
- Export & Import file excel chứa dữ liệu của database

Ứng dụng được xây dựng bằng:

- Backend: Python (Flask) kết nối đến một API dịch vụ .NET.
- Frontend: HTML/CSS sử dụng Jinja2 templating.
- API Backend: .NET Web API lưu trữ dữ liệu và xử lý rút gọn URL.
- Database: PostgreSQL

---

## Các chức năng chính

### 1. Tạo Short Link (Create)



**Đường dẫn**: `/create`

- Nhập:
    - URL log lỗi cần rút gọn.
    - Title (optional)
- Chọn:
    - Team phụ trách (`OPS`, `OMS`, `TMS`, `WMS`).
    - Mức độ lỗi (`Warn`, `Error`, `Fatal`).
- Hệ thống gửi dữ liệu đến API, tạo URL rút gọn.
- Nếu thành công: lưu vào database sau đó redirect về dashboard với thông báo thành công.
- Chi tiết cơ chế shorten URL và redirect short URL API:
    
    
    

### 2. Quản lý URL Log (Dashboard)



**Đường dẫn**: `/`

- Hiển thị danh sách các log event dưới dạng bảng:
    - ID, Original URL, Shortened URL, Team, Level, Thời gian tạo.
- Các chức năng hỗ trợ:
    - Tìm kiếm theo keyword (gốc hoặc rút gọn).
    - Lọc theo Team, Level, Ngày tạo.
    - Sắp xếp theo ID, Level, Team, Ngày tạo.
    - Hard delete.
    - Sao chép URL rút gọn.
- Phân trang và chọn số lượng bản ghi mỗi trang.

### 3. Thống kê lỗi (Statistics)

**Đường dẫn**: `/stats`

- Hiển thị tổng số log lỗi theo:
    - Mức độ (`Warn`, `Error`, `Fatal`) bằng **thẻ số lớn**.
    
    
    
    - Biểu đồ **pie chart** cho:
        - Phân phối lỗi theo Team.
        - Phân phối lỗi theo Level.
    
    
    
    - Biểu đồ **bar chart** cho:
        - Mức độ lỗi của từng Team.
    
    
    
- Cho phép lọc theo thời gian: 1 ngày, 3 ngày, 7 ngày, 30 ngày.
    
    
    
- Hiển thị bảng các lỗi mới nhất ở cuối trang.



---

### 4. Export & Import dữ liệu



**Đường dẫn:** `/`

- Export:
    - Xuất toàn bộ dữ liệu từ bảng `ShortUrls` trong database ra một file Excel:
- Import:
    - Nhận một file Excel, đọc từng dòng và cập nhật hoặc thêm dữ liệu vào database.

### Cấu trúc dữ liệu

Một URL Log gồm:

| Trường | Ý nghĩa |
| --- | --- |
| `id` | Mã định danh duy nhất |
| `originalUrl` | URL gốc dài |
| `shortenedUrl` | URL rút gọn |
| `team` | Nhóm phụ trách log lỗi (`OPS`, `OMS`, `TMS`, `WMS`) |
| `level` | Mức độ nghiêm trọng (`Warn`, `Error`, `Fatal`) |
| `createDate` | Thời gian tạo (UTC trong database, GMT+7 khi hiển thị lên web) |
| `isDeleted` | Đã bị xoá mềm hay chưa |

---

## Các route chính

| Route | Phương thức | Mô tả |
| --- | --- | --- |
| `/` | GET | Trang dashboard với bảng log |
| `/create` | POST | Trang tạo mới URL log |
| `/stats` | GET | Trang thống kê dữ liệu |
| `/search?query=...` | GET | Tìm kiếm URL |
| `/delete/<id>` | DELETE | Xoá cứng một log |
| `/api/urls` | GET | Trả về JSON danh sách URL – dùng cho AJAX |

---

## Giao diện & UX

Ứng dụng có giao diện hiện đại với:

- **Navbar** điều hướng chính: Dashboard, Create, Statistics.
- **Form thân thiện** khi nhập URL, chọn team/level.
- **Thống kê sống động** bằng biểu đồ Chart.js.

---

## Công nghệ sử dụng

| Thành phần | Công nghệ |
| --- | --- |
| Web Framework | Flask |
| Giao diện | HTML5, CSS3 (custom), Chart.js |
| API backend | ASP.NET Web API |
| Templating | Jinja2 |
| API call | Python `requests` |
| Deployment (đề xuất) | Docker / Kubernetes |

---

## TODO

- ~~feat: thống kê mỗi team có các event level impact nào
e.g: Team TMS có 10 event ở level Warn, 6 ở level Error, 1 ở Level Fatal~~ (**done** 19/6)
- ~~feat: Thống kê theo tháng~~ (**done** 19/6)
- ~~Điều chỉnh lại giao diện: e.g: https://comeout.netlify.app/demo/default/portfolio~~ (**done** 10/7)
- ~~feat: Import & Export~~ (**done** 11/7)

---

## Source Code:

- Backend
    
    https://github.com/abnormal-log-manager/alm-backend
    
- Frontend
    
    https://github.com/abnormal-log-manager/alm-frontend

## Document chi tiết
- https://www.notion.so/Abnormal-Log-Manager-Documentation-22391f52357a80f5a1ccdbc302b87629?source=copy_link
