# Health Check

## Level 1: Skill Surface

```bash
python3 "$CODEX_HOME/skills/ai-da-guan-jia/scripts/ai_da_guan_jia.py" inventory-skills
python3 "$CODEX_HOME/skills/os-yuanli/scripts/doctor.py"
```

Pass condition:

- `inventory-skills` completes
- `os-yuanli doctor.py` returns `OK`

## Level 2: Bundle Surface

```bash
python3 scripts/verify_yuanli_os_ops_bundle.py
```

Pass condition:

- required docs, scripts, schemas, and curated sample surfaces exist

## Level 3: Audit Surface

```bash
python3 FORCE-CLAW/scripts/sync_yuanli_os_audit_to_feishu.py --dry-run --sync-scope internal
```

Pass condition:

- the audit bundle builds locally
- no absolute source-machine skill path is required
- `dry-run` completes as a local preview even before remote Feishu apply is enabled

## Level 4: Content Surface

Run one minimum content task through:

`AI大管家 -> OS-原力 -> wechat-topic-outline-planner -> wechat-draft-writer -> wechat-title-generator`

Pass condition:

- the run produces a brief
- the strategy layer is stated
- the execution route is explicit
- a real artifact exists
- one `Evolution Note` is left
