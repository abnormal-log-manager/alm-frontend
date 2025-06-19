# Web-app Thống Kê Lỗi Hệ Thống Abnormal Log Manager

## Mục đích:

Các link log query trong splunk thường rất dài nên app được tạo ra để rút gọn lại các link query, đồng thời tổng hợp các event bất thường lại vào một nơi để theo dõi một cách trực quan hơn. Các issue được tạo sẽ lưu vào trong database
Document chi tiết: https://www.notion.so/Web-app-Th-ng-K-L-i-H-Th-ng-Abnormal-Log-Manager-20791f52357a80f091dcdeebbf268a5d?source=copy_link

## Chức năng chính:
# Create issue
# Dashboard
# Statistic

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
