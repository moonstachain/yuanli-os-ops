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
- `moonstachain/yuanli-os-skills-pack`
  - private first-wave skill bundle for unpublished method organs, content-growth skills, and bridge skills

## Clone Targets

Default local layout:

```text
~/workspace/yuanli-stack/
├── os-yuanli/
├── ai-da-guan-jia/
├── yuanli-os-ops/
└── yuanli-os-skills-pack/
```

## Bootstrap Phases

### Phase 1: System Surface

- complete macOS first-boot setup
- connect to the same LAN as the source machine
- enable `Remote Login`
- enable `Screen Sharing` or `Remote Management`
- create or import the SSH key that the source machine will use

### Phase 2: Code And Runtime Surface

Clone all four repositories, then restore the private-bundle skills:

```bash
python3 ../yuanli-os-skills-pack/scripts/install_skills_pack.py --codex-home "${CODEX_HOME:-$HOME/.codex}"
```

Then restore the public skills listed in [SKILLS_MANIFEST.md](SKILLS_MANIFEST.md).

### Phase 3: Account And Collaboration Surface

- log in locally to GitHub, Feishu, OpenClaw, and any browser-based auth surfaces
- import the required environment variables
- confirm the Feishu audit base link can be opened by the target account

### Phase 4: Health Check Surface

Run the checks in [HEALTHCHECK_CONTRACT.md](HEALTHCHECK_CONTRACT.md) in order.

### Phase 5: Cutover Surface

- start with `内容与增长` on the new machine
- keep the old machine as rollback and training ground for `1-2` weeks
- only shift repeated Feishu recursion and high-frequency production tasks after the health checks stay green

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
ssh <target-user>@<target-host> "echo remote-ready && sw_vers && uname -m"
python3 ../yuanli-os-skills-pack/scripts/verify_yuanli_os_skills_pack.py
python3 "$CODEX_HOME/skills/ai-da-guan-jia/scripts/ai_da_guan_jia.py" inventory-skills
python3 "$CODEX_HOME/skills/os-yuanli/scripts/doctor.py"
python3 scripts/verify_yuanli_os_ops_bundle.py
python3 FORCE-CLAW/scripts/sync_yuanli_os_audit_to_feishu.py --dry-run --sync-scope internal
```

Then run one content-chain smoke task through `AI大管家 -> OS-原力`.
