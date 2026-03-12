# App C: 闭环进化 Workflow

## 目标

把发布后的数据和主观反馈转成 `结构化复盘 + 下一轮偏好更新`。

## 输入

- `feedback_record`
- `content_script_package`
- `selected_topic_brief`
- `content_preference_memory`
- `failure_pattern_memory`

## 输出

- `feedback_analysis`
- `next_round_updates`

## Dify 节点建议

1. `Start`
2. `Code / Normalize Metrics`
   - 统一不同平台字段
3. `LLM / Outcome Diagnosis`
   - 判断表现强弱与主要原因
4. `LLM / Failure Decomposition`
   - 区分：
     - 选题问题
     - 内容问题
     - 平台匹配问题
     - 标题/开场问题
     - 原力创业关联过弱问题
5. `LLM / Reusable Insight`
   - 提炼可复用规律
6. `Template / Memory Updates`
   - 输出下一轮偏好变量
7. `End`

## 关键规则

- 不要只给“继续优化”这种空建议
- 必须指出具体该改哪里
- 复盘结果要能回流到选题雷达

## 第一版输入方式

- 表单录入
- 粘贴 JSON
- 手动摘要评论反馈
