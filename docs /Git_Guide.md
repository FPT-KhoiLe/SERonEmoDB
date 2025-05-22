# Git "One for Life"

Tài liệu này tổng hợp các bước **đơn giản nhất** để bạn có thể :
- Tạo và thêm SSH key 
- Clone repository 
- Làm việc với branch local (tạo, chuyển)
- Thêm (add), commit, push code
- Cập nhật từ nhánh `main`

> Áp dụng cho cả Windows và Linux/MacOS 

## 1. Tạo SSH Key và thêm vào GitHub/GitLab
### 1.1. Kiểm tra SSH Key hiện có

```bash
ls ~/.ssh
```

Nếu thấy `id_rsa` / `id_rsa.pub` hoặc `id_ed25519`/`id_ed25519.pub` thì đã có key, bỏ qua bước tạo mới.

### 1.2 Tạo SSH Key mới (nếu chưa có)
```bash
ssh-keygen -t ed25519 -C "your-github-email@example.com"
```
- Nhấn `Enter` để lưu ở `~/.ssh/id_ed25519`.
- Nhập passphrase (khuyến nghị) hoặc để trống rồi `Enter`

### 1.3 Chạy SSH agent và load key 
```bash
# Khởi động agent
eval "$(ssh-agent -s)"

# Thêm key vào agent 
ssh-add ~/.ssh/id_ed25519
```

### 1.4 Sao chép public key lên clipboard
- Windows (Git Bash):
```bash
clip < ~/.ssh/id_ed25519.pub 
```

- MacOS:
```bash 
pbcopy < ~/.ssh/id_ed25519.pub 
```

- Linux (cài `xclip`):
```bash
 xclip -sel clip < ~/.ssh/id_ed25519.pub
```

### 1.5. Thêm SSH Key vào tài khoản
1. Đăng nhập vào GitHub -> **Setting** -> **SSH and GPG keys**
2. Nhấn **New SSH key**
3. Đặt **Title** (ví dụ: "Laptop cá nhân")
4. Dán (Ctr + V) public key vào ô **Key**
5. Nhấn **Add SSH Key**


## 2. Clone Repository qua SSH 
```bash
git clone git@github.com:<username>/<repo>.git
```
Sẽ tạo ra thư mục <repo> chứa toàn bộ mã nguồn + remote branch từ mã nguồn.

## 3. Làm việc với local branch
### 3.1. Tạo & chuyển sang branch mới 
```bash 
git checkout -b feature/ten-tinh-nang
```

### 3.2. Kiểm tra branch hiện tại 
```bash
git branch
```

## 4. Thêm, commit & push code 
### 4.1. Thêm file/thay đổi
```bash
git add <file> # thêm 1 file
# hoặc 
git add . # Thêm tất cả thay đổi
```
### 4.2 Ghi commit với message 
```bash
git commit -m "Your commit"
```

### 4.3. Đẩy branch lên remote lần đầu
```bash
git push -u origin <your branch name> # (trong ví dụ này mình sẽ dùng <feature/tên-tính-năng> hen)
```
> Sau này chỉ cần `git push` để đẩy tiếp trên branch cũ

## 5. Cập nhật nhánh `main` mới nhất
```bash
git fetch origin # tải về refs mới nhất
git checkout main # chuyển sang main
git pull origin main # merge remote/main
```

## 6. Mẹo & Lưu ý 
- Viết **commit message** rõ ràng, bắt đầu bằng các động từ: `Add`, `Fix`, `Update`, `Remove`.
- **Không commit** file nhạy cảm (API keys) - thêm API keys file vào `.gitignore`.
- **Pull main** (cập nhật mã nguồn local) trước khi bắt đầu làm feature mới để tránh conflict sau khi push.
- **Xóa branch** sau khi merge: `git branch -d feature/xxx`

## 7. Bảng tóm tắt lệnh

| Nhiệm vụ              | Lệnh                                         |
| --------------------- | -------------------------------------------- |
| Kiểm tra SSH Key      | `ls ~/.ssh`                                  |
| Tạo SSH Key           | `ssh-keygen -t ed25519 -C "you@example.com"` |
| Clone repo qua SSH    | `git clone git@github.com:...`               |
| Tạo & chuyển branch   | `git checkout -b <branch>`                   |
| Thêm thay đổi         | `git add <file>` / `git add .`               |
| Commit thay đổi       | `git commit -m "message"`                    |
| Push branch (lần đầu) | `git push -u origin <branch>`                |
| Push (các lần sau)    | `git push`                                   |
| Cập nhật `main`       | `git pull origin main`                       |
| Xóa branch local      | `git branch -d <branch>`                     |

---

*Giờ thì bạn đã có ****"One for Life"**** Git cheat-sheet!*
