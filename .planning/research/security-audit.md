# Security Posture Audit

**Audited:** 2026-03-06T02:32:00Z
**Auditor:** Claude Code (automated)
**Scope:** Network bindings (0.0.0.0 and [::] exposure), credential storage, file permissions, SSH configuration, firewall gaps

## Executive Summary

The system has **5 CRITICAL** and **2 HIGH** security findings. The most severe issues are services bound to all network interfaces (0.0.0.0) that should be restricted to localhost or Tailscale: VNC on port 5900, SyncThing GUI on port 8384, Nginx default on port 80, and plaintext credential storage in `.git-credentials`. While Tailscale and fail2ban provide some network-layer protection, the exposure surface is unnecessarily large. SSH configuration is strong (key-only, no root login). Firewall rules (UFW) could not be inspected without sudo -- this is a gap that must be addressed in Phase 3 before any binding changes.

**Finding count:** 5 CRITICAL, 2 HIGH, 1 MEDIUM, 1 LOW = 9 total findings

## Findings

### Finding: VNC Exposed on All Interfaces (Port 5900)

| Property | Value |
|----------|-------|
| Severity | CRITICAL |
| Category | security |
| Current State | VNC listening on 0.0.0.0:5900 (IPv4) and [::]:5900 (IPv6) -- accessible from any network interface. No process name visible without sudo (likely x11vnc, vino, or gnome-remote-desktop). gnome-remote-desktop.service is running. |
| Expected State | VNC should bind to 127.0.0.1 only, accessed via Tailscale SSH tunnel |
| Remediation | Phase 3: SEC-02 -- Rebind VNC to localhost; access via `ssh -L 5900:localhost:5900 dionysus` over Tailscale |
| Verified By | `ss -tlnp \| grep 5900` showing `0.0.0.0:5900` and `[::]:5900` |

**Risk:** VNC is a graphical desktop protocol. If exposed to the LAN or internet (depending on firewall), an attacker could view/control the desktop. VNC authentication varies by implementation; some configurations have weak or no passwords.

### Finding: SyncThing GUI Exposed on All Interfaces (Port 8384)

| Property | Value |
|----------|-------|
| Severity | CRITICAL |
| Category | security |
| Current State | SyncThing web GUI listening on *:8384 (all interfaces, both IPv4 and IPv6). Process: syncthing (pid=1641). Running as systemd service `syncthing@rookslog.service`. |
| Expected State | SyncThing GUI should bind to 127.0.0.1:8384 only |
| Remediation | Phase 3: SEC-05 -- Change SyncThing GUI listen address in config.xml to 127.0.0.1:8384 |
| Verified By | `ss -tlnp` showing `*:8384` with syncthing process |

**Risk:** The SyncThing GUI provides full administrative control over file synchronization. An attacker on the network could modify sync folders, add devices, or access synchronized file metadata. SyncThing has its own authentication but default configurations may be weak.

### Finding: Plaintext .git-credentials with credential.helper=store

| Property | Value |
|----------|-------|
| Severity | CRITICAL |
| Category | security |
| Current State | `git config --global credential.helper` returns `store`. File `~/.git-credentials` exists (69 bytes, created Sep 7 2025, permissions 600). This stores GitHub/Git credentials in plaintext on disk. |
| Expected State | Use `gh auth` token-based authentication (already configured) or `credential.helper=cache` with timeout. Remove plaintext `.git-credentials` file. |
| Remediation | Phase 3: SEC-04 -- Switch to `gh auth` (already working), remove `.git-credentials`, set `credential.helper=` to empty or use credential-cache |
| Verified By | `git config --global credential.helper` returns "store", `ls -la ~/.git-credentials` shows file exists |

**Risk:** If an attacker gains read access to the home directory (e.g., via the exposed VNC or SyncThing), they can read GitHub credentials directly. The 600 permissions mitigate casual access but do not protect against privilege escalation or processes running as the user.

**Note:** Git remotes are already converted to HTTPS with `gh auth` handling push/pull (per MEMORY.md). The `.git-credentials` file may be vestigial from before the `gh auth` migration.

### Finding: Nginx Default Site on All Interfaces (Port 80)

| Property | Value |
|----------|-------|
| Severity | CRITICAL |
| Category | security |
| Current State | Nginx listening on 0.0.0.0:80 (IPv4) and [::]:80 (IPv6). Only the `default` site is enabled in `/etc/nginx/sites-enabled/`. nginx.service is running. |
| Expected State | Either disable nginx entirely (no web serving use case documented) or bind to 127.0.0.1 for reverse proxy use |
| Remediation | Phase 3: SEC-03 -- Disable nginx service or restrict binding; no active use case documented |
| Verified By | `ss -tlnp \| grep ':80'` and `ls /etc/nginx/sites-enabled/` |

