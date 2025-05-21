# Hướng Dẫn Phối Hợp Team Build Package với MLOps

## 1. Tổng Quan

Tài liệu này hướng dẫn quy trình phối hợp giữa các thành viên trong team nhằm xây dựng, đóng gói và triển khai hệ thống nhận diện cảm xúc từ dữ liệu giọng nói, theo chuẩn MLOps. Đảm bảo mọi thành viên thực hiện đúng quy trình sẽ giúp dự án vận hành hiệu quả, dễ bảo trì và mở rộng.

---

## 2. Quy Ước Làm Việc Nhóm

- **Sử dụng GitHub để quản lý code:** Mỗi tính năng/bugfix nên được phát triển trên nhánh riêng và tạo Pull Request (PR) để review.
- **Đặt tên branch:**  
  - `feature/<ten-tinh-nang>`
  - `bugfix/<ten-loi>`
  - `experiment/<ten-thu-nghiem>`
- **Review code:** Mỗi PR cần ít nhất 1 người review trước khi merge vào main.

---

## 3. Tổ Chức Dự Án & Đóng Gói Module

- **Cấu trúc thư mục chuẩn:**
  ```
  project-root/
  ├── src/
  │   └── <tên_package>/
  ├── notebooks/
  ├── tests/
  ├── requirements.txt
  ├── setup.py
  ├── README.md
  └── .github/
      └── workflows/
  ```
- **Viết code module hóa:**  
  - Tách rời các thành phần: tiền xử lý, training, evaluation, inference, utils...
  - Không để notebook chứa logic chính, chỉ dùng cho minh họa hoặc thử nghiệm.
- **Viết test:**  
  - Đặt vào thư mục `tests/`
  - Sử dụng pytest cho unit test.

---

## 4. Quản Lý Phụ Thuộc & Đóng Gói

- **requirements.txt**: Ghi rõ phiên bản thư viện.
- **setup.py**: Khai báo metadata, entry_points nếu có CLI.
- **Hướng dẫn cài đặt nội bộ:**
  ```bash
  pip install -e .
  ```

---

## 5. CI/CD với GitHub Actions

- **Thiết lập workflow tự động:**
  - Kiểm tra code style (black, flake8)
  - Chạy unit test khi có PR
  - Build và publish package lên PyPI (nếu cần)

- **Ví dụ file workflow:**
  ```yaml
  name: CI Pipeline

  on: [push, pull_request]

  jobs:
    build:
      runs-on: ubuntu-latest
      steps:
        - uses: actions/checkout@v4
        - name: Setup Python
          uses: actions/setup-python@v5
          with:
            python-version: '3.10'
        - name: Install dependencies
          run: |
            pip install -r requirements.txt
            pip install pytest
        - name: Run tests
          run: pytest tests/
        - name: Lint code
          run: |
            pip install black flake8
            black --check src/
            flake8 src/
  ```

---

## 6. Quản Lý Model và Experiment

- **Dùng DVC (Data Version Control)** hoặc MLflow để quản lý data, model, kết quả experiment.
- **Không push dữ liệu lớn/model lên Git:** Dùng `.gitignore` và lưu ở DVC/S3/Google Drive.
- **Ghi chú các tham số, seed, kết quả vào log (MLflow hoặc notebook).**

---

## 7. Đảm Bảo Tái Sử Dụng & Reproducibility

- **Gắn phiên bản cho package và model.**
- **Tài liệu hóa hàm, module bằng docstring chuẩn.**
- **Cung cấp ví dụ sử dụng trong README.md hoặc docs.**

---

## 8. Môi Trường Làm Việc

- **Khuyến cáo dùng Python 3.10+**
- **Sử dụng virtualenv/conda cho môi trường ảo.**
- **Ghi rõ hướng dẫn setup môi trường trong README.**

---

## 9. Giao Tiếp & Báo Cáo

- **Giao tiếp qua Slack/Teams/Zalo, cập nhật tiến độ hàng ngày hoặc theo tuần.**
- **Tổ chức họp review sprint/retro định kỳ.**

---

## 10. Tài Liệu & Hỗ Trợ

- **Link tài liệu dự án:** [README.md]
- **Tham khảo về MLOps:**  
  - [MLOps by Microsoft](https://mlops.microsoft.com/)
  - [Cookiecutter Data Science](https://drivendata.github.io/cookiecutter-data-science/)
  - [DVC](https://dvc.org/)
  - [MLflow](https://mlflow.org/)

---

**Liên hệ leader/MLOps Dev khi gặp vấn đề ngoài phạm vi tài liệu này.**
