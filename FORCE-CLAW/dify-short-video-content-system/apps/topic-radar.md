# App A: 选题雷达 Workflow

## 目标

从 `X + 海外 AI 媒体` 自动收集 AI 热点，聚合人物、事件、争议点，输出 `3 个候选选题卡`。

## 输入

- `time_window`
- `seed_keywords`
- `blocked_topics`
- `content_preference_memory`
- `failure_pattern_memory`
- `source_payloads`

## 输出

- `topic_candidates[]`
- `radar_summary`

## Dify 节点建议

1. `Start`
   - 接收时间窗口、主题偏好、禁区、来源载荷
2. `HTTP / Source Intake`
   - 从聚合接口接收热点条目
   - 第一版可由外部轻量抓取服务统一提供 JSON
3. `Code / Normalize`
   - 统一字段
   - 去除广告、重复转载、低信号噪声
4. `LLM / Story Angle Extractor`
   - 提炼每条热点可讲的故事角度
5. `LLM / Counterintuitive Signal`
   - 判断是否有反认知或非直觉价值
6. `LLM / Force Claw Relevance`
   - 判断与原力创业的相关性
7. `Code / Rank Candidates`
   - 综合排序
   - 公式：`故事张力 + 反认知价值 + 原力创业相关性`
8. `Template / Top 3 Output`
   - 只输出 3 个候选卡
9. `End`

## 关键规则

- 热度不是唯一标准
- 无故事核的热点直接降权
- 只输出 3 个候选，禁止泛泛铺满

## 人工节点

- 你从 3 个候选里选 1 个进入创作

## 失败模式

- 热点很热但没有故事张力
- 故事猎奇但和原力创业无关
- 论点有料但不适合短视频表达
