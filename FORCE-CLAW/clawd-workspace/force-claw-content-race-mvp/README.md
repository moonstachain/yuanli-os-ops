# FORCE-CLAW Content Race MVP Workspace

这是 FORCE-CLAW 面向 `CLAW/AI` 内容赛马的首版参考工作区。

它负责两件事：

- 把 `小红书爆款采集与归因` 固化成共享前置 skill
- 把 `Coze / Dify / Feishu / n8n` 四套 workflow surface 拉到同一证据输入下做赛马

## 当前目标

- 固定飞书知识源：`https://h52xu4gwob.feishu.cn/wiki/UCFJwrGYJiOk52k1NYFcPkIon9b`
- 固定主赛道：`小红书图文`
- 固定主题桶：`OpenAI/模型热点`、`AI 工作流/工具链`、`CLAW 邻近表达`
- 固定赛制：先共享采集，再统一评分，再下发训练任务

## 目录

- `skills/ai-ling-shou-core`
  - 根层宪法，负责进化、治理、验真和人类友好
- `skills/xhs-viral-evidence-collector`
  - 小红书爆款采集与归因共享 skill
- `skills/force-claw-workflow-race-judge`
  - 四个 workflow skill 的统一评测与训练 skill
- `contracts/`
  - 证据包、桥接包、赛马输出、周评分卡契约
- `references/`
  - 采样方法、评分口径、知识源说明
- `templates/`
  - 轮次初始化模板
- `examples/`
  - 本地回归样例
- `scripts/`
  - round bootstrap、证据归一化、评分、本地校验

## 运行原则

- 没有真实小红书帖子证据，不得宣称“爆款方向成立”
- 产物存在不等于目标达成，必须同时检查 `artifact/state` 与 `goal fit`
- 前置采集 skill 是共享基础设施，不参与冠军竞争
- 最终只留一个主 workflow surface

## 本地校验

```bash
python3 FORCE-CLAW/clawd-workspace/force-claw-content-race-mvp/scripts/validate_content_race_workspace.py
```
