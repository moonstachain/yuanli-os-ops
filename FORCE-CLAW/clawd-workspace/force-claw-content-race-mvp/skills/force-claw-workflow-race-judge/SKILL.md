---
name: force-claw-workflow-race-judge
description: 用于在同一份 `knowledge_digest + xhs_evidence_pack + viral_pattern_digest + claw_topic_bridge` 输入下，对 Coze、Dify、Feishu、n8n 四个 workflow surface 的内容方案进行统一评分、红线检查、排名和训练任务下发。
---

# force-claw-workflow-race-judge

## 目标

- 保证四方比较公平
- 优先识别伪爆款判断和证据使用错误
- 用最少主观漂移给出 `weekly_scorecard`

## 输入

- `knowledge_digest`
- `xhs_evidence_pack`
- `viral_pattern_digest`
- `claw_topic_bridge`
- 四份 `workflow_race_submission`

## 输出

- `weekly_scorecard`
- `training_backlog`
- `selection_outlook`

## 固定流程

1. 先检查共享证据四件套是否齐全
2. 再逐份检查四个 workflow submission 是否符合契约
3. 使用 `references/race-rubric.md` 和 `scripts/score_content_race_round.py`
4. 若触发红线，本题封顶 `50`
5. 每方最多下发 `2` 个训练任务

## 评分纪律

- 先看是否正确使用证据，再看文案表现
- 没有 evidence refs 的理由，不算有效理由
- `CLAW` 主轴偏离是高严重度错误
- `n8n` 允许诚实声明平台边界，但不能靠“拒绝承载”自动拿高分

## 参考

- `references/race-rubric.md`
- `contracts/workflow_race_submission.schema.json`
- `contracts/weekly_scorecard.schema.json`
