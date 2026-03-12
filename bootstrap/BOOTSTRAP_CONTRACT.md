# Bootstrap Contract

## Goal

Rebuild a usable `OS-原力` operating stack on another notebook without copying the entire source machine state.

## GitHub Repositories

- `moonstachain/os-yuanli`
  - public method kernel
- `moonstachain/ai-da-guan-jia`
  - default outer governor source; if your target machine already has another canonical source, keep that source and only align behavior
- `moonstachain/yuanli-os-ops`
  - private operating-layer bundle

## Clone Targets

Default local layout:

```text
~/workspace/yuanli-stack/
├── os-yuanli/
├── ai-da-guan-jia/
└── yuanli-os-ops/
```

## Required Skill Installs

Install or restore these into `$CODEX_HOME/skills` in this order:

1. `ai-da-guan-jia`
2. `os-yuanli`
3. `wechat-style-profiler`
4. `wechat-topic-outline-planner`
5. `wechat-draft-writer`
6. `wechat-title-generator`
7. `wechat-article-writer`
8. `feishu-reader`
9. `openai-docs`
10. `pdf`
11. `spreadsheet`

## Required Runtime Surfaces

- GitHub auth via `gh auth login` or a valid `GITHUB_TOKEN`
- Feishu internal app credentials in `~/.openclaw/openclaw.json`
- target Feishu base link for 原力OS审计
- Codex runtime with a valid `$CODEX_HOME`

## Minimum Environment Variables

- `CODEX_HOME`
  - optional if using the default `~/.codex`
- `GITHUB_TOKEN`
  - optional fallback when `gh auth` is not used
- `FEISHU_BITABLE_BRIDGE_BASE_TOKEN`
  - optional override when the Feishu link cannot be resolved automatically
- `AI_DA_GUAN_JIA_FEISHU_BASE_TOKEN`
  - optional fallback alias for the same base token
- `YUANLI_OS_FEISHU_LINK`
  - optional override for the default audit base link
- `YUANLI_OS_FEISHU_ACCOUNT_ID`
  - optional override for the default Feishu account id

## Fixed Feishu Landing Surface

- default audit base link:
  - `https://h52xu4gwob.feishu.cn/wiki/DdNXw06poicDHHkSKIdcRrYDnod?from=from_copylink`
- default bridge path inside this repository:
  - `tools/feishu-bitable-bridge/scripts/feishu_bitable_bridge.py`

## First Health Checks

Run in this order after bootstrap:

```bash
python3 "$CODEX_HOME/skills/ai-da-guan-jia/scripts/ai_da_guan_jia.py" inventory-skills
python3 "$CODEX_HOME/skills/os-yuanli/scripts/doctor.py"
python3 scripts/verify_yuanli_os_ops_bundle.py
python3 FORCE-CLAW/scripts/sync_yuanli_os_audit_to_feishu.py --dry-run --sync-scope internal
```

Then run one content-chain smoke task through `AI大管家 -> OS-原力`.
