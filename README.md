# Quản Lý Hosts

Ứng dụng quản lý file hosts.json viết dành riêng cho tool Ping-monitor

https://blog.webdep24h.com/2024/11/ping-monitor.html

## 📂 Cài đặt và triển khai

### 1. Xóa và tạo lại môi trường ảo
Xóa thư mục env, dist, build...
```bash
rmdir /s /q env dist build
```
File Python có sử dụng các thư viện chính sau đây:

1. **PyQt6**: Cung cấp các thành phần GUI.
2. **pandas**: Để đọc và xử lý file Excel/CSV.
3. **json**: Để đọc và ghi dữ liệu JSON.
4. **csv**: Để xử lý file CSV cơ bản.
5. **os** (không được nhập, nhưng có thể cần thiết nếu bổ sung thao tác với hệ thống file).

## Dưới đây là các bước để thiết lập môi trường ảo và cài đặt đầy đủ các thư viện cần thiết:

### 1. Tạo môi trường ảo
Mở terminal và thực hiện:
```bash
python3 -m venv myenv
```
Thay `myenv` bằng tên bạn muốn cho môi trường ảo.

### 2. Kích hoạt môi trường ảo
- **Trên Linux/MacOS**:
  ```bash
  source myenv/bin/activate
  ```
- **Trên Windows**:
  ```cmd
  myenv\Scripts\activate
  ```

### 3. Cài đặt thư viện
Chạy lệnh sau để cài đặt các thư viện cần thiết:
```bash
pip install PyQt6 pandas
```

### 4. Kiểm tra phiên bản
Đảm bảo rằng bạn đã cài đặt đúng các thư viện với phiên bản tương thích:
```bash
pip freeze
```
Xác nhận rằng `PyQt6` và `pandas` đã được liệt kê trong danh sách.

### 5. Chạy chương trình
Khi môi trường đã được thiết lập, bạn có thể chạy chương trình của mình:
```bash
python Hosts.py
```

### Lưu ý
Nếu bạn muốn tạo file `requirements.txt` để tái sử dụng môi trường, bạn có thể làm như sau:
```bash
pip freeze > requirements.txt
```
Với file này, bạn chỉ cần dùng lệnh sau trên máy khác:
```bash
pip install -r requirements.txt
```
### 📌 Ghi chú


- **`hosts.json`**: Chứa danh sách các thiết bị theo dõi. Định dạng mẫu:
  ```json
  [
    {"host": "192.168.1.1", "name": "Router"},
    {"host": "google.com", "name": "Google"}
  ]


