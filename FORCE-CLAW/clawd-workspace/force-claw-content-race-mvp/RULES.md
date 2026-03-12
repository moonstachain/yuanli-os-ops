# Rules

## 采集规则

- 每个关键词必须同时采 `热门` 与 `新近`
- 样本必须来自真实小红书帖子
- 样本去重优先 `post_url/post_id`
- 单一作者样本占比封顶 `20%`
- 单一关键词样本占比封顶 `25%`
- 互动数据看得到就记，看不到记 `unknown`

## 归因规则

- 每条样本至少标：
  - `hook_type`
  - `promise_type`
  - `format_type`
  - `emotion_or_identity_lever`
  - `why_it_may_win`
- 每轮必须写 `negative_notes`
- 必须明确哪些模式不适合 `CLAW`

## 赛马规则

- 四方必须吃同一份 `knowledge_digest + xhs_evidence_pack + viral_pattern_digest + claw_topic_bridge`
- 输出接口固定
- 评分口径固定
- 训练任务最多每方 2 个
- 所有 submission 都必须声明 `platform_fit`

## 红线

- 没有真实小红书证据却宣称“这是爆款方向”
- 把外部新闻热度伪装成小红书热度
- 只模仿标题，不解释为什么火
- 选题脱离 `CLAW/AI` 主轴
