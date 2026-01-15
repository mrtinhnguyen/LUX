# Hướng dẫn Public Thư viện LUX & Deploy Website LUX

Tài liệu này hướng dẫn chi tiết cách phát hành thư viện `lux-format` lên PyPI và triển khai trang web tài liệu/công cụ lên Vercel.

---

## 📦 1. Public Thư viện lên PyPI

Chúng ta sử dụng bộ công cụ đã được thiết lập sẵn trong dự án LUX.

### Bước 1: Chuẩn bị tài khoản
1. Tạo tài khoản trên [PyPI](https://pypi.org/) và [TestPyPI](https://test.pypi.org/).
2. Tạo **API Token** cho mỗi hệ thống và lưu lại an toàn.

### Bước 2: Build và Upload thử nghiệm (TestPyPI)
Dự án được tối ưu để sử dụng `uv`. Nếu môi trường Python máy bạn gặp lỗi, hãy dùng `uv run` để tạo môi trường sạch:
```bash
# Đảm bảo dùng Python 3.12 sạch qua uv
uv run --python 3.12 python scripts/publish.py --env test
```
*   Nhập `__token__` làm username.
*   Nhập API Token của TestPyPI làm password.

### Bước 3: Public chính thức (PyPI)
Khi mọi thứ đã sẵn sàng:
```bash
uv run --python 3.12 python scripts/publish.py --env prod
```
*   Nhập `__token__` làm username.
*   Nhập API Token của PyPI làm password.

---

## 🌐 2. Deploy lên Vercel

Để chạy công cụ LUX (nén/giải nén trực tuyến) như một web app trên Vercel:

### Bước 1: Chuẩn bị mã nguồn Frontend
Nếu bạn có một trang web (ví dụ viết bằng Next.js hoặc Vite), hãy đảm bảo thư mục dự án có cấu trúc phù hợp. Để demo nhanh, bạn có thể sử dụng cấu trúc sẵn có của project LUX (nếu có thư mục `web/` hoặc `docs/`).

### Bước 2: Cài đặt Vercel CLI
```bash
npm install -g vercel
```

### Bước 3: Phân tích cấu trúc Deploy
Vercel hỗ trợ Python Serverless Functions. Bạn có thể tạo folder `api/` ở root:

```python
# api/convert.py
from http.server import BaseHTTPRequestHandler
import json
import lux

class handler(BaseHTTPRequestHandler):
    def do_POST(self):
        content_length = int(self.headers['Content-Length'])
        post_data = self.rfile.read(content_length)
        data = json.loads(post_data)
        
        # Nén dữ liệu JSON sang LUX
        result = lux.encode(data)
        
        self.send_response(200)
        self.send_header('Content-Type', 'text/plain')
        self.end_headers()
        self.wfile.write(result.encode())
```

### Bước 4: Chạy lệnh Deploy
Mở terminal tại thư mục project và gõ:
```bash
vercel
```
Vercel sẽ tự động:
1. Nhận diện project Python.
2. Cài đặt các dependencies từ `pyproject.toml` hoặc `requirements.txt`.
3. Cung cấp URL chính thức (ví dụ: `lux.tonyx.dev` nếu bạn đã cấu hình tên miền).

### Bước 5: Cấu hình Tên miền (`lux.tonyx.dev`)
1. Truy cập Vercel Dashboard -> Project Settings -> Domains.
2. Add domain `lux.tonyx.dev`.
3. Cấu hình CNAME/A record trong DNS của bạn theo hướng dẫn của Vercel.

---

## 🛠 3. Tự động hóa với GitHub Actions
Bạn có thể cấu hình để mỗi khi push lên thư mục `main`, hệ thống tự động deploy:
1. File cấu hình: `.github/workflows/deploy.yml`.
2. Connect Repo với Vercel trên giao diện web của Vercel.

Mọi thay đổi trên repository `mrtinhnguyen/LUX` sẽ lập tức được cập nhật lên trang web chính thức.
