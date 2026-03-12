"""License rights checking for content access decisions.

Implements ADR-0003 (License and provenance first) by classifying arXiv
license URIs and making deployment-mode-aware access decisions. Local
deployments allow all access with warnings; hosted deployments block
non-permissive licenses.
"""

from __future__ import annotations

from arxiv_mcp.content.models import AccessDecision


class RightsChecker:
    """Checks license rights and returns access decisions.

    Classifies the 6 arXiv license URIs into permissive vs personal-use:

    Permissive (hosted OK):
    - CC BY 4.0
    - CC BY-SA 4.0
    - CC0 1.0 (public domain)

    Personal-use only (local OK, hosted blocked):
    - arXiv nonexclusive distribution
    - CC BY-NC-SA 4.0
    - CC BY-NC-ND 4.0

    Unknown/None licenses are treated as restrictive (blocked in hosted).
    """

    PERMISSIVE_LICENSES: set[str] = {
        "http://creativecommons.org/licenses/by/4.0/",
        "http://creativecommons.org/licenses/by-sa/4.0/",
        "http://creativecommons.org/publicdomain/zero/1.0/",
    }

    PERSONAL_USE_LICENSES: set[str] = {
        "http://arxiv.org/licenses/nonexclusive-distrib/1.0/",
        "http://creativecommons.org/licenses/by-nc-sa/4.0/",
        "http://creativecommons.org/licenses/by-nc-nd/4.0/",
    }

    def check_access(
        self, license_uri: str | None, deployment_mode: str
    ) -> AccessDecision:
        """Check whether content access is allowed for the given license.

        Args:
            license_uri: The arXiv license URI, or None if unknown.
            deployment_mode: Either "local" or "hosted".

        Returns:
            AccessDecision with allowed status and optional reason/warning.
        """
        if license_uri is None:
            return self._decide_unknown(deployment_mode)

        if license_uri in self.PERMISSIVE_LICENSES:
            return self._decide_permissive(license_uri, deployment_mode)

        if license_uri in self.PERSONAL_USE_LICENSES:
            return self._decide_personal_use(license_uri, deployment_mode)

        # Unknown license URI -- treat as restrictive
        return self._decide_unknown(deployment_mode, license_uri)

    def _decide_permissive(
        self, license_uri: str, deployment_mode: str
    ) -> AccessDecision:
        """Permissive license: always allowed, local mode adds informational warning."""
        if deployment_mode == "local":
            return AccessDecision(
                allowed=True,
                warning=f"Local mode: content used under {license_uri}",
            )
        return AccessDecision(allowed=True)

    def _decide_personal_use(
        self, license_uri: str, deployment_mode: str
    ) -> AccessDecision:
        """Personal-use license: allowed locally with warning, blocked in hosted."""
        if deployment_mode == "local":
            return AccessDecision(
                allowed=True,
                warning=(
                    f"Personal/research use only under {license_uri}. "
                    "Do not redistribute."
                ),
            )
        return AccessDecision(
            allowed=False,
            reason=(
                f"License {license_uri} restricts redistribution. "
                "Content not available in hosted mode."
            ),
        )

    def _decide_unknown(
        self, deployment_mode: str, license_uri: str | None = None
    ) -> AccessDecision:
        """Unknown or missing license: allowed locally with warning, blocked in hosted."""
        uri_desc = license_uri if license_uri else "unknown"
        if deployment_mode == "local":
            return AccessDecision(
                allowed=True,
                warning=(
                    f"License is {uri_desc}. "
                    "Treating as personal use in local mode."
                ),
            )
        return AccessDecision(
            allowed=False,
            reason=(
                f"License is {uri_desc}. "
                "Cannot serve content without permissive license in hosted mode."
            ),
        )
