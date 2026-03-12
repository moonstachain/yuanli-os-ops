# Feishu Build Runbook

这份手册对应 `短视频增长MVP` 的飞书侧落地动作。

## 目标

在 `原力战略` 空间中，新建一个独立 Base：

- 名称：`短视频增长MVP`

并完成：

- 4 张主表
- 7 个核心视图
- 1 个 linked Doc 模板
- 1 组本地 connector-ready 服务配置

## 你只需要介入的两步

### 1. 编辑授权

使用有编辑权限的飞书账号登录当前页面，让我能：

- 新建独立 Base
- 新建表、字段、视图
- 新建 Doc 模板

### 2. 自建应用授权

当开始接通 connector 时，需要提供：

- `FEISHU_APP_ID`
- `FEISHU_APP_SECRET`
- `FEISHU_VERIFY_TOKEN`
- `FEISHU_ENCRYPT_KEY`

## Base 结构

按 [bitable-schema.md](/Users/liming/AI%20Project/codex-force-claw/FORCE-CLAW/feishu-short-video-growth-mvp/workflow-pack/short-video-growth/bitable-schema.md) 建立：

1. `Topic Candidate`
2. `Content Draft`
3. `Performance Review`
4. `Evolution Rule`

## 必建视图

- `待选题 Top 3`
- `候选池总览`
- `研究中`
- `待发布`
- `待复盘`
- `双平台对比`
- `进化规则库`

## Doc 模板

按 [research-script-doc-template.md](/Users/liming/AI%20Project/codex-force-claw/FORCE-CLAW/feishu-short-video-growth-mvp/workflow-pack/short-video-growth/research-script-doc-template.md) 创建模板，固定段落：

- 故事角度
- 有料/反认知
- 人物/事件/证据线索
- 脚本结构
- 原力创业收束
- 发布备注
- 复盘结论

## 本地服务接通

本地先用：

```bash
cd "/Users/liming/AI Project/codex-force-claw/FORCE-CLAW/feishu-short-video-growth-mvp"
python3 run_local.py
```

验证：

- `GET /health`
- `POST /events` challenge
- `POST /jobs/full-run`

## MVP 完成标准

必须同时满足：

- Base 中每轮出现 3 个 shortlisted topics
- 选中 topic 会生成一条 draft 和一份 Doc
- 视频号/小红书都有 publish package
- 指标能进 `Performance Review`
- `Evolution Rule` 至少有一条回写

## 当前阻塞

- 当前 Feishu 页面还是访客读权限
- 还没有自建应用凭据
- 所以我现在能做的是准备好所有对象结构、服务、样例数据和验证脚本；真正写入飞书需要你完成那一次账号授权

## 2026-03-10 现场观察

我在访客可读权限下已经确认：

- 当前 base token：`ZqsUbVegpaskp5sYcQTcCXOvn4c`
- 已存在短视频相关表：
  - `闭环总览` `tbl2L1C6R6ah52V3`
  - `选题候选` `tbl1ud63yTYJG33C`
  - `脚本包` `tbl11Caf7HtwylDF`
  - `反馈复盘` `tbl3OJJZ8tvHsxiq`
- 当前记录状态：
  - `闭环总览` 总记录 `11`，非空记录 `1`
  - `选题候选` 总记录 `10`，非空记录 `3`
  - `脚本包` 总记录 `10`，非空记录 `1`
  - `反馈复盘` 总记录 `10`，非空记录 `1`

这说明飞书现场已经有一版短视频承载结构，但我还不能判断字段是否符合最终 MVP，因为当前没有编辑权限，也拿不到完整字段配置面板。
