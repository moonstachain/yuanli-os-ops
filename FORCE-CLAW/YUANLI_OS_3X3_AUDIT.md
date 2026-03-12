# 原力OS 3x3 全域战略审计报告

> 审计时点：`2026-03-12` 本地可检索快照  
> 审计公式：`治理OS × 工作OS = 原力OS 3x3 审计矩阵`

本报告不是重写 [YUANLI_OS.md](./YUANLI_OS.md)。

它的角色是把 `原力OS` 从总纲推进到一次真实的系统级盘点：当前到底有哪些可验证资产，哪些只是叙事，哪些已经形成操作系统，哪些还停留在实验层。

## 1. 执行摘要

### 1.1 总评级

`总体评级：B`

结论不是“系统还没东西”，而是：

- 这已经不是一个空概念系统，而是一个 `治理强于广度` 的内部高验证实验系统。
- 当前最强资产不是单个模型或单篇内容，而是 `guan-jia-claw` 这套有 canonical task ledger、有 runtime artifacts、有 verification 文件的运行骨架。
- 当前最大的战略短板不是“不会做事”，而是 `中层编排能力不足`、`多表面覆盖不足`、`transport 与 access gate 仍然脆弱`。
- 当前最容易产生的错觉，是把这些内部高验证实验，误判成已经跨越到真实多表面生产系统。

主证据：

- `FORCE-CLAW/clawd-workspace/guan-jia-claw-workspace/state/task-ledger.json`
- `FORCE-CLAW/clawd-workspace/guan-jia-claw-workspace/runtime-artifacts/README.md`
- `FORCE-CLAW/clawd-workspace/force-claw-content-race-mvp/runtime-artifacts/runs/real-round-20260310-01/round_status.json`
- `FORCE-CLAW/feishu-short-video-growth-mvp/runtime-artifacts/state/full_run_summary.json`
- `/Users/liming/.codex/skills/ai-da-guan-jia/artifacts/ai-da-guan-jia/reviews/2026-03-12/adagj-review-20260312-220318/review.json`

### 1.2 六判断

- `自治判断`
  当前审计可高自治推进，因为主证据都在本地，且已有 canonical ledger、runtime artifacts 与 skill review 快照。
- `全局最优判断`
  当前最优不是继续扩题材或扩 surface，而是先补 `中层 routing-playbook`、`worker transport 稳定性` 和 `canonical 字段闭环`。
- `能力复用判断`
  当前最该复用的不是新增 skill，而是已有的 `ai-da-guan-jia`、`ai-metacognitive-core`、`guan-jia-claw runtime`、`pilot 证据链`。
- `验真判断`
  这个系统最有价值的部分，是它已经形成了 `verification-first` 习惯；最危险的部分，是部分 canonical state 还没有把 verification 字段收紧到位。
- `进化判断`
  当前最适合晋升的不是更多 persona，而是 `中层编排手册`、`workflow hardening`、`evidence canonicalization`。
- `当前最大失真`
  把 `内部高验证的实验系统` 误读成 `已经完成多表面生产化的操作系统`。

### 1.3 最关键结论

1. `总纲与蓝图` 已经形成一致结构，方向不是问题。
2. `guan-jia-claw` 已经形成真实运行骨架，但仍高度集中于 `codex_backend + green lane` 的内部场景。
3. `公众号/多机 pilot` 已经形成可验证的阶段式证据链，是当前最接近“可复制执行系统”的部分。
4. `内容赛马` 与 `短视频增长` 仍更像有结构的实验资产，而不是成熟运行系统。
5. `106 个 skill` 带来了覆盖度，但中层 playbook 缺失，使系统更像“能力森林”，还不像“稳定交通网”。

## 2. 审计范围与证据底座

### 2.1 Included：canonical evidence

以下资产纳入主审计：

