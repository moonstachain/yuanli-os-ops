# Remote Control Runbook

## Default Architecture

- `主通道`
  - `SSH`
- `辅通道`
  - `Screen Sharing` or `Remote Management`
- `后备通道`
  - physical local login

Do not use full-disk migration as the primary rebuild path.

## First-Boot Setup On The New Mac

1. Finish macOS setup, Apple ID, and system update locally.
2. Open `System Settings -> General -> Sharing`.
3. Enable:
   - `Remote Login`
   - `Screen Sharing` or `Remote Management`
4. Restrict access to the intended admin user.
5. Confirm the machine keeps a stable LAN hostname or reserve a static DHCP lease.

## SSH Bring-Up

From the source machine:

```bash
ssh-copy-id <target-user>@<target-host>
ssh <target-user>@<target-host> "echo remote-ready && sw_vers && uname -m"
```

Daily rule:

- use `SSH` for install, clone, verify, sync, and runtime operations
- use `Screen Sharing` only for GUI auth, OAuth, browser-only setup, or system-permission prompts

## When To Use Screen Sharing

- first login to GitHub, Feishu, or OpenClaw in a browser
- macOS permission prompts
- browser-extension or app-based auth that cannot be scripted safely

## Non-Goals

- do not mirror the entire old machine
- do not copy browser profiles or auth storage
- do not treat screen sharing as the main execution surface
