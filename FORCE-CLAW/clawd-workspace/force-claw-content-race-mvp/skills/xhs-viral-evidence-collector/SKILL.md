---
name: xhs-viral-evidence-collector
description: >
  小红书爆款内容采集与归因分析，用于内容赛马前置层。从小红书公开页采集爆款帖，
  提取传播模式、标签策略和互动数据。当用户说"小红书爆款"、"采集小红书"、
  "内容赛马"、"爆款分析"、"小红书研究"时使用。
  NOT for 公众号写作（用 wechat-article-writer）。
---

# xhs-viral-evidence-collector

只在 `小红书图文` 范围内工作。

## 目标

- 产出可复跑的 `xhs_collection_method_log`
- 产出真实帖子级别的 `xhs_evidence_pack`
- 归纳 `viral_pattern_digest`
- 形成 `claw_topic_bridge`

## 何时使用

- 用户要求“去小红书收集什么火了、为什么火”
- 用户要给 `Coze / Dify / Feishu / n8n` 提供统一爆款证据输入
- 需要判断某个热点是否适合转译成 `CLAW/AI` 图文

## 固定流程

1. 先用 `references/xhs-collection-method.md` 生成本轮 query plan
2. 运行 `scripts/bootstrap_content_race_round.py` 初始化轮次目录
3. 用 `playwright` 在小红书执行公开页 + 已登录辅助采样
4. 每条样本按 `templates/raw_sample.template.json` 结构落盘到 `collector/raw_samples/`
5. 运行 `scripts/normalize_xhs_evidence.py` 生成四个标准件
6. 若 evidence pack 不满足最小样本与覆盖规则，直接判定本轮 `证据不足`

## 关键规则

- 不接受新闻聚合链接替代帖子证据
- 每条样本必须有 `post_url` 或 `post_id`
- 每条样本必须有截图路径或截图缺失说明
- 不得跳过 `negative_notes`
- 对无法核实的数据明确写 `unknown`

## 参考

- `references/xhs-collection-method.md`
- `contracts/xhs_evidence_pack.schema.json`
- `contracts/viral_pattern_digest.schema.json`
- `contracts/claw_topic_bridge.schema.json`
