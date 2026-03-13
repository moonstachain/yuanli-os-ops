# Connection Order

1. On the new Mac, enable `Remote Login` and `Screen Sharing`.
2. Confirm the new Mac is reachable over the LAN by hostname or static IP.
3. Clone `os-yuanli`, `ai-da-guan-jia`, `yuanli-os-ops`, and `yuanli-os-skills-pack`.
4. Restore `ai-da-guan-jia` into `$CODEX_HOME/skills/ai-da-guan-jia`.
5. Restore `os-yuanli` into `$CODEX_HOME/skills/os-yuanli`.
6. Run `python3 ../yuanli-os-skills-pack/scripts/install_skills_pack.py --codex-home "${CODEX_HOME:-$HOME/.codex}"`.
7. Restore the public first-wave skills from `moonstachain/feishu-reader`, `moonstachain/openai-docs`, `moonstachain/pdf`, `moonstachain/spreadsheet`, and `moonstachain/wechat-article-writer`.
8. Confirm GitHub auth.
9. Confirm Feishu internal-app credentials in `~/.openclaw/openclaw.json`.
10. Run the remote, bundle, audit, and content checks from `HEALTHCHECK_CONTRACT.md`.
11. Run one content smoke task.
12. Only after the local loop is stable, enable repeated Feishu audit sync and recursive review cadence.

## Default External Responsibilities

- GitHub
  - versioning
  - distribution
  - repository topology
- Feishu
  - audit operations
  - benchmark visibility
  - recursion queue
- local machine
  - canonical truth
  - auth state
  - real execution traces
