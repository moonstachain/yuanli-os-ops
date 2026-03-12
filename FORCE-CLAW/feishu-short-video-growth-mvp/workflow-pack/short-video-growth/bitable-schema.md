# Bitable Schema: Short-Video Growth

Use this as the v1 schema blueprint for the Feishu operating center.

## Table 1: Topic Candidate

One row per imported or manual topic lead.

Suggested fields:

- `Topic ID`
- `Title`
- `Source`
- `Reference URL`
- `Summary`
- `Topic Tags`
- `Trend Reason`
- `Captured At`
- `Entry Mode`
  - `scheduled`
  - `manual`
- `Curiosity Score`
- `Substance Score`
- `Relevance Score`
- `Final Score`
- `Status`
  - `captured`
  - `ranked`
  - `shortlisted`
  - `selected`
  - `rejected`
  - `archived`
- `Manual Notes`
- `Linked Draft`

Suggested views:

- `待打分`
- `待选题`
- `已选题`
- `归档`

## Table 2: Content Draft

One row per selected topic.

Suggested fields:

- `Draft ID`
- `Topic Candidate`
- `Working Title`
- `Primary Platform Pair`
- `Research Summary`
- `Story Angle`
- `Anti-Consensus Insight`
- `Original Evidence Clues`
- `Hook`
- `Story Arc`
- `Key Beats`
- `Payoff`
- `原力创业收束`
- `Doc URL`
- `Publish Package Status`
- `Status`
  - `researching`
  - `drafting`
  - `ready_for_publish`
  - `published`
  - `review_pending`
  - `reviewed`
  - `evolved`
- `Draft Owner`
- `Draft SLA`
- `Last Nudged At`

Suggested views:

- `研究中`
- `待发布`
- `待复盘`

## Table 3: Performance Review

One row per content item and platform.

Suggested fields:

- `Review ID`
- `Content Draft`
- `Platform`
  - `视频号`
  - `小红书`
- `Published At`
- `Plays`
- `Completion Rate`
- `Engagement Rate`
- `Likes`
- `Comments`
- `Shares`
- `Saves`
- `New Followers`
- `Leads`
- `Qualitative Diagnosis`
- `Repeat`
- `Avoid`
- `Rule Candidate`
- `Import Batch`
- `Import Status`
  - `pending`
  - `imported`
  - `retry_needed`

Suggested views:

- `待导入`
- `待复盘`
- `跨平台对比`

## Table 4: Evolution Rule

One row per approved reusable lesson.

Suggested fields:

- `Rule ID`
- `Source Draft`
- `Source Review`
- `Rule Statement`
- `Rule Type`
  - `topic`
  - `hook`
  - `story`
  - `ending`
  - `platform`
- `Topic Pattern`
- `Story Archetype`
- `Hook Style`
- `Ending Strategy`
- `Evidence Strength`
- `Apply Next Round`
- `Created At`

Suggested views:

- `下轮启用`
- `按故事模式`
- `按平台表现`

## Dashboard Suggestions

Build one comparison dashboard with:

- top 3 shortlisted topics by cycle
- drafted vs published count
- per-platform completion and engagement comparison
- evolution rule count by type
