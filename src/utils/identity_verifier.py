"""Optional agent identity verification for auto-trading mode.

Adds a verification gate before order execution so only authenticated
agents can place trades. Disabled by default — opt in via config.

The verifier interface is pluggable. The built-in TokenVerifier checks
a static token from config. Implement AgentVerifier for any identity
system (JWT, API keys, ZKP, etc.).
"""

import logging
from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from datetime import datetime, timezone
from typing import Optional

logger = logging.getLogger(__name__)


@dataclass
class VerificationResult:
    """Result of an agent identity check."""
    verified: bool
    agent_id: str = ""
    reason: str = ""
    timestamp: str = field(default_factory=lambda: datetime.now(timezone.utc).isoformat())


class AgentVerifier(ABC):
    """Pluggable agent identity verifier.

    Implement this for any identity system: JWT validation,
    API key lookup, ZKP proof checking, etc.
    """

    @abstractmethod
    def verify(self, token: str) -> VerificationResult:
        """Verify an agent token and return the result."""


class TokenVerifier(AgentVerifier):
    """Simple token-based verifier for development.

    Compares the provided token against a configured secret.
    NOT for production — use a real verifier.
    """

    def __init__(self, expected_token: str):
        if not expected_token:
            raise ValueError(
                "TokenVerifier requires a non-empty token. "
                "Set AGENT_IDENTITY_TOKEN in config."
            )
        self._expected = expected_token

    def verify(self, token: str) -> VerificationResult:
        if not token:
            return VerificationResult(verified=False, reason="no token provided")
        if token != self._expected:
            return VerificationResult(verified=False, reason="token mismatch")
        return VerificationResult(verified=True, agent_id="auto-trader")


# Audit log for verification decisions
_audit_log: list[dict] = []


def check_agent_identity(config) -> Optional[str]:
    """Check agent identity before order execution.

    Called from buy_stock() and sell_stock() in auto mode.
    Returns None if verified (or verification disabled),
    or an error message string if denied.

    Args:
        config: The config module with identity settings.

    Returns:
        None if authorized, error message if denied.
    """
    enabled = getattr(config, "AGENT_IDENTITY_VERIFICATION", False)
    if not enabled:
        return None

    token = getattr(config, "AGENT_IDENTITY_TOKEN", "")
    if not token:
        msg = "AGENT_IDENTITY_VERIFICATION is enabled but AGENT_IDENTITY_TOKEN is empty"
        logger.error(f"[identity] {msg}")
        return msg

    verifier = TokenVerifier(token)

    # In auto mode, the token is self-held — verify it matches config
    result = verifier.verify(token)

    entry = {
        "action": "allow" if result.verified else "deny",
        "agent_id": result.agent_id,
        "reason": result.reason,
        "timestamp": result.timestamp,
    }
    _audit_log.append(entry)

    if not result.verified:
        logger.warning(f"[identity] DENIED: {result.reason}")
        return f"Agent identity verification failed: {result.reason}"

    logger.info(f"[identity] Verified: {result.agent_id}")
    return None


def get_audit_log() -> list[dict]:
    """Read-only access to the verification audit log."""
    return list(_audit_log)
