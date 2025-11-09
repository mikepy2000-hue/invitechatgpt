"""Configuration helpers for the invite application."""
from __future__ import annotations

from dataclasses import dataclass
import os
from typing import Optional


@dataclass
class Settings:
    """Runtime configuration for the invite application."""

    invite_link: str
    smtp_host: Optional[str]
    smtp_port: Optional[int]
    smtp_username: Optional[str]
    smtp_password: Optional[str]
    from_address: Optional[str]
    use_tls: bool
    audit_log: str


def _get_bool(name: str, default: bool) -> bool:
    value = os.getenv(name)
    if value is None:
        return default
    return value.strip().lower() in {"1", "true", "yes", "on"}


def load_settings() -> Settings:
    """Load configuration from environment variables.

    The function applies sensible defaults so that the application can run
    without additional configuration. When SMTP configuration is not provided
    the application falls back to logging invites locally.
    """

    invite_link = os.getenv(
        "CHATGPT_BUSINESS_INVITE_LINK",
        "https://chat.openai.com/",
    )
    smtp_host = os.getenv("INVITE_SMTP_HOST") or None
    smtp_port_str = os.getenv("INVITE_SMTP_PORT")
    smtp_port = int(smtp_port_str) if smtp_port_str else None
    settings = Settings(
        invite_link=invite_link,
        smtp_host=smtp_host,
        smtp_port=smtp_port,
        smtp_username=os.getenv("INVITE_SMTP_USERNAME") or None,
        smtp_password=os.getenv("INVITE_SMTP_PASSWORD") or None,
        from_address=os.getenv("INVITE_FROM_ADDRESS") or None,
        use_tls=_get_bool("INVITE_SMTP_USE_TLS", True),
        audit_log=os.getenv("INVITE_AUDIT_LOG", "invite_audit.log"),
    )
    return settings
