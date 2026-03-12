# FORCE-CLAW Curated Bundle

This is the curated `FORCE-CLAW` slice carried by `yuanli-os-ops`.

It is not the full source repo. It is the cross-notebook operating subset required to rebuild the current 原力OS stack.

## Included Surfaces

- `YUANLI_OS.md`
  - top-level constitution
- `YUANLI_OS_3X3_EVOLUTION.md`
  - second-order expansion
- `YUANLI_OS_3X3_WECHAT_PLAYBOOK.md`
  - high-frequency content-task implementation
- `YUANLI_OS_3X3_AUDIT.md`
  - global 3 × 3 audit
- `YUANLI_OS_SYSTEM_AUDIT_REPORT.md`
  - 6-axis maturity report
- `BLUEPRINT.md`
  - current runtime blueprint
- `scripts/sync_yuanli_os_audit_to_feishu.py`
  - local canonical audit to Feishu mirror sync
- `references/`
  - Feishu schema and external benchmark seed
- `feishu-short-video-growth-mvp/`
  - first-wave content-growth sample and Feishu delivery slice
- `dify-short-video-content-system/`
  - Dify-side short-video content system
- `clawd-workspace/force-claw-content-race-mvp/`
  - curated content-race workspace slice
- `ops-samples/yuanli-os-feishu-sync/`
  - one successful audit sync sample

## Excluded On Purpose

- broad historical backups
- auth storage
- full runtime noise
- unrelated business plans and old design drafts

## Validation

Run:

```bash
python3 ../scripts/verify_yuanli_os_ops_bundle.py
```
