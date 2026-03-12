# Connection Order

1. Clone `os-yuanli`, `ai-da-guan-jia`, and `yuanli-os-ops`.
2. Restore `ai-da-guan-jia` into `$CODEX_HOME/skills/ai-da-guan-jia`.
3. Restore `os-yuanli` into `$CODEX_HOME/skills/os-yuanli`.
4. Restore the first-wave domain skills for `内容与增长`.
5. Confirm GitHub auth.
6. Confirm Feishu internal-app credentials in `~/.openclaw/openclaw.json`.
7. Run the internal audit dry-run.
8. Run one content smoke task.
9. Only after the local loop is stable, enable repeated Feishu audit sync and recursive review cadence.

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