- `FORCE-CLAW/YUANLI_OS.md`
- `FORCE-CLAW/BLUEPRINT.md`
- `FORCE-CLAW/README.md`
- `FORCE-CLAW/clawd-workspace/guan-jia-claw-workspace/state/task-ledger.json`
- `FORCE-CLAW/clawd-workspace/guan-jia-claw-workspace/state/worker-registry.json`
- `FORCE-CLAW/clawd-workspace/guan-jia-claw-workspace/runtime-artifacts/runs/**`
- `FORCE-CLAW/clawd-workspace/guan-jia-claw-workspace/runtime-artifacts/pilots/**`
- `FORCE-CLAW/clawd-workspace/force-claw-content-race-mvp/runtime-artifacts/runs/real-round-20260310-01/*`
- `FORCE-CLAW/feishu-short-video-growth-mvp/runtime-artifacts/state/*`
- `AI大管家` 当日 `review-skills` 快照与 route 快照

纳入理由：

- 有明确文件落点
- 有 contract 或 state 角色
- 能承载审计判断，而不是只承载叙事

### 2.2 Supporting：辅助证据

以下资产作为辅证使用：

- `output/dify-cycles/demo-20260310-001/*`
- 局部失败 run 下的 `result.json`、`verification.json`、`summary.md`
- `AI大管家` 当日 `inventory-skills` 原始扫描快照

使用规则：

- 只用来解释失败链路、补足背景或说明跨系统连接情况
- 不用它们单独得出总判断

### 2.3 Excluded：噪音与排除项

以下资产不进入主审计：

- `tmp-*`
- `node_modules`
- `.pyc`
- 原始 auth storage
- 历史 backup
- 无 contract、无 canonical state 角色的零散输出目录

排除理由：

- 这些文件会放大动作噪音
- 不能代表系统真完成
- 容易把“产物很多”误判成“系统成熟”

### 2.4 关键计数快照

本报告的关键数字口径如下：

| 指标 | 结果 | 口径说明 |
|---|---:|---|
| 顶层 skills | 106 | 以 `review-skills` 的 normalized snapshot 为准 |
| raw inventory count | 108 | 以 `inventory-skills` 扫描结果为辅证，不作为主口径 |
| GitHub 来源 skills | 31 | 来自 `review.json` |
| canonical tasks | 30 | 来自 `task-ledger.json` |
| guan-jia run 目录 | 31 | 来自 `runtime-artifacts/runs/` |
| verification files | 65 | 来自 `runtime-artifacts/**/verification.json` 搜索结果 |
| verified | 59 | 同上 |
| failed | 6 | 同上 |
| blocked tasks | 4 | 来自 `task-ledger.json` |
| preflight tasks | 1 | 来自 `task-ledger.json` |
| registered workers | 1 | 来自 `worker-registry.json` |

方法说明：

- `106` 与 `108` 的差异说明当前 inventory 与 review 的总数口径尚未完全统一
- 这本身也是一个治理问题，而不是简单统计误差

## 3. 总体盘点

### 3.1 repo 运行资产

当前 repo 里最成熟的运行资产是 `guan-jia-claw workspace`。

它的成熟度并不体现在“功能多”，而体现在：

- 有 `canonical task state`
- 有 `runtime-artifacts`
- 有 `verification.json`
- 有 `pilot` 分阶段证据链
- 有 `worker registry`

但它也非常清楚地暴露出边界：

- 30 条 canonical tasks 全部来自 `codex_backend`
- 30 条 tasks 全部是 `green lane`
- canonical task 中 `verification_status`、`summary_granularity` 仍未闭环写入

这说明它现在是一个 `后台高验证控制面`，还不是 `多表面、多风险等级、多路由制度` 的成熟运行系统。

主证据：

- `FORCE-CLAW/clawd-workspace/guan-jia-claw-workspace/README.md`
- `FORCE-CLAW/clawd-workspace/guan-jia-claw-workspace/state/README.md`
- `FORCE-CLAW/clawd-workspace/guan-jia-claw-workspace/state/task-ledger.json`

### 3.2 实验资产

当前实验资产分成两类：

- `公众号/多机 pilot`
  已形成相对完整的阶段式链路，含 `style / topic_outline / draft / titles`
