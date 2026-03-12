# App D: 主编排 Workflow

## 目标

串联 `选题雷达 -> 创作引擎 -> 闭环进化`，维护每轮内容生命周期状态。

## 输入

- `run_id`
- `operator_name`
- `time_window`
- `seed_keywords`
- `blocked_topics`
- `content_preference_memory`
- `failure_pattern_memory`

## 输出

- `workflow_state`
- `selected_topic_brief`
- `content_script_package`
- `next_round_updates`

## 生命周期状态

- `radar-generated`
- `topic-selected`
- `script-generated`
- `published-manually`
- `feedback-recorded`
- `evolved`

## 编排规则

1. 先调用 `选题雷达`
2. 等待人工选题
3. 把选中的 brief 传给 `创作引擎`
4. 等待人工发布
5. 接收反馈数据
6. 调用 `闭环进化`
7. 更新下一轮偏好

## 第一版不要做的事

- 自动发帖
- 多账号矩阵调度
- 自动拉平台数据
- 自动 AB 投放

## 运行面板建议

内部 Web App 展示：

- 当前 run 状态
- 3 个候选选题卡
- 已选选题
- 当前脚本包
- 发布后反馈录入入口
- 下一轮偏好更新摘要
