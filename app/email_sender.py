"""Email sender implementations for the invite application."""
from __future__ import annotations

from abc import ABC, abstractmethod
from email.message import EmailMessage
from pathlib import Path
import smtplib
from typing import Optional


class EmailSender(ABC):
    """Abstract base class for email delivery backends."""

    @abstractmethod
    def send_invite(self, email: str, invite_link: str, name: Optional[str]) -> None:
        """Send an invite to ``email`` with the provided invite link."""


class SMTPEmailSender(EmailSender):
    """Deliver invites through an SMTP server."""

    def __init__(
        self,
        host: str,
        port: int,
        from_address: str,
        username: Optional[str] = None,
        password: Optional[str] = None,
        use_tls: bool = True,
    ) -> None:
        self.host = host
        self.port = port
        self.username = username
        self.password = password
        self.use_tls = use_tls
        self.from_address = from_address

    def send_invite(self, email: str, invite_link: str, name: Optional[str]) -> None:
        message = EmailMessage()
        message["Subject"] = "Bạn được mời tham gia ChatGPT Business"
        message["From"] = self.from_address
        message["To"] = email
        greeting = f"Chào {name}," if name else "Xin chào,"
        message.set_content(
            f"""{greeting}

Bạn vừa được thêm vào danh sách mời của không gian ChatGPT Business.
Hãy nhấp vào liên kết sau để hoàn tất quá trình đăng ký: {invite_link}

Nếu bạn không mong đợi email này, vui lòng bỏ qua.
"""
        )

        with smtplib.SMTP(self.host, self.port) as server:
            if self.use_tls:
                server.starttls()
            if self.username and self.password:
                server.login(self.username, self.password)
            server.send_message(message)


class ConsoleEmailSender(EmailSender):
    """A fallback sender that persists invites to a local log file."""

    def __init__(self, log_file: str) -> None:
        self.log_file = Path(log_file)
        self.log_file.parent.mkdir(parents=True, exist_ok=True)

    def send_invite(self, email: str, invite_link: str, name: Optional[str]) -> None:
        greeting = f"Chào {name or 'bạn'}"
        content = f"{greeting}! Gửi invite tới {email} với link {invite_link}."
        with self.log_file.open("a", encoding="utf-8") as handle:
            handle.write(content + "\n")
