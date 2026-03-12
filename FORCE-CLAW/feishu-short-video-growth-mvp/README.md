# Feishu Short-Video Growth MVP

这是一套为 `原力创业` 短视频业务准备的 `Feishu MVP` 本地交付包。

它的角色不是替代飞书，而是把三件事压实：

1. `Feishu 侧对象结构` 已经定好
2. `本地 Python 边缘服务` 已经能跑通闭环示例
3. `你需要介入的授权步骤` 已经被压缩到最少
4. `飞书现场已补齐的对象` 已经有真实工作账可追溯

## 当前包含

- `workflow-pack/short-video-growth/`
  - Bitable schema
  - Doc 模板
  - acceptance checklist
  - sample topic leads
  - sample platform metrics
- `src/feishu_workflow_app/`
  - `/health`
  - `/events`
  - manual job endpoints
  - 本地 runtime，用于把 `选题 -> draft -> publish package -> review -> evolution rule` 跑通
- `deployment-checklist.md`
  - 上线检查和回滚点
- `run_demo.py`
  - 一键跑通本地短视频闭环示例

## 2026-03-10 已完成的飞书侧动作

已在现有飞书 base `新媒体-安克妙记多维表` 上完成最小闭环补齐，而不是另起独立 Base。

- 已确认并继续使用 4 张主表：
  - `选题候选`
  - `脚本包`
  - `反馈复盘`
  - `闭环总览`
- 已新建：
  - `进化规则库`
  - `短视频研究脚本模板`
- 已新建视图：
  - `待选题 Top 3`
  - `研究中`
  - `待发布`
  - `待复盘`
  - `双平台对比`
- 已确认样例闭环：
  - `选题候选` 3 条有效候选题
  - `脚本包` 1 条非空脚本包
  - `反馈复盘` 1 条非空复盘记录
  - `进化规则库` 1 条非空进化规则
  - `闭环总览` 1 条非空总览记录

## 快速开始

### 1. 本地闭环演练

```bash
cd "FORCE-CLAW/feishu-short-video-growth-mvp"
python3 run_demo.py
```

输出物会写到：

- `runtime-artifacts/docs/`
- `runtime-artifacts/publish/`
- `runtime-artifacts/state/`

### 2. 启动本地服务

```bash
cd "FORCE-CLAW/feishu-short-video-growth-mvp"
python3 run_local.py
```

可用接口：

- `GET /health`
- `POST /events`
- `POST /jobs/topic-ingest`
- `POST /jobs/create-draft`
- `POST /jobs/publish-package`
- `POST /jobs/import-metrics`
- `POST /jobs/extract-rules`
- `POST /jobs/full-run`

### 3. Feishu 落地

真正继续扩展飞书时，按 [feishu-build-runbook.md](./docs/feishu-build-runbook.md) 执行。

如果后续要把 Dify 的四个应用接到这套 Feishu MVP 上，先看 [dify-feishu-bridge.md](./docs/dify-feishu-bridge.md)。

## 当前真实边界

- 现有 `新媒体-安克妙记多维表` 已被补齐 MVP 对象，但还不是全自动生产系统
- 当前浏览器自动化已经拿到编辑权限，并完成了表/视图/文档的最小落地
- Feishu 自建应用凭据还没注入，所以 `/events` 目前仍是 connector-ready scaffold，不是已连通生产 app
- 当前 `脚本包` 还没有显式 `Doc URL` 字段，文档模板与运行记录之间仍是弱链接
- 当前视图只补齐了命名，筛选/排序规则还没全部收紧

## 2026-03-10 现场发现

浏览器现场读到的真实状态与最初假设有出入：

- 不需要从零创建独立 Base，现有 base 已足以承载 MVP
- 现场已经完成从只读勘测到编辑落地的切换
- 因此下次优先动作不再是“先建空壳”，而是：
  - 继续补齐筛选/排序和自动化规则
  - 给 `脚本包` 增加文档链接字段
  - 接通 Feishu 自建应用和外部 connector

详细现场记录见 [observed-feishu-state-2026-03-10.md](./docs/observed-feishu-state-2026-03-10.md)。
