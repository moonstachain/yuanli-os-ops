# yuanli-os-ops

`yuanli-os-ops` is the private operating-layer repository for `OS-原力`.

It is not the public method kernel. It is the portable runtime bundle for rebuilding the system on another machine.

## Topology

- `公开方法核`
  - `os-yuanli`
  - `ai-da-guan-jia`
- `私有运行层`
  - this repository
- `目标机本地态`
  - auth, browser state, caches, environment variables, and local canonical task traces

## What This Repository Carries

- `FORCE-CLAW/`
  - the curated 原力OS docs, blueprint, Feishu audit sync script, schemas, and high-evidence content-growth samples
- `tools/feishu-bitable-bridge/`
  - the minimal bridge needed by the Feishu audit sync stack
- `bootstrap/`
  - target-machine bootstrap contract, environment checklist, connection order, collaboration protocol, and health checks
- `scripts/`
  - repository-level bundle verification

## What This Repository Does Not Carry

- `~/.codex` as a whole
- browser profiles or login cookies
- temporary runtime noise without a stable contract
- unverified experiments and backup leftovers

## Intended Bring-Up Order

1. restore `AI大管家`
2. restore `OS-原力`
3. restore the `内容与增长` chain
4. restore the `研究与审计` chain
5. restore the Feishu audit landing path

Read [bootstrap/BOOTSTRAP_CONTRACT.md](bootstrap/BOOTSTRAP_CONTRACT.md) first.