- `内容赛马 / 短视频增长`
  已形成一定的策略与输出资产，但证据密度和闭环完整度明显低于 `guan-jia-claw`

这里最重要的结论是：

- 公众号 pilot 已经可以证明“结构化执行”存在
- 内容赛马和短视频增长更多证明“方向与意图存在”，尚未证明“系统已跑稳”

主证据：

- `FORCE-CLAW/clawd-workspace/guan-jia-claw-workspace/runtime-artifacts/README.md`
- `FORCE-CLAW/clawd-workspace/force-claw-content-race-mvp/runtime-artifacts/runs/real-round-20260310-01/round_status.json`
- `FORCE-CLAW/feishu-short-video-growth-mvp/runtime-artifacts/state/full_run_summary.json`

### 3.3 skill 生态

skill 生态的事实不是“太少”，而是“太多但中层不足”。

当前结构快照显示：

- 顶层 skill 总数 `106`
- `专家角色层` 有 `56`
- `元治理层` 有 `9`
- `平台/工具集成层` 有 `20`
- `垂直工作流层` 有 `21`

这意味着系统已经有很强的覆盖度，但不意味着调用成本低。

`review-skills` 已经明确指出：

- 最强集群是 `工作流完整度高`、`平台证据型技能`
- 最弱集群是 `人格说明型技能过多`、`轻结构技能偏多`
- 缺失的中层能力包括 `routing-playbook`、`workflow-hardening`、`skill-deduper`

所以 skill 生态的主问题，不是“有没有能力”，而是“有没有中层交通规则”。

主证据：

- `/Users/liming/.codex/skills/ai-da-guan-jia/artifacts/ai-da-guan-jia/reviews/2026-03-12/adagj-review-20260312-220318/review.md`
- `/Users/liming/.codex/skills/ai-da-guan-jia/artifacts/ai-da-guan-jia/reviews/2026-03-12/adagj-review-20260312-220318/review.json`

## 4. 3x3 审计矩阵

判断标准固定为三档：

- `已形成`
- `部分形成`
- `缺口`

### 4.1 子系统一：总纲与蓝图一致性

`总体评级：A-`

主证据：

- `FORCE-CLAW/YUANLI_OS.md`
- `FORCE-CLAW/BLUEPRINT.md`
- `FORCE-CLAW/README.md`

当前最大失真：

- 总纲与蓝图已经一致，但“周期蓝图”“workspace 运行时”“外部审计机制”还没有形成固定的季度或阶段性复查制度。

下一步战略含义：

- 方向层已经稳，接下来不该再大量改名，而应该把审计与进化机制固化下来。

| 工作层 | 递归进化 | 全局最优 | 人类友好 |
|---|---|---|---|
| `主题层` | 已形成。证据：`YUANLI_OS.md` 已把治理OS与工作OS定成上位总纲。失真：总纲刚建立，主题级复查节奏还没制度化。 | 已形成。证据：`README.md` 与 `BLUEPRINT.md` 都把 FORCE-CLAW 放在原力OS框架下解释。失真：仍可能被旧的 agent catalogue 叙事回拉。 | 部分形成。证据：`README.md` 已压缩成短入口。失真：关键判断仍分散在多份文档里，首次进入者仍需跨文档切换。 |
| `策略层` | 部分形成。证据：`BLUEPRINT.md` 已把 runtime、session、hooks、contracts 讲清。失真：缺少定期审计蓝图是否偏航的制度。 | 已形成。证据：`BLUEPRINT.md` 明确“唯一权威蓝图”，避免多套平行真相。失真：总纲与实现之间仍缺自动化一致性检查。 | 部分形成。证据：`README.md` 已明确宿主、关键文档与本地校验。失真：文档入口清晰，但策略分层对新参与者仍偏重。 |
| `执行层` | 部分形成。证据：本次已新增独立审计文档，说明执行层开始反哺总纲。失真：审计产物仍是文档驱动，未形成自动快照。 | 部分形成。证据：`BLUEPRINT.md` 已要求“命令成功不等于任务完成”。失真：repo 中尚无一条自动守门会因总纲偏离而阻断执行。 | 已形成。证据：`README.md` 当前入口已把总纲、蓝图、运行时说明并列收敛。失真：人类入口更友好，但系统入口仍不够自动化。 |