**Risk:** The nginx default page reveals server information (version, OS). While low-risk on its own, an unnecessary exposed web server increases the attack surface. If nginx is not actively used for reverse proxying, it should be stopped.

### Finding: PaddleOCR Exposed on All Interfaces (Port 8765)

| Property | Value |
|----------|-------|
| Severity | CRITICAL |
| Category | security |
| Current State | PaddleOCR Docker container publishing port 8765 to 0.0.0.0:8765 (IPv4) and [::]:8765 (IPv6). Docker port mapping bypasses host firewall rules. Container running since Jan 9, 2026 (7 weeks). |
| Expected State | Docker port mapping should restrict to 127.0.0.1:8765:8765 (localhost only) |
| Remediation | Phase 3: SEC-01 -- Recreate container with `-p 127.0.0.1:8765:8765` instead of `-p 8765:8765` |
| Verified By | `docker ps` showing port mapping `0.0.0.0:8765->8765/tcp, [::]:8765->8765/tcp` |

**Risk:** PaddleOCR is an OCR service that processes document images. If accessible from the network, an attacker could use it to process arbitrary documents or potentially exploit vulnerabilities in the OCR engine. Docker port mappings bypass UFW/iptables rules, making this especially concerning.

### Finding: Uvicorn Annotation Tool on All Interfaces (Port 9001)

| Property | Value |
|----------|-------|
| Severity | HIGH |
| Category | security |
| Current State | Uvicorn (PHL410 annotation tool) bound to 0.0.0.0:9001. Spawned from a Claude shell snapshot on Jan 16, 2026. Process pid=2366305. |
| Expected State | Should bind to 127.0.0.1:9001 or be stopped if not in active use |
| Remediation | Phase 3: SEC-01 -- Rebind to localhost or terminate; likely no longer needed |
| Verified By | `ss -tlnp` showing `0.0.0.0:9001` with uvicorn process |

**Risk:** A web application exposed to all interfaces could be probed for vulnerabilities. The annotation tool likely has no authentication.

### Finding: SyncThing Data Port on All Interfaces (Port 22000)

| Property | Value |
|----------|-------|
| Severity | HIGH |
| Category | security |
| Current State | SyncThing data transfer listening on *:22000 (all interfaces). This is the peer-to-peer sync protocol port. |
| Expected State | Port 22000 should ideally be restricted to Tailscale interfaces, but SyncThing requires this for peer discovery. Acceptable if UFW restricts access to known peers. |
| Remediation | Phase 3: SEC-05 -- Verify UFW rules restrict 22000 to Tailscale subnet; SyncThing relay may handle NAT traversal instead |
| Verified By | `ss -tlnp` showing `*:22000` with syncthing process |

**Risk:** Lower than GUI exposure since SyncThing data protocol has its own encryption and device authentication. However, exposure to the broader network is unnecessary when all sync peers are on Tailscale.

### Finding: UFW Firewall Rules Not Inspectable

| Property | Value |
|----------|-------|
| Severity | MEDIUM |
| Category | configuration |
| Current State | UFW (Uncomplicated Firewall) is installed and fail2ban.service is running, but `ufw status` requires sudo and cannot be inspected in this audit. The actual firewall rules are unknown. |
| Expected State | Firewall rules should be documented and verified to restrict 0.0.0.0 bindings |
| Remediation | Phase 3: first action should be `sudo ufw status verbose` before making any binding changes |
| Verified By | `systemctl list-units \| grep fail2ban` confirms fail2ban running; UFW status requires sudo |

**Risk:** Without knowing the firewall state, we cannot assess the true network exposure. It is possible (but unverified) that UFW restricts access to the CRITICAL-severity ports above. Phase 3 MUST inspect firewall rules before assuming worst-case exposure.

### Finding: SSH Configuration is Strong (Positive Finding)

| Property | Value |
|----------|-------|
| Severity | LOW |
| Category | security (positive) |
| Current State | SSH on 0.0.0.0:22 (expected for remote access). PasswordAuthentication=no, PermitRootLogin=no. 3 authorized ed25519 keys. fail2ban running. Key permissions correct (600). No user SSH config file. |
| Expected State | Current state is good. SSH on 0.0.0.0:22 is expected and acceptable for a remote development server. |
| Remediation | None required -- SSH configuration meets security best practices |
| Verified By | `grep PasswordAuthentication /etc/ssh/sshd_config`, `stat -c '%a' ~/.ssh/id_ed25519` |

