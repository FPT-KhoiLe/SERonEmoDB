# SERonEmoDB
## Notes: 
Đọc file SSH_Key_Create_Guide.md trước để biết cách setup SSH để sử dụng github.

Building a deep learning system for identifying and classifying emotions from speech data.

## Guide to setup
Run `pip install -r requirements.txt` để cài đặt toàn bộ requirements cần thiết trong thư viện. Notes: đây là phiên bản cổ đại nhất. Có lỗi gì feedback với Khôi Lê qua zalo `0981275337`

Lựa chọn thay thế: Run `conda env create -f environment.yml` để tạo môi trường conda.

Run `pip install -e .` trong thư mục repo gốc để chạy file `pyproject.toml`  

Run `pytest` để chạy test toàn bộ dự án.

KaggleHub không cho phép tải data cụ thể vào một specified path, cho nên mọi người tự tải data vào theo path sau : `/SERonEmoDB/datas/EmoDB/wav/` việc specified download để bên engineer làm.