### 4.2 子系统二：guan-jia-claw 任务与运行系统

`总体评级：B+`

主证据：

- `FORCE-CLAW/clawd-workspace/guan-jia-claw-workspace/README.md`
- `FORCE-CLAW/clawd-workspace/guan-jia-claw-workspace/state/task-ledger.json`
- `FORCE-CLAW/clawd-workspace/guan-jia-claw-workspace/state/worker-registry.json`
- `FORCE-CLAW/clawd-workspace/guan-jia-claw-workspace/runtime-artifacts/README.md`

当前最大失真：

- 它已经是一个强验证后台系统，但还不是一个真实多 surface 的协作系统；目前 ledger 事实几乎全部收敛到 `codex_backend`。

下一步战略含义：

- 不应再把资源主要投入新能力，而应优先把现有运行系统扩到 `多表面 + 多 lane + canonical verification 字段闭环`。

| 工作层 | 递归进化 | 全局最优 | 人类友好 |
|---|---|---|---|
| `主题层` | 部分形成。证据：`README.md` 已定义接任务、看待办、收尾复盘等固定意图。失真：`task-ledger.json` 里的主题几乎都还是 OpenClaw、wechat、concurrency、vscode 这类内部验证主题。 | 部分形成。证据：系统明确把 `假完成` 作为第一风险。失真：30 条 tasks 全部来自 `codex_backend` 且全部是 `green lane`，说明主题层的场景广度仍不足。 | 部分形成。证据：`README.md` 强调低打扰、显式授权、复杂任务切后台。失真：实际 ledger 还没有真实飞书群或客户群任务来证明这套人类友好机制已跑通。 |
| `策略层` | 已形成。证据：`task-ledger.json` 已是 canonical state，`runtime-artifacts/README.md` 明确每次运行必须留痕。失真：任务事实在积累，但还没升格为跨主题的中层策略手册。 | 部分形成。证据：`README.md` 定义绿区/黄区/红区路由制度。失真：ledger 当前没有显示真实的 lane 差异，策略设计比实际运行更成熟。 | 部分形成。证据：线程授权码、公开 recap、写后重读都在设计里。失真：任务主账尚未把 `verification_status`、`summary_granularity` 等协作关键信息填实。 |
| `执行层` | 已形成。证据：当前有 31 个 run 目录和 65 个 verification 文件，其中 59 个 verified。失真：执行证据很多，但 canonical state 与 verification 字段没有完全打通。 | 部分形成。证据：`verification.json` 能明确区分 `transport_failed` 与 `remote_command_failed`。失真：仍有 6 个 failed、4 个 blocked，说明执行稳定性未过生产门槛。 | 部分形成。证据：worker registry、远程派单、public recap 设计都在。失真：`worker-registry.json` 只有 1 个 worker，且运行时健康状态未写成更强的 canonical 视图。 |

### 4.3 子系统三：公众号 / 多机 pilot 证据链

`总体评级：B`

主证据：

- `FORCE-CLAW/clawd-workspace/guan-jia-claw-workspace/runtime-artifacts/README.md`
- `FORCE-CLAW/clawd-workspace/guan-jia-claw-workspace/runtime-artifacts/pilots/wechat-demo-smoke/stages/*`
- `FORCE-CLAW/clawd-workspace/guan-jia-claw-workspace/runtime-artifacts/pilots/yuanli-openclaw-visible-20260312-1148/stages/*`
- 对应 run 下的 `verification.json`

当前最大失真：

- 它已经证明了“阶段式可执行”，但还没有证明“在更广题材、更复杂来源、更高频需求下同样稳定”。

下一步战略含义：

- 公众号 pilot 最适合被提升为可复制流程资产，但前提是先减少重复重跑、补齐 stage 级回滚与统一 summary。

