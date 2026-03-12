# Observed Feishu State on 2026-03-10

这份记录来自浏览器自动化在 2026-03-10 的现场勘测与后续实际落地。

## 页面与对象

- Wiki token: `UCFJwrGYJiOk52k1NYFcPkIon9b`
- Base token: `ZqsUbVegpaskp5sYcQTcCXOvn4c`
- Base name: `新媒体-安克妙记多维表`

## 编辑权限与账号

- 已使用可编辑账号登录
- 当前可见编辑身份：`Ray`
- tenant: `北京奥德修斯教育科技有限公司`

## 发现的短视频相关表

- `闭环总览`
  - table id: `tbl2L1C6R6ah52V3`
  - view id: `vew6HBGjjB`
  - current meaningful records: `1`
- `选题候选`
  - table id: `tbl1ud63yTYJG33C`
  - view id: `vew58C2kIJ`
  - current meaningful records: `3`
- `脚本包`
  - table id: `tbl11Caf7HtwylDF`
  - view id: `vew4mZjfd2`
  - current meaningful records: `1`
- `反馈复盘`
  - table id: `tbl3OJJZ8tvHsxiq`
  - view id: `vew40DxjiT`
  - current meaningful records: `1`
- `进化规则库`
  - table id: `tblSEtl6NUNMMYuc`
  - view id: `vewJ9OmtDm`
  - current meaningful records: `1`

## 当天实际完成的飞书侧动作

- 没有新建独立 Base，改为在现有 `新媒体-安克妙记多维表` 中补齐短视频 MVP
- 新建视图：
  - `选题候选` -> `待选题 Top 3`
  - `脚本包` -> `研究中`
  - `脚本包` -> `待发布`
  - `反馈复盘` -> `待复盘`
  - `反馈复盘` -> `双平台对比`
- 新建表：
  - `进化规则库`
- 新建文档：
  - `短视频研究脚本模板`
- 文档模板固定段落已写入：
  - `故事角度`
  - `有料/反认知`
  - `人物/事件/证据线索`
  - `脚本结构`
  - `原力创业收束`
  - `发布备注`
  - `复盘结论`

## 当天确认的样例闭环

- `选题候选`
  - 已确认 3 条可用候选题样例，使用同一 `run_id`: `demo-20260310-001`
- `脚本包`
  - 已确认 1 条非空脚本包样例，包含 3 个标题候选、Hook、故事弧线、平台文案
- `反馈复盘`
  - 已确认 1 条非空复盘样例，平台为 `小红书`
  - 包含播放、点赞、评论、收藏、诊断、下轮迭代建议
- `进化规则库`
  - 已补入 1 条规则样例，来源为 `demo-20260310-001 / 小红书复盘`
- `闭环总览`
  - 已补入 1 条总览样例，状态走到 `ready_for_publish -> published -> reviewed -> evolved`

## 其他仍在同一 base 中的对象

- `安克妙记`
- `得到笔记`
- `仪表盘`
- `公众号AI成文`
- `FLOMO笔记`
- `量化因子`
- `因子详情宽表`
- `知识库演绎`

## 结论

- 这套短视频 MVP 已经不是只读观察，而是完成了最小闭环补齐
- 当前最佳策略不是迁移，而是继续沿现有 base 演进
- 下一阶段优先动作应是：
  - 为 `脚本包` 增加显式 `Doc URL` 或 `Doc Token` 字段
  - 为视图补齐筛选/排序规则，而不是只创建名字
  - 接入 Feishu 自建应用凭据，启用外部 connector
