# Web-app Thống Kê Lỗi Hệ Thống Abnormal Log Manager

## Mục đích:

Các link log query trong splunk thường rất dài nên app được tạo ra để rút gọn lại các link query, đồng thời tổng hợp các event bất thường lại vào một nơi để theo dõi một cách trực quan hơn. Các issue được tạo sẽ lưu vào trong database

## Công nghệ:

- Frontend: Python, Flask, HTML, Jinja2
- Backend: C#, [ASP.NET](http://ASP.NET), Entity Framework
    
    [ShortLinkAPI(Old)](https://www.notion.so/ShortLinkAPI-Old-20691f52357a8068b6abf64d2d10f66a?pvs=21)
    
- Database: PostgreSQL

## Chức năng chính:

### **Create Issue**

- Nhập Event Original URL
- Chọn team (OPS, OMS, TMS, WMS)
- Chọn level imapct (Warn, Error, Fatal)
- Sau khi hoàn tất confirm để tạo short url và sau đó lưu và database (hiện tại: SQL Server)

![image.png](attachment:f0920361-ffeb-407b-a0fa-8f1afb7c9145:image.png)

### **Dashboard**

- Load dữ liệu event từ trong database show lên dashboard
- Show tất cả thông tin của event
- Các actions tương tác với dashboard: Xem chi tiết event, Soft-delete (set isDelete = true), Hard-delete khỏi database, test redirect
- Filter theo Ngày tạo, Team, Impact Level
- Sort theo ID/Team/Level/Ngày tạo với thứ tự tăng dần/giảm dần

![image.png](attachment:7eab2df2-a04f-439c-801d-384f40c9a29e:image.png)

### **Statistic**

- Tổng hợp số lượng tất cả event đang lưu trong hệ thống
- Pie Chart: phân loại theo team và level, có nút để switch view giữa team và level
- Bar Graph: phân loại event theo level và team, có drop down để switch giữa các team
- Cả Pie Chart và Bar Graph đều có thể filter theo ngày (1 ngày, 3 ngày, 1 tuần, 1 tháng)
- Recent Events: các issue được tạo gần đây

![image.png](attachment:9a0878e1-3246-44f1-82cb-c15061f93605:image.png)

![image.png](attachment:f569a0df-34aa-492a-88db-31b4917d78c4:image.png)

## Known Bugs:

- Sau khi soft-delete thì ko thể permanent-delete được
- Recent events chưa sắp xếp theo ngày tạo mới nhất, dẫn đến những issue tạo sau này có thể không xuất hiện trên list
- Recent events format giờ hơi sai so với giờ địa phương (có vẻ do mặc định utc hay thì utc+7)

## TODO:

- TODO: new-feat để thống kê mỗi team có các event level impact nào
e.g: Team TMS có 10 event ở level Warn, 6 ở level Error, 1 ở Level Fatal (done 19/6)
- Thống kê theo tháng (done 19/6)
- Chắc bỏ không hiển thị ID lên trang web (view ID trên web thấy không có tác dụng gì cả)

REPO: https://github.com/orgs/abnormal-log-manager/dashboard