| 工作层 | 递归进化 | 全局最优 | 人类友好 |
|---|---|---|---|
| `主题层` | 已形成。证据：已存在 `wechat-demo-smoke`、`yuanli-openclaw-cold-thinking`、`yuanli-openclaw-visible` 等多轮 pilot。失真：主题仍然高度集中于 OpenClaw 与公众号写作，覆盖面偏窄。 | 部分形成。证据：同一主题被多轮迭代，说明系统在主动寻找更优切法。失真：多次围绕同一主题重试，也说明主题层还没有形成更高层的取舍机制。 | 部分形成。证据：把 style、topic_outline、draft、titles 拆段，降低一次性认知负担。失真：主机仍需承担收尾与多次重发，人的流程劳动尚未最小化。 |
| `策略层` | 已形成。证据：`01-style-dna.md`、`02-style-calibration.md`、`03-topic-angles.md` 等链路明确存在。失真：这些策略资产尚未升格为跨 pilot 复用的统一模板库。 | 部分形成。证据：能通过阶段拆解把“写作”拆成更细的打法单元。失真：是否真的服务业务目标，目前更多靠主题判断而不是跨项目指标验证。 | 部分形成。证据：策略被拆成短阶段，便于校验。失真：当某一阶段失败时，仍会把新的协调成本推回给主机与操作者。 |
| `执行层` | 已形成。证据：各个 stage 下都有 `result.json` 与 `verification.json`。失真：阶段产物齐全，但最终 package 的一次性整体验真仍偏人工。 | 部分形成。证据：大多数 stage 是 verified。失真：`wechat-demo-smoke topic_outline` 和若干 OpenClaw 相关 run 出现过 `remote_command_failed`。 | 部分形成。证据：worker 承接了 Style DNA、初稿、标题等重活。失真：transport 与失败重跑仍让人承担较重的操作与判错成本。 |

### 4.4 子系统四：内容赛马与短视频增长实验系统

`总体评级：C+`

主证据：

- `FORCE-CLAW/clawd-workspace/force-claw-content-race-mvp/README.md`
- `FORCE-CLAW/clawd-workspace/force-claw-content-race-mvp/runtime-artifacts/runs/real-round-20260310-01/round_manifest.json`
- `FORCE-CLAW/clawd-workspace/force-claw-content-race-mvp/runtime-artifacts/runs/real-round-20260310-01/round_status.json`
- `FORCE-CLAW/feishu-short-video-growth-mvp/runtime-artifacts/state/full_run_summary.json`
- `FORCE-CLAW/feishu-short-video-growth-mvp/runtime-artifacts/state/performance_reviews.json`

当前最大失真：

- 这部分系统最容易显得“已经有策略和产物”，但主流程实际上还被 `auth/access gate` 卡住，成熟度明显低于 guan-jia-claw。

下一步战略含义：

- 不应继续把它包装成成熟业务系统，而应明确把它定义成 `受 gate 约束的实验编排系统`，先解决 access 和 shared evidence 问题。

| 工作层 | 递归进化 | 全局最优 | 人类友好 |
|---|---|---|---|
| `主题层` | 部分形成。证据：`README.md` 固定了小红书图文、OpenAI/模型热点等主题桶。失真：主题定义存在，但真实共享证据仍未到位。 | 部分形成。证据：`full_run_summary.json` 已能从 shortlist 选出一个主题。失真：当前被选主题还未经过同等密度的真实渠道验证。 | 部分形成。证据：主题和发布平台被明确写出，减少决策游离。失真：Feishu 登录、XHS IP 风险仍把人重新拖回 access 处理。 |
| `策略层` | 部分形成。证据：`performance_reviews.json` 已有 review_count=2、rule_count=2。失真：规则数量很少，说明策略层还处在早期试验阶段。 | 部分形成。证据：内容赛马定义了四方 workflow race 和统一评分。失真：`round_status.json` 显示 scorecard 仍因 shared evidence 缺失而 pending。 | 缺口。证据：`round_status.json` 的 next_actions 仍要求人工登录、手动重建 digest。失真：策略层知道该怎么做，但人类友好度不够。 |
| `执行层` | 部分形成。证据：已有 `round_manifest.json`、`worklog.md`、`full_run_summary.json` 等执行产物。失真：这些产物更多证明“流程被设计”，还不等于“流程已跑稳”。 | 缺口。证据：`round_status.json` 明确 `status=blocked_auth_or_access_gate`、`closure_state=not_closed`。失真：系统对边界诚实，但执行结果尚未形成闭环。 | 缺口。证据：卡点主要是 Feishu auth 和 XHS IP 风险。失真：当前执行链仍高度依赖人工过 gate，不满足低打扰标准。 |

