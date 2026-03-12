# Workflow Brief: Short-Video Growth

Use this template for a solo short-video growth workflow in Feishu.

## Human Summary

- `workflow_template`: `short-video-growth`
- `workflow_name`: `短视频增长闭环`
- `project_name`: `feishu-short-video-growth`
- `business_goal`: `把选题、研究、脚本、发布复盘和下一轮优化做成飞书里的可追踪闭环。`
- `initiator_role`: `创始人/主理人`
- `approver_roles`: []
- `core_object`: `Bitable row + linked Doc`
- `state_model`:
  - `captured`
  - `ranked`
  - `shortlisted`
  - `selected`
  - `researching`
  - `drafting`
  - `ready_for_publish`
  - `published`
  - `review_pending`
  - `reviewed`
  - `evolved`
- `notification_nodes`:
  - `shortlist_ready`
  - `selected_topic_created_draft`
  - `draft_stalled`
  - `publish_package_ready`
  - `review_overdue`
  - `evolution_rule_added`
- `cross_system`: true
- `completion_evidence`:
  - `Feishu shows exactly 3 shortlisted topic candidates`
  - `A selected topic creates one linked research-plus-script Doc`
  - `A publish package exists for 视频号 and 小红书`
  - `Imported metrics appear in Performance Review`
  - `A comparison board can compare topic performance`
  - `At least one evolution rule is written back`
- `topic_ingest_mode`: `scheduled-ai-plus-manual`
- `topic_sources`:
  - `ai-hot-topic-source`
  - `manual-supplement`
- `platforms`:
  - `视频号`
  - `小红书`
- `creation_artifact`: `research-plus-script`
- `publish_mode`: `semi-automatic-human-confirmed`
- `analytics_mode`: `semi-automatic-import`
- `metrics_focus`:
  - `completion_rate`
  - `engagement_rate`
- `notes`: `首版按单人运营，不引入审批对象和任务对象。`

## Machine Block

```json
{
  "workflow_template": "short-video-growth",
  "workflow_name": "短视频增长闭环",
  "project_name": "feishu-short-video-growth",
  "business_goal": "把选题、研究、脚本、发布复盘和下一轮优化做成飞书里的可追踪闭环。",
  "initiator_role": "创始人/主理人",
  "approver_roles": [],
  "core_object": "Bitable row + linked Doc",
  "state_model": [
    "captured",
    "ranked",
    "shortlisted",
    "selected",
    "researching",
    "drafting",
    "ready_for_publish",
    "published",
    "review_pending",
    "reviewed",
    "evolved"
  ],
  "notification_nodes": [
    "shortlist_ready",
    "selected_topic_created_draft",
    "draft_stalled",
    "publish_package_ready",
    "review_overdue",
    "evolution_rule_added"
  ],
  "cross_system": true,
  "completion_evidence": [
    "Feishu shows exactly 3 shortlisted topic candidates",
    "A selected topic creates one linked research-plus-script Doc",
    "A publish package exists for 视频号 and 小红书",
    "Imported metrics appear in Performance Review",
    "A comparison board can compare topic performance",
    "At least one evolution rule is written back"
  ],
  "topic_ingest_mode": "scheduled-ai-plus-manual",
  "topic_sources": [
    "ai-hot-topic-source",
    "manual-supplement"
  ],
  "platforms": [
    "视频号",
    "小红书"
  ],
  "creation_artifact": "research-plus-script",
  "publish_mode": "semi-automatic-human-confirmed",
  "analytics_mode": "semi-automatic-import",
  "metrics_focus": [
    "completion_rate",
    "engagement_rate"
  ],
  "deployment_mode": "python-service",
  "notes": "首版按单人运营，不引入审批对象和任务对象。"
}
```
