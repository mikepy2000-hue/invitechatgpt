"""Command-line entry point for the invite application."""
from __future__ import annotations

import argparse
from pathlib import Path

from .config import load_settings
from .email_sender import ConsoleEmailSender, SMTPEmailSender
from .invite_service import InviteService, InvalidEmailError


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="Tự động gửi invite ChatGPT Business khi nhập email",
    )
    parser.add_argument("email", help="Địa chỉ email cần mời")
    parser.add_argument(
        "--name",
        help="Tên người được mời (tùy chọn)",
        default=None,
    )
    parser.add_argument(
        "--audit-log",
        help="Đường dẫn lưu lịch sử gửi invite",
        default=None,
    )
    return parser


def main() -> None:
    parser = build_parser()
    args = parser.parse_args()

    settings = load_settings()
    audit_log = args.audit_log or settings.audit_log

    if settings.smtp_host and settings.smtp_port and settings.from_address:
        sender = SMTPEmailSender(
            host=settings.smtp_host,
            port=settings.smtp_port,
            from_address=settings.from_address,
            username=settings.smtp_username,
            password=settings.smtp_password,
            use_tls=settings.use_tls,
        )
    else:
        log_path = Path(audit_log).with_suffix(".log")
        sender = ConsoleEmailSender(log_file=str(log_path))

    service = InviteService(
        email_sender=sender,
        invite_link=settings.invite_link,
        audit_log=audit_log,
    )

    try:
        result = service.invite(email=args.email, name=args.name)
    except InvalidEmailError as exc:
        parser.error(str(exc))
        return

    print(
        "Đã gửi invite tới {email} lúc {timestamp}.".format(
            email=result.email,
            timestamp=result.timestamp.isoformat(),
        )
    )


if __name__ == "__main__":
    main()
