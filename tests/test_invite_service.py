"""Tests for the invite service."""
from __future__ import annotations

from datetime import datetime
from typing import Optional

import pytest

from app.invite_service import InviteService, InvalidEmailError


class DummySender:
    def __init__(self) -> None:
        self.sent = []

    def send_invite(self, email: str, invite_link: str, name: Optional[str]) -> None:
        self.sent.append((email, invite_link, name))


def test_invite_sends_email_and_logs(tmp_path):
    sender = DummySender()
    audit_log = tmp_path / "audit.log"
    service = InviteService(sender, "https://example.com/invite", str(audit_log))

    result = service.invite("user@example.com", name="Người Dùng")

    assert sender.sent == [("user@example.com", "https://example.com/invite", "Người Dùng")]
    assert audit_log.read_text(encoding="utf-8").split("\t")[1] == "user@example.com"
    assert isinstance(result.timestamp, datetime)


def test_invite_rejects_invalid_email(tmp_path):
    sender = DummySender()
    audit_log = tmp_path / "audit.log"
    service = InviteService(sender, "https://example.com/invite", str(audit_log))

    with pytest.raises(InvalidEmailError):
        service.invite("invalid-email")

    assert sender.sent == []