## Raw Data

### Services Bound to 0.0.0.0 (Exposed to All IPv4 Interfaces)

```
LISTEN 0      32                         0.0.0.0:5900       0.0.0.0:*
LISTEN 0      511                        0.0.0.0:80         0.0.0.0:*
LISTEN 0      4096                       0.0.0.0:22         0.0.0.0:*
LISTEN 0      2048                       0.0.0.0:9001       0.0.0.0:*    users:(("uvicorn",pid=2366305,fd=13))
LISTEN 0      4096                       0.0.0.0:8765       0.0.0.0:*
```

### Services Bound to [::] (Exposed to All IPv6 Interfaces)

```
LISTEN 0      32                            [::]:5900          [::]:*
LISTEN 0      511                           [::]:80            [::]:*
LISTEN 0      4096   [fd7a:115c:a1e0::3101:d42c]:57309         [::]:*
LISTEN 0      4096                         [::1]:631           [::]:*
LISTEN 0      4096                          [::]:8765          [::]:*
LISTEN 0      511                          [::1]:6379          [::]:*
```

### Services Bound to Wildcard (*) -- All Interfaces

```
LISTEN 0      4096                             *:22000            *:*    users:(("syncthing",pid=1641,fd=13))
LISTEN 0      4096                             *:8384             *:*    users:(("syncthing",pid=1641,fd=22))
```

### Binding Classification

| Port | Service | Local Address | Classification | Severity |
|------|---------|---------------|----------------|----------|
| 5900 | VNC | 0.0.0.0 + [::] | EXPOSED (all interfaces) | CRITICAL |
| 8384 | SyncThing GUI | * (all) | EXPOSED (all interfaces) | CRITICAL |
| 80 | Nginx | 0.0.0.0 + [::] | EXPOSED (all interfaces) | CRITICAL |
| 8765 | PaddleOCR | 0.0.0.0 + [::] | EXPOSED (all interfaces, Docker) | CRITICAL |
| 9001 | Uvicorn | 0.0.0.0 | EXPOSED (all interfaces) | HIGH |
| 22000 | SyncThing Data | * (all) | EXPOSED (expected for sync) | HIGH |
| 22 | SSH | 0.0.0.0 | EXPOSED (expected for access) | ACCEPTABLE |
| 34825 | Tailscale | 100.93.212.44 | TAILSCALE ONLY | GOOD |
| 57309 | Tailscale IPv6 | fd7a:... | TAILSCALE ONLY | GOOD |
| 5432 | PostgreSQL | 127.0.0.1 | LOCALHOST ONLY | GOOD |
| 6379 | Redis | 127.0.0.1 + [::1] | LOCALHOST ONLY | GOOD |
| 631 | CUPS | 127.0.0.1 + [::1] | LOCALHOST ONLY | GOOD |
| 9050 | Tor SOCKS | 127.0.0.1 | LOCALHOST ONLY | GOOD |
| 9002 | Python (alt annotation) | 127.0.0.1 | LOCALHOST ONLY | GOOD |
| 53 | systemd-resolved | 127.0.0.53/127.0.0.54 | LOCALHOST ONLY | GOOD |
| 53 | libvirt DNS | 192.168.122.1 | VIRBR0 ONLY | GOOD |
| Various | VS Code/extensions | 127.0.0.1 | LOCALHOST ONLY | GOOD |

### Credential Storage

| File | Permissions | Size | Contents Risk |
|------|-------------|------|---------------|
| ~/.git-credentials | 600 | 69 bytes | CRITICAL: plaintext GitHub credentials |
| ~/.env | 600 | 129 bytes | OK: proper permissions, expected location |
| ~/.ssh/id_ed25519 | 600 | 411 bytes | OK: private key, proper permissions |
| ~/.ssh/id_ed25519_vm | 600 | 399 bytes | OK: VM-specific key, proper permissions |
| ~/.ssh/id_ed25519.pub | 644 | 103 bytes | OK: public key, expected permissions |
| ~/.ssh/id_ed25519_vm.pub | 644 | 94 bytes | OK: public key, expected permissions |
| ~/.ssh/authorized_keys | 600 | -- | OK: 3 ed25519 keys, proper permissions |

