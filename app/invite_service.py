"""Core invitation logic."""
from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime
from pathlib import Path
import re
from typing import Optional

from .email_sender import EmailSender

EMAIL_REGEX = re.compile(r"^[^@\s]+@[^@\s]+\.[^@\s]+$")


@dataclass
class InviteResult:
    email: str
    name: Optional[str]
    timestamp: datetime


class InvalidEmailError(ValueError):
    """Raised when an invalid email is provided."""


class InviteService:
    """Service responsible for validating and dispatching invites."""

    def __init__(self, email_sender: EmailSender, invite_link: str, audit_log: str) -> None:
        self.email_sender = email_sender
        self._invite_link = invite_link
        self.audit_log = Path(audit_log)
        if self.audit_log.parent and not self.audit_log.parent.exists():
            self.audit_log.parent.mkdir(parents=True, exist_ok=True)

    def validate_email(self, email: str) -> None:
        if not EMAIL_REGEX.match(email):
            raise InvalidEmailError(f"Địa chỉ email không hợp lệ: {email}")

    def invite(self, email: str, name: Optional[str] = None) -> InviteResult:
        self.validate_email(email)
        self.email_sender.send_invite(email=email, invite_link=self._invite_link, name=name)
        result = InviteResult(email=email, name=name, timestamp=datetime.utcnow())
        self._append_audit(result)
        return result

    def _append_audit(self, result: InviteResult) -> None:
        line = (
            f"{result.timestamp.isoformat()}\t{result.email}\t"
            f"{(result.name or '').strip()}\n"
        )
        with self.audit_log.open("a", encoding="utf-8") as handle:
            handle.write(line)