### 4.5 子系统五：skill 生态与中层编排能力

`总体评级：B-`

主证据：

- `/Users/liming/.codex/skills/ai-da-guan-jia/artifacts/ai-da-guan-jia/reviews/2026-03-12/adagj-review-20260312-220318/review.md`
- `/Users/liming/.codex/skills/ai-da-guan-jia/artifacts/ai-da-guan-jia/reviews/2026-03-12/adagj-review-20260312-220318/review.json`
- `/Users/liming/.codex/skills/ai-da-guan-jia/artifacts/ai-da-guan-jia/inventory/skills-20260312-222100.json`

当前最大失真：

- 系统表面上像“能力过剩”，实际上是“中层交通不足”；很多 skill 可以完成任务，但系统还没有一张稳定的调用地图。

下一步战略含义：

- skill 战略现在不该追求继续扩容，而应该开始治理 `重复命名`、`persona 偏多`、`workflow hardening` 与 `routing-playbook`。

| 工作层 | 递归进化 | 全局最优 | 人类友好 |
|---|---|---|---|
| `主题层` | 部分形成。证据：`review.md` 已能识别最强集群、最弱集群和缺失中层能力。失真：能力主题被盘出来了，但还没有稳定映射到高频任务家族。 | 部分形成。证据：分层统计已经存在。失真：`106` 与 `108` 的口径差异说明总览层还未完全统一。 | 缺口。证据：56 个专家角色型 skill 会显著提高选择成本。失真：用户和上层路由器容易被命名密度拖慢。 |
| `策略层` | 部分形成。证据：daily review 已产出 A/B/C 三个候选进化动作。失真：这些动作还未进入固定节奏，不足以持续改造生态。 | 部分形成。证据：`routing-policy.md` 已定义任务适配度优先。失真：缺 `routing-playbook` 导致策略能判断，不能稳定落地。 | 缺口。证据：review 已明确 `人格说明型技能过多`、`轻结构技能偏多`。失真：对人类来说，系统仍不够“少打扰”。 |
| `执行层` | 部分形成。证据：`inventory-skills`、`route`、`review-skills` 已形成可执行工具链。失真：执行动作存在，但后续 resolve-action 还未形成常态化闭环。 | 部分形成。证据：review 能指出 overlap pairs 和 missing middle layer。失真：当前仍需人工读取 review，再转成结构性改造。 | 缺口。证据：没有 `routing-playbook` 时，skill 组合仍高度依赖顶层判断者的记忆。失真：系统覆盖度高，但调用摩擦也高。 |

## 5. 关键失真与根因

### 5.1 失真一：内部高验证，被误判成多表面生产化

结论：

- 这套系统最强的是内部控制面，不是全域生产面。

根因：

- canonical tasks 全部来自 `codex_backend`
- 所有 tasks 当前都在 `green lane`
- 尚无足够真实飞书群面、客户群面、外部写面进入主账

主证据：

- `FORCE-CLAW/clawd-workspace/guan-jia-claw-workspace/state/task-ledger.json`

### 5.2 失真二：verification 很强，但 canonical state 没完全接住

结论：

- 验真文化已经形成，但 canonical 字段闭环还不够强。

根因：

- `verification.json` 很多
- `task-ledger.json` 中 `verification_status`、`summary_granularity` 当前缺失

主证据：

- `FORCE-CLAW/clawd-workspace/guan-jia-claw-workspace/state/task-ledger.json`
- `FORCE-CLAW/clawd-workspace/guan-jia-claw-workspace/runtime-artifacts/README.md`

