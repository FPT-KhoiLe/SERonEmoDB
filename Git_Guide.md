# Hướng dẫn thêm SSH Key trên Windows

Hướng dẫn này áp dụng cho Windows, sử dụng Git Bash (hoặc Windows Terminal có cài Git) để tạo và thêm SSH Key cho GitHub, GitLab hoặc server từ xa.

---

## 1. Cài đặt Git Bash

1. Truy cập trang Git: [https://git-scm.com/downloads](https://git-scm.com/downloads)
2. Tải và cài đặt bản Windows (Git for Windows).
3. Hoàn tất cài đặt, mở **Git Bash** hoặc **Windows Terminal** có Git.

---

## 2. Kiểm tra xem đã có SSH Key chưa

Trong Git Bash, chạy:

```bash
ls ~/.ssh
```

Nếu có file `id_rsa`/`id_rsa.pub` hoặc `id_ed25519`/`id_ed25519.pub`, bạn đã có SSH Key. Nếu chưa có, sang bước tiếp theo.

---

## 3. Tạo SSH key mới

Tạo SSH Key với thuật toán Ed25519:

```bash
ssh-keygen -t ed25519 -C "youremail@example.com"
```

* Khi hỏi `Enter file in which to save the key`, nhấn **Enter** để lưu ở đường dẫn mặc định: `C:\Users\<YourUser>/.ssh/id_ed25519`.
* Khi hỏi `Enter passphrase`, bạn có thể nhập passphrase (khuyến nghị) hoặc để trống rồi nhấn **Enter**.

---

## 4. Khởi động SSH agent và load key

1. Khởi động SSH agent:

   ```bash
   eval "$(ssh-agent -s)"
   ```
2. Thêm private key vào agent:

   ```bash
   ssh-add ~/.ssh/id_ed25519
   ```

---

## 5. Sao chép public key

Trong Git Bash, chạy:

```bash
clip < ~/.ssh/id_ed25519.pub
```

Lệnh này sẽ copy nội dung file `id_ed25519.pub` lên clipboard. Bạn có thể paste trực tiếp sau.

---

## 6. Thêm SSH Key vào GitHub/GitLab

1. Đăng nhập vào GitHub/GitLab.
2. Vào:

   * GitHub: **Settings → SSH and GPG keys**
   * GitLab: **User Settings → SSH Keys**
3. Nhấn **New SSH key** hoặc **Add key**.
4. Nhập **Title** (ví dụ: “Windows Laptop”).
5. Dán (Ctrl+V) public key từ clipboard.
6. Nhấn **Add SSH key** (GitHub) hoặc **Add key** (GitLab).

---

## 7. Kiểm tra kết nối

Chạy lệnh:

```bash
ssh -T git@github.com
```

Lần đầu sẽ hỏi `Are you sure you want to continue connecting (yes/no)?`, gõ **yes** và nhấn **Enter**.

Nếu thấy:

```
Hi username! You've successfully authenticated...
```

thì quá trình đã thành công.

---

## 8. (Tùy chọn) Cấu hình Git user

```bash
git config --global user.name "Tên của bạn"
git config --global user.email "youremail@example.com"
```

---

**Hoàn thành!**

Giờ bạn có thể dùng Git qua SSH trên Windows mà không cần nhập mật khẩu mỗi lần tương tác với remote repository.

# Hướng dẫn các lệnh cơ bản trong quá trình làm việc 

```bash
git clone git@github.com:FPT-KhoiLe/SERonEmoDB.git
```
Chạy lệnh này đầu tiên để clone toàn bộ repo về máy (trong thư mục của repo này sẽ chứa cả các git branch bao gồm cả main branch, mình không muốn nói quá nhiều về branch, mọi người hãy tự nghiên cứu hoặc hỏi AI nhé!) 

```bash
git checkout -b <branch_name>
```

Chạy lệnh này để tạo ra một 'local branch', dùng nó để push lên cho master branch kiểm tra sau đó mới merge vào main branch.

NHẤT ĐỊNH PHẢI CHẠY CHECKOUT, NHẤT ĐỊNH PHẢI CHẠY CHECKOUT, NHẤT ĐỊNH PHẢI CHẠY CHECKOUT 

Sau khi đã code xong phần của mình, để push code lên ta thực hiện các chuỗi lệnh 
```bash
git add . 
git commit -m "<Content>"
git push
```

Khi có người đã update code, để update repo local ta sử dụng lệnh 
```bash
git pull origin main
```

Lệnh này sẽ giúp mọi người update được toàn bộ thay đổi sau khi người khác push code lên.
Sau khi ban đầu chạy `git clone` thì mỗi lần mọi người bật máy lên, hãy cứ chạy lệnh trên cho mình để update code người khác đã làm.


