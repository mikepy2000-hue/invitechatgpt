# Ứng dụng gửi invite ChatGPT Business

Ứng dụng dòng lệnh đơn giản giúp bạn tự động gửi lời mời tham gia không gian
ChatGPT Business của riêng mình khi người dùng cung cấp địa chỉ email. Hệ thống
có thể gửi email thật qua SMTP hoặc chỉ ghi lại lời mời vào file log để thử
nghiệm.

## Chuẩn bị môi trường

1. Cài đặt Python 3.10 trở lên.
2. (Tuỳ chọn) tạo virtualenv rồi kích hoạt.
3. Cài đặt phụ thuộc cho kiểm thử:

```bash
pip install -r requirements.txt
```

## Cấu hình

Ứng dụng đọc cấu hình qua biến môi trường. Các biến quan trọng:

| Biến | Ý nghĩa | Giá trị mặc định |
|------|---------|------------------|
| `CHATGPT_BUSINESS_INVITE_LINK` | Liên kết invite gửi cho người dùng | `https://chat.openai.com/` |
| `INVITE_SMTP_HOST` | Host SMTP (để gửi email thật) | *(không bắt buộc)* |
| `INVITE_SMTP_PORT` | Cổng SMTP | *(không bắt buộc)* |
| `INVITE_SMTP_USERNAME` | Tên đăng nhập SMTP | *(không bắt buộc)* |
| `INVITE_SMTP_PASSWORD` | Mật khẩu SMTP | *(không bắt buộc)* |
| `INVITE_SMTP_USE_TLS` | `true/false`, bật STARTTLS | `true` |
| `INVITE_FROM_ADDRESS` | Địa chỉ email người gửi | *(không bắt buộc)* |
| `INVITE_AUDIT_LOG` | File lưu lịch sử gửi invite | `invite_audit.log` |

Khi thiếu cấu hình SMTP, ứng dụng sẽ tự động chuyển sang chế độ ghi log cục bộ
(`ConsoleEmailSender`).

## Cách chạy

Gửi invite cho một email:

```bash
python -m app.main user@example.com --name "Tên người dùng"
```

Nếu email hợp lệ, ứng dụng sẽ báo kết quả thành công và ghi vào file audit.

## Kiểm thử

Chạy toàn bộ test với `pytest`:

```bash
pytest
```