**Git credential configuration:**
- `git config --global credential.helper` = `store` (CRITICAL: stores plaintext)
- `gh auth` is also configured and working (per MEMORY.md)
- `.git-credentials` may be vestigial -- test if removing it breaks anything after confirming `gh auth` works

**Other credential files found:**
- `~/miniconda3/ssl/cert.pem` -- standard SSL certificates (not sensitive)
- `~/miniconda3/ssl/cacert.pem` -- CA certificate bundle (not sensitive)
- `~/.env` -- proper location per project conventions

### SSH Configuration

**Server settings (from /etc/ssh/sshd_config):**
- `PermitRootLogin no` -- GOOD
- `PasswordAuthentication no` -- GOOD (key-only)

**Authorized keys (3 entries):**
1. `ssh-ed25519 ...Yjvi logansrooks@gmail.com` -- primary key
2. `ssh-ed25519 ...1XG8 logansrooks@gmail.com` -- secondary key
3. `ssh-ed25519 ...fA86 logan-borrowed-laptop` -- borrowed laptop key

**User SSH config:** No `~/.ssh/config` file exists.

**SSH key types:** All ed25519 (modern, strong). No legacy RSA or DSA keys.

### Loginctl Linger

- `Linger=no` -- user services will stop when user logs out
- **Impact:** Phase 4 may need linger enabled for persistent user systemd services (DEV-04)

### Nginx Configuration

- Only `default` site enabled in `/etc/nginx/sites-enabled/`
- No custom configurations or reverse proxy setups
- Service is running but appears to serve no purpose

## Verification Against Research

| Claim (from research/CLAUDE.md) | Verified? | Actual State | Notes |
|---------------------------------|-----------|--------------|-------|
| VNC on 0.0.0.0:5900 | YES | Confirmed on both IPv4 and IPv6 | CRITICAL -- matches research finding |
| SyncThing GUI on 0.0.0.0:8384 | YES | Confirmed on all interfaces (*:8384) | CRITICAL -- matches research finding |
| Plaintext .git-credentials | YES | credential.helper=store, file exists with 600 perms | CRITICAL -- matches research. Note: gh auth may make this vestigial |
| Nginx default on 0.0.0.0:80 | YES | Confirmed on both IPv4 and IPv6 | CRITICAL -- matches research finding |
| PaddleOCR on 0.0.0.0:8765 | YES | Confirmed on both IPv4 ([::]:8765) via Docker | HIGH (upgraded to CRITICAL per combined IPv4+IPv6 exposure) -- matches research |
| PostgreSQL on localhost only | YES | 127.0.0.1:5432 | GOOD -- matches CLAUDE.md |
| Redis on localhost only | YES | 127.0.0.1:6379 and [::1]:6379 | GOOD -- matches CLAUDE.md |
| fail2ban running | YES | fail2ban.service active | GOOD -- security positive |
| UFW status requires sudo | YES | Cannot inspect without sudo | Gap acknowledged -- must verify in Phase 3 |
| SSH key-only auth | YES | PasswordAuthentication=no, PermitRootLogin=no | GOOD -- strong configuration |

**Additional finding not in research:** Uvicorn on 0.0.0.0:9001 -- not documented as a security concern in prior research but represents an exposed web application. CLAUDE.md lists it as "Running" without noting the binding.

## Phase 3 Remediation Mapping

| Finding | Severity | Phase 3 Requirement | Priority |
|---------|----------|---------------------|----------|
| VNC on 0.0.0.0:5900 | CRITICAL | SEC-02 | 1 (highest) |
| SyncThing GUI on *:8384 | CRITICAL | SEC-05 | 2 |
| Plaintext .git-credentials | CRITICAL | SEC-04 | 3 |
| Nginx default on 0.0.0.0:80 | CRITICAL | SEC-03 | 4 |
| PaddleOCR on 0.0.0.0:8765 + [::]:8765 | CRITICAL | SEC-01 | 5 |
| Uvicorn on 0.0.0.0:9001 | HIGH | SEC-01 | 6 |
| SyncThing data on *:22000 | HIGH | SEC-05 | 7 |
| UFW rules unknown | MEDIUM | First action in Phase 3 | 0 (prerequisite) |

**Phase 3 dependency note:** UFW inspection (requires sudo) MUST happen before any binding changes. If UFW is already blocking external access to these ports, the risk is lower than documented here. But the principle of defense-in-depth means services should still bind to localhost regardless of firewall state.

---

*Audit complete: 2026-03-06T02:32Z*
*No system changes made -- document only*