### 5.3 失真三：worker 已注册，但 transport 仍是脆弱点

结论：

- 运行系统的主要失败并不是“没有思路”，而是 `transport` 与 `remote command` 脆弱。

根因：

- 失败样本明确显示 `transport_failed`
- 失败样本也显示 `remote_command_failed`

主证据：

- `FORCE-CLAW/clawd-workspace/guan-jia-claw-workspace/state/worker-registry.json`
- `FORCE-CLAW/clawd-workspace/guan-jia-claw-workspace/runtime-artifacts/runs/gjc-20260312-061734-v1-39617f9c/verification.json`
- `FORCE-CLAW/clawd-workspace/guan-jia-claw-workspace/runtime-artifacts/runs/gjc-20260312-043450-concurrency-shell-smoke--7ed018ed/verification.json`

### 5.4 失真四：实验系统有方向，但尚未穿越 access gate

结论：

- 内容赛马和短视频增长并不是没有产物，而是策略先于执行成熟。

根因：

- 内容赛马被 `blocked_auth_or_access_gate` 卡住
- 短视频增长虽然有主题 shortlist 和 publish package，但 review_count、rule_count 仍低

主证据：

- `FORCE-CLAW/clawd-workspace/force-claw-content-race-mvp/runtime-artifacts/runs/real-round-20260310-01/round_status.json`
- `FORCE-CLAW/feishu-short-video-growth-mvp/runtime-artifacts/state/full_run_summary.json`

### 5.5 失真五：skill 覆盖很广，但中层编排缺位

结论：

- 目前最真实的技能问题不是“不够多”，而是“不够编排”。

根因：

- 缺少 `routing-playbook`
- persona-heavy skills 偏多
- overlap 与边界冲突已被 review 明确指出

主证据：

- `/Users/liming/.codex/skills/ai-da-guan-jia/artifacts/ai-da-guan-jia/reviews/2026-03-12/adagj-review-20260312-220318/review.md`

## 6. 战略建议

### 6.1 0-30 天：止血项

目标：

- 先把会伤害可信度的断点修掉

建议：

1. 修 `worker transport` 和 `host reachability`
   先让 `transport_failed` 不再成为高频失败源，再谈 worker 扩容。
2. 把 `verification_status`、`summary_granularity` 等关键字段打通到 `task-ledger.json`
   否则 verification 只会存在于 run 目录，难以变成真正的系统记忆。
3. 把 `blocked_auth_or_access_gate` 这类状态显式纳入实验系统的统一 lane
   不要让实验系统看起来像“做了一半”，而要清楚地标识“因 gate 暂停”。
4. 对 `公众号 / 多机 pilot` 做一次失败样本整理
   把 rerun 原因、transport 原因、command 原因分开，不再混在同一类失败里。

主证据：

- `FORCE-CLAW/clawd-workspace/guan-jia-claw-workspace/runtime-artifacts/runs/gjc-20260312-061734-v1-39617f9c/verification.json`
- `FORCE-CLAW/clawd-workspace/guan-jia-claw-workspace/runtime-artifacts/runs/gjc-20260312-043450-concurrency-shell-smoke--7ed018ed/verification.json`
- `FORCE-CLAW/clawd-workspace/force-claw-content-race-mvp/runtime-artifacts/runs/real-round-20260310-01/round_status.json`

### 6.2 30-90 天：增益项

目标：

- 把“高验证实验系统”推进到“更稳的系统操作层”

建议：

1. 新建 `routing-playbook`
   先覆盖 8 到 12 个最高频任务家族，把 skill 组合、默认顺序、验真清单固化下来。
2. 把 `guan-jia-claw` 从 `codex_backend` 扩到至少一个真实飞书内部群 lane
   否则人类友好与路由制度始终停留在设计层。
3. 为 `pilot` 建立统一的 stage summary contract
   让 style/topic/draft/titles 不只是有结果，还能有可汇总的统一结构。
