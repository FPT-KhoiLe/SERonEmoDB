# Hướng dẫn sử dụng pytest

Tài liệu này giúp bạn nhanh chóng cài đặt, viết và chạy unit tests với **pytest** cho dự án Python.

---

## 1. Cài đặt pytest

Nếu bạn dùng **conda**:

```bash
conda activate my-project-env
conda install -c conda-forge pytest
```

Hoặc dùng **pip**:

```bash
pip install pytest
```

> Phiên bản pytest tối thiểu khuyến nghị: **7.x**

---

## 2. Cấu trúc thư mục tests

Tạo thư mục `tests/` ngay dưới root của project:

```
project-root/
├── src/
└── tests/
    ├── test_example.py    # Ví dụ
    └── test_*.py          # Tất cả file bắt đầu bằng `test_`
```

**Lưu ý**: pytest tự động nhận dạng mọi file, mọi hàm/chương trình có tên:

* File: `test_*.py` hoặc `*_test.py`
* Hàm: `def test_*(…):`
* Class: `class Test*:` (không có phương thức `__init__`)

---

## 3. Viết test đầu tiên

Giả sử bạn có trong `src/utils.py` hàm:

```python
# src/utils.py

def add(a, b):
    """Trả về tổng của a và b"""
    return a + b
```

Tạo file `tests/test_utils.py` chứa:

```python
# tests/test_utils.py

from src.utils import add

def test_add_positive():
    assert add(2, 3) == 5

def test_add_negative():
    assert add(-1, -4) == -5
```

---

## 4. Chạy tests

Tại thư mục root, đảm bảo environment đã activate, chạy:

```bash
pytest
```

* Pytest sẽ scan `tests/` và hiển thị kết quả pass/fail.
* Khi test fail, pytest in chi tiết diff để debug nhanh.

**Một số option hữu ích**:

* `pytest -q` (quiet): tóm tắt ngắn gọn.
* `pytest -v` (verbose): show tên test chi tiết.
* `pytest --maxfail=1` dừng sau 1 lỗi.
* `pytest --durations=5` hiển thị 5 test tốn thời gian lâu nhất.

---

## 5. Sử dụng fixtures

Fixtures giúp setup/teardown data hoặc resource dùng chung:

```python
# tests/conftest.py
import pytest

@ pytest.fixture
def sample_data(tmp_path):
    data_file = tmp_path / "data.txt"
    data_file.write_text("1,2,3,4")
    return data_file
```

Sử dụng fixture trong test:

```python
# tests/test_data_ingest.py

def test_read_data(sample_data):
    from src.data_ingest import read_data
    data = read_data(sample_data)
    assert isinstance(data, list)
```

---

## 6. Tích hợp với CI

Trong file `.github/workflows/ci.yml` (hoặc tương tự), thêm job test:

```yaml
jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      - name: Setup conda
        uses: conda-incubator/setup-miniconda@v2
        with:
          environment-file: environment.yml
          activate-environment: my-project-env
      - name: Install pytest
        run: pip install pytest
      - name: Run tests
        run: pytest --maxfail=1 --disable-warnings -q
```

---

## 7. Mẹo & best practices

* **Đặt tên test** rõ ràng, mô tả hành vi: `test_<func>_<condition>_returns_<expected>`.
* Giữ test **độc lập** và **nhanh**.
* Không commit test fail; chạy `pytest` trước khi push.
* Kết hợp **coverage** nếu cần: `pip install pytest-cov` và `pytest --cov=src`.

---

*Giờ bạn đã sẵn sàng viết và chạy unit tests cho dự án!*
