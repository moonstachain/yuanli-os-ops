# Real Round Recovery

当真实 round 卡在 gate 时，按以下顺序恢复：

## 1. 飞书知识源

先替换知识源，再重建 `knowledge_digest`。

仅替换 URL：

```bash
python3 scripts/apply_knowledge_source.py \
  --round-dir runtime-artifacts/runs/<round-id> \
  --source-url 'https://example.feishu.cn/wiki/...'
```

从新的 Feishu 提取结果重建：

```bash
python3 scripts/apply_knowledge_source.py \
  --round-dir runtime-artifacts/runs/<round-id> \
  --source-url 'https://example.feishu.cn/wiki/...' \
  --source-json output/feishu-reader/source.json
```

要求：

- `source-json.status == ok`
- 文本长度足够支撑 `brand_truths` 和 `principle_cards`
- 脚本会自动刷新 `round_status.json` 和 AI大管家督办产物

## 2. 小红书采样

知识源 ready 后，再切换到可靠网络环境重试小红书采样。

若采样仍被拦截，可先记录 gate，再停止进入 submission：

```bash
python3 scripts/update_round_status.py \
  --round-dir runtime-artifacts/runs/<round-id> \
  --stage xhs_collection \
  --status blocked \
  --reason xiaohongshu_ip_risk_gate
```

若采样成功并已生成共享证据四件套：

```bash
python3 scripts/update_round_status.py \
  --round-dir runtime-artifacts/runs/<round-id> \
  --stage xhs_collection \
  --status ready \
  --reason xhs_evidence_pack_generated \
  --artifact runtime-artifacts/runs/<round-id>/collector/xhs_evidence_pack.json
```

说明：`update_round_status.py` 会自动刷新 AI大管家督办产物。

## 3. 四方交卷与评分

只有 `knowledge_digest` 与 `xhs_collection` 都是 `ready` 时，才允许：

- 生成四方真实 submission
- 运行 `score_content_race_round.py`
- 更新 `workflow_submissions` 与 `weekly_scorecard`
- `score_content_race_round.py` 会先检查前置 gate，再自动更新 `round_status` 与 AI大管家督办产物
