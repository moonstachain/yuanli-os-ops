# Dify to Feishu Bridge

这份桥接说明用于把现有 `FORCE-CLAW/dify-short-video-content-system` 和新的 Feishu MVP 对齐。

## 对齐原则

- Feishu 管 `运营状态与对象沉淀`
- Dify 管 `AI 生成与推理链`
- 人工保留 `选题确认` 与 `最终发布`

## 对象映射

### Topic Candidate

Feishu 表：`Topic Candidate`

对应 Dify 契约：

- [topic_candidate.schema.json](/Users/liming/AI%20Project/codex-force-claw/FORCE-CLAW/dify-short-video-content-system/contracts/topic_candidate.schema.json)

建议映射：

- `headline` -> `Title`
- `source` -> `Source`
- `story_angle` -> `Summary` 或 `Story Angle`
- `force_claw_relevance_score` -> `Relevance Score`
- `selection_reason` -> `Trend Reason`

### Selected Topic Brief

Feishu 表：`Content Draft` 的选题触发阶段

对应 Dify 契约：

- [selected_topic_brief.schema.json](/Users/liming/AI%20Project/codex-force-claw/FORCE-CLAW/dify-short-video-content-system/contracts/selected_topic_brief.schema.json)

建议映射：

- `core_story` -> `Story Angle`
- `counterintuitive_insight` -> `Anti-Consensus Insight`
- `force_claw_link` -> `原力创业收束`
- `target_platforms` -> `Primary Platform Pair`

### Content Script Package

Feishu 表：`Content Draft` + publish package 产物

对应 Dify 契约：

- [content_script_package.schema.json](/Users/liming/AI%20Project/codex-force-claw/FORCE-CLAW/dify-short-video-content-system/contracts/content_script_package.schema.json)

建议映射：

- `title_options` -> 发布包标题候选
- `opening_hook` -> `Hook`
- `story_arc` -> `Story Arc`
- `key_reveals` -> `Key Beats`
- `final_force_claw_lesson` -> `原力创业收束`
- `xiaohongshu_copy` -> 小红书文案
- `wechat_video_copy` -> 视频号文案

### Feedback Record

Feishu 表：`Performance Review`

对应 Dify 契约：

- [feedback_record.schema.json](/Users/liming/AI%20Project/codex-force-claw/FORCE-CLAW/dify-short-video-content-system/contracts/feedback_record.schema.json)

建议映射：

- `views` -> `Plays`
- `completion_or_watch_quality` -> `Completion Rate` 或质性诊断
- `operator_notes` -> `Qualitative Diagnosis`
- `suggested_next_adjustments` -> `Repeat/Avoid/Rule Candidate`

## 推荐接法

第一阶段：

- Feishu 负责全流程对象与状态
- Dify 只负责生成 `topic candidates` 和 `content script package`

第二阶段：

- Feishu 自建应用 + Python service 作为中枢
- Python service 调 Dify 工作流
- 结果回写到 Feishu