4. 给 `content race` 增加 access gate 解除后的最小闭环模板
   把“blocked but honest”升级成“unblocked and comparable”。

主证据：

- `/Users/liming/.codex/skills/ai-da-guan-jia/artifacts/ai-da-guan-jia/reviews/2026-03-12/adagj-review-20260312-220318/review.md`
- `FORCE-CLAW/clawd-workspace/guan-jia-claw-workspace/README.md`

### 6.3 结构长期项：收敛项

目标：

- 让系统从“能力森林”变成“可运营操作系统”

建议：

1. 收敛 persona-heavy skills
   优先 harden 高频 agency skill，而不是继续扩角色数量。
2. 统一 skill 总数口径
   解决 `inventory=108` 与 `review=106` 的差异，避免治理报表失真。
3. 建立定期 `原力OS 3x3 审计`
   把这份报告从一次性盘点，升级成周期性治理机制。
4. 把 canonical evidence 统一到“主账 + run + verification + summary”四件套
   任何新工作区和实验系统都按同一最小标准收口。

主证据：

- `/Users/liming/.codex/skills/ai-da-guan-jia/artifacts/ai-da-guan-jia/reviews/2026-03-12/adagj-review-20260312-220318/review.json`
- `FORCE-CLAW/BLUEPRINT.md`

## 7. 优先级路线图

### P1：立刻做

- 稳定 worker transport
- 补 canonical verification fields
- 把 blocked gate 状态标准化

### P2：随后做

- routing-playbook MVP
- 飞书内部群真实 lane 扩展
- pilot stage summary contract

### P3：长期做

- skill 收敛与 hardening
- 定期原力OS审计
- 统一多工作区 evidence standard

## 8. 附录

### 8.1 主要证据文件清单

- `FORCE-CLAW/YUANLI_OS.md`
- `FORCE-CLAW/BLUEPRINT.md`
- `FORCE-CLAW/README.md`
- `FORCE-CLAW/clawd-workspace/guan-jia-claw-workspace/README.md`
- `FORCE-CLAW/clawd-workspace/guan-jia-claw-workspace/state/task-ledger.json`
- `FORCE-CLAW/clawd-workspace/guan-jia-claw-workspace/state/worker-registry.json`
- `FORCE-CLAW/clawd-workspace/guan-jia-claw-workspace/runtime-artifacts/README.md`
- `FORCE-CLAW/clawd-workspace/force-claw-content-race-mvp/runtime-artifacts/runs/real-round-20260310-01/round_manifest.json`
- `FORCE-CLAW/clawd-workspace/force-claw-content-race-mvp/runtime-artifacts/runs/real-round-20260310-01/round_status.json`
- `FORCE-CLAW/feishu-short-video-growth-mvp/runtime-artifacts/state/full_run_summary.json`
- `FORCE-CLAW/feishu-short-video-growth-mvp/runtime-artifacts/state/performance_reviews.json`
- `/Users/liming/.codex/skills/ai-da-guan-jia/artifacts/ai-da-guan-jia/reviews/2026-03-12/adagj-review-20260312-220318/review.json`
- `/Users/liming/.codex/skills/ai-da-guan-jia/artifacts/ai-da-guan-jia/reviews/2026-03-12/adagj-review-20260312-220318/review.md`

### 8.2 审计口径说明

- `canonical evidence`
  指能代表系统当前真相的 state、contract、run、verification 或 normalized review 快照。
- `supporting evidence`
  指有说明价值，但不足以单独代表系统真相的输出资产。
- `excluded noise`
  指不能稳定代表真完成、只会放大动作噪音的目录与文件。

### 8.3 最后结论

这套系统当前最值得珍惜的，不是它已经“什么都能做”，而是它已经长出了一个非常难得的能力：

`它开始把做事，变成一个可验证、可留证、可反思的系统。`

下一阶段真正的战略任务，不是继续堆更多东西，而是把这种能力：

- 从内部实验
- 推进到中层编排
- 再推进到更宽的真实表面

只有这样，`原力OS` 才会从一套很强的内部方法，真正长成一套外部可运行的操作系统。
