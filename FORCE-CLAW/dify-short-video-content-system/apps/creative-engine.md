# App B: 创作引擎 Workflow

## 目标

把选中的选题卡转成 `可拍脚本 + 平台文案`。

## 输入

- `selected_topic_brief`
- `content_preference_memory`
- `tone_constraints`
- `target_platforms`

## 输出

- `content_script_package`

## Dify 节点建议

1. `Start`
2. `LLM / 故事核`
   - 写出最值得讲的戏剧冲突、人物张力、事件反差
3. `LLM / 反认知价值`
   - 提炼让人意外但有证据支撑的洞见
4. `LLM / 原力创业映射`
   - 把故事结论自然收束到原力创业
5. `LLM / 脚本整合`
   - 产出开场钩子、故事线、关键揭示、结尾升华
6. `LLM / 平台文案`
   - 产出小红书文案、视频号文案、标题候选
7. `Template / Script Package`
8. `End`

## 关键规则

- 先讲故事，再讲道理
- 必须有“猎奇点”或“反差点”
- 原力创业相关性必须自然，不允许硬贴标签
- 发布文案与脚本共源，不要写成两套完全不同的表达

## 建议局部 Agent Node

仅在“故事素材角度扩展”或“标题变体扩展”时局部使用 `Agent node`。

不要把整个创作引擎做成纯 Agent。

## 验收标准

- 能直接拍
- 不空洞
- 有故事推进
- 有反认知揭示
- 结尾能自然导向原力创业
