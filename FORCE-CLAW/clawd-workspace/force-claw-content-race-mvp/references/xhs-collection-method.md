# 小红书爆款采集方法

## 1. 范围

- 只采 `图文`
- 只采 `公开页 + 已登录辅助`
- 不进创作者后台

## 2. 查询桶

- `OpenAI/模型热点`
- `AI 工作流/工具链`
- `CLAW 邻近表达`

默认首轮关键词：

- `OpenAI`
- `ChatGPT`
- `Agent`
- `工作流`
- `Coze`
- `Dify`
- `飞书自动化`
- `知识库`
- `AI 提效`
- `CLAW`
- `小龙虾 AI`

## 3. 采样纪律

- 每个关键词同时采 `hot` 和 `recent`
- 每个查询至少保留 2 条样本
- 记录看得到的互动字段；看不到写 `unknown`
- 每条样本必须附带截图路径或截图缺失原因

## 4. 最小归因标签

- `hook_type`
- `promise_type`
- `format_type`
- `emotion_or_identity_lever`
- `why_it_may_win`

## 5. 负样本纪律

每轮都要写 `negative_notes`，说明哪些内容虽然热，但不该被 `CLAW` 借鉴，例如：

- 空泛鸡汤
- 纯娱乐八卦
- 无法核实的夸张承诺
- 与 `CLAW/AI` 主轴无关的流量标题
