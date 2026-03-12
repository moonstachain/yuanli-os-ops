# Recovery Commands

## 1. 替换飞书知识源

仅替换 URL：

```bash
python3 FORCE-CLAW/clawd-workspace/force-claw-content-race-mvp/scripts/apply_knowledge_source.py \
  --round-dir "FORCE-CLAW/clawd-workspace/force-claw-content-race-mvp/runtime-artifacts/runs/real-round-20260310-01" \
  --source-url "新的飞书链接"
```

若已拿到可读的 Feishu 提取结果：

```bash
python3 FORCE-CLAW/clawd-workspace/force-claw-content-race-mvp/scripts/apply_knowledge_source.py \
  --round-dir "FORCE-CLAW/clawd-workspace/force-claw-content-race-mvp/runtime-artifacts/runs/real-round-20260310-01" \
  --source-url "新的飞书链接" \
  --source-json "output/feishu-reader/source.json"
```

说明：`apply_knowledge_source.py` 现在会自动刷新 `round_status` 和 AI大管家督办产物。

## 2. 重新尝试小红书采样

网络环境恢复后，先最小复测 `OpenAI`，再扩到完整 query plan。

若共享证据四件套已生成：

```bash
python3 FORCE-CLAW/clawd-workspace/force-claw-content-race-mvp/scripts/update_round_status.py \
  --round-dir "FORCE-CLAW/clawd-workspace/force-claw-content-race-mvp/runtime-artifacts/runs/real-round-20260310-01" \
  --stage xhs_collection \
  --status ready \
  --reason xhs_evidence_pack_generated \
  --artifact "FORCE-CLAW/clawd-workspace/force-claw-content-race-mvp/runtime-artifacts/runs/real-round-20260310-01/collector/xhs_evidence_pack.json"
```

说明：`update_round_status.py` 现在会自动刷新 AI大管家督办产物。

## 3. 四方交卷后打分

```bash
python3 FORCE-CLAW/clawd-workspace/force-claw-content-race-mvp/scripts/score_content_race_round.py \
  --round-dir "FORCE-CLAW/clawd-workspace/force-claw-content-race-mvp/runtime-artifacts/runs/real-round-20260310-01"
```

打分后再刷新一次督办状态，确保简报与真实进度一致。

说明：`score_content_race_round.py` 现在会校验前置 gate，并在成功后自动更新 `workflow_submissions`、`weekly_scorecard` 和 AI大管家督办状态。
