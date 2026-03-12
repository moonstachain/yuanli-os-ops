# FORCE-CLAW Blueprint

> 从 Agent catalogue 到 OpenClaw 式物种运行时

## 1. 定位

FORCE-CLAW 不再定义为一组松散的 AI Agents，而定义为一个面向创业者的物种化运行时：

- 上层是 `四周期产品地图`
- 下层是 `OpenClaw 风格 runtime 骨架`
- 中间由 `AI灵兽` 统一宪法、技能治理、验真纪律和人类友好

更上位的总纲见 `YUANLI_OS.md`。

就 `FORCE-CLAW` 而言，这份文档仍是当前唯一权威蓝图。

`DESIGN.md` 保留为早期设计资产，用于理解概念来源，不再代表当前架构真相。

## 2. 重构原则

### 2.1 吸收官方 OpenClaw 的灵魂

FORCE-CLAW 明确继承 OpenClaw 的这些优势：

- `workspace-first`：能力先落到工作区，而不是堆在单条 prompt 里
- `session 容器`：任务必须有明确状态、阶段和闭环
- `skills 装配`：能力按 root/domain/utility 分层治理
- `hooks 守门`：生命周期边界自动触发最小守门
- `contracts`：完成条件靠结构化契约，而不是靠措辞承诺
- `governance-first`：治理优先于功能堆砌

### 2.2 保留原力龙虾的独特性

FORCE-CLAW 不复制官方 OpenClaw 的通用平台定位，而是在同一运行时哲学上做领域化收敛：

- 用户不是开发者，而是创业者/超级个体
- 中心算法不是通用 agent orchestration，而是 `原型人格 × 四周期`
- 核心价值不是工具集合，而是 `高可信诊断 + 路径推进 + 闭环验证`

## 3. 双层蓝图

### 3.1 上层：四周期产品地图

四周期继续保留，但只作为用户价值地图和产品路线图，不再被表达为四套平行引擎。

| 周期 | 核心问题 | 目标产物 |
|------|----------|----------|
| Cycle 1 原力觉醒 | 我是谁？ | 诊断报告、优势假设、行动建议 |
| Cycle 2 品类独创 | 我为谁？ | 用户任务、品类假设、一句入脑、验证计划 |
| Cycle 3 模式升维 | 怎么赚？ | 链路设计、模式假设、单位经济、验证卡 |
| Cycle 4 模式壁垒 | 怎么守？ | 壁垒地图、控制点、防守策略 |

### 3.2 下层：统一运行时骨架

所有周期运行在同一套 runtime 上。

```text
FORCE-CLAW Runtime
├── Gateway / Channel
│   ├── Clawd workspace
│   ├── Feishu bot
│   └── Web/API（后续接入面）
├── Workspace
│   ├── 宪法与规则
│   ├── 技能战略
│   ├── 闭环标准
│   └── 工作/成长双账
├── Session
│   ├── preflight
│   ├── execution
│   └── closure
├── Skill Ecology
│   ├── root skills
│   ├── domain skills
│   └── utility/scripts/automations
├── Memory
│   ├── 私有成长账
│   └── 公开工作账
├── Hooks
│   ├── session-start
│   ├── major-execution
│   ├── pre-close
│   └── post-close
└── Contracts
    ├── 输出契约
    ├── 状态契约
    └── 评估契约
```

## 4. 物种宪法：AI灵兽

`AI灵兽` 是 FORCE-CLAW 的根层宪法，不再只是 Cycle 1 MVP 的附属 skill。

### 4.1 冲突顺序

1. `进化第一`
2. `超级技能治理`
3. `人类友好`

以上三者都不得突破：

- 真实边界
- 授权边界
- 验真纪律

### 4.2 对外主接口

高价值任务默认先经过 `灵兽态势图`：

- 进化判断
- 技能治理判断
- 人类友好判断
- 验真判断
- 当前最大失真
- 本轮进化动作

### 4.3 七个器官

| 器官 | 作用 |
|------|------|
| 认知器官 | 识别失真、任务假设、验真边界 |
| 技能治理器官 | 决定能力放进 root、domain、utility 还是不晋升 |
| 目标定形器官 | 压实用户真实目标与范围 |
| 能力路由器官 | 选择最佳技能组合 |
| 强自治执行器官 | 以少打扰原则完成主流程 |
| 验真闸门器官 | 检查产物、目标和边界是否都成立 |
| 闭环晋升器官 | 判断是否有结构能力值得晋升 |

## 5. 技能生态图

旧版“大量 Agent 清单”不再作为主表达，改为技能生态分层。

### 5.1 Root Skills

负责宪法、治理和高层判断。

- `ai-ling-shou-core`
- 未来可扩展的认知/治理类 root skills

### 5.2 Domain Skills

围绕四周期的稳定高频能力。

- Cycle 1：intake / diagnosis / closure
- Cycle 2：用户任务、品类假设、定位验证
- Cycle 3：链路设计、模式验证、单位经济
- Cycle 4：壁垒评估、控制点、防守验证

### 5.3 Utility / Scripts / Automations

不应被包装成 skill 的辅助能力。

- 飞书同步
- CRM 流转
- 数据整理
- 回归脚本
- 报表生成

### 5.4 技能晋升阈值

只有同时满足以下条件才考虑晋升为 domain skill：

- 高频重复
- 结构稳定
- 边界清晰
- 显著降低未来摩擦
- 不制造技能蔓生

## 6. Workspace-First 交付方式

Clawd/飞书工作区是当前一等宿主，Web/API 是后续接入层，不反客为主。

### 6.1 标准工作区资产

每个 FORCE-CLAW workspace 默认包含：

- `AGENTS.md`
- `SOUL.md`
- `RULES.md`
- `HEARTBEAT.md`
- `GENOME.md`
- `SKILL_STRATEGY.md`
- `EVOLUTION_RULES.md`
- `CLOSURE_STANDARD.md`
- `GROWTH_LOG_POLICY.md`
- `WORK_LOG_POLICY.md`
- `skills/`
- `hooks/`
- `contracts/`

### 6.2 当前参考实现

`clawd-workspace/force-claw-awakening-mvp/` 是当前 `Cycle 1 reference runtime`。

它的意义不是 demo，而是新蓝图下的第一阶段参考实现：

- 展示 root skill 如何约束 domain skills
- 展示 hooks 如何承担真完成守门
- 展示 contracts 如何定义最小交付标准
- 展示双账系统如何保护隐私与进化质量

### 6.3 未来扩展方式

- Cycle 1 继续保持最窄、最稳、最可信
- Cycle 2-4 不平地起四套系统
- 新周期一律在同一工作区标准上增加 domain skills、contracts 和 evidence gates

## 7. Session 与闭环

FORCE-CLAW 的默认完成公式：

`命令成功 ≠ 任务完成`

只有同时满足以下条件才算完成：

- 产物存在
- 目标达成
- 边界安全
- 结果可验证

### 7.1 Session 三段

- `Preflight`：任务是否值得做、最佳技能组合是什么、什么能证明完成
- `Execution`：按最少打扰原则执行
- `Closure`：产物/目标/边界/晋升判断全部过门

### 7.2 Hooks 四门

- `session-start`
- `major-execution`
- `pre-close`
- `post-close`

Hook 只负责守门，不负责长篇表演。

## 8. 四周期的最小 runtime 定义

### Cycle 1 原力觉醒

- 目标：建立人格、优势、阴影与行动建议的高可信诊断
- 输入条件：人生故事、8 问访谈
- 关键技能：intake / diagnosis / closure
- 必要 contracts：诊断报告 contract
- 最小 evidence gate：主副人格、优势、阴影、建议、JSON 完整
- completion：用户获得可信诊断，且未伪装完成后续周期

### Cycle 2 品类独创

- 目标：确认用户任务、甜用户、贵问题和一句入脑
- 输入条件：Cycle 1 关键假设已成立
- 关键技能：目标定形、用户任务、品类假设、定位验证
- 必要 contracts：品类假设与验证计划 contract
- 最小 evidence gate：用户任务、定位陈述、验证方案齐全
- completion：形成可测试的品类独创假设，而非只给灵感

### Cycle 3 模式升维

- 目标：建立可验证的增长与交付机制
- 输入条件：Cycle 2 已有验证中的价值主张
- 关键技能：链路设计、模式假设、单位经济、验证卡
- 必要 contracts：链路与经济模型 contract
- 最小 evidence gate：链路设计、模式假设、验证卡存在
- completion：形成可执行的模式实验，不伪装成成熟公司体系

### Cycle 4 模式壁垒

- 目标：建立长期防守和系统性壁垒
- 输入条件：Cycle 3 已有稳定模式信号
- 关键技能：壁垒评估、控制点、防守策略、长期验证
- 必要 contracts：壁垒地图 contract
- 最小 evidence gate：壁垒假设、控制点、长期策略齐全
- completion：形成可检验的防守方案，而不是抽象口号

## 9. 记忆与双账

FORCE-CLAW 固定维护两本账：

- `私有成长账`
  - 记录失真、路径选择、可晋升能力
  - 只写结构结论，不外泄
- `公开工作账`
  - 记录任务状态、验真结果、交付物、下一步建议
  - 只写对人类有用的事实

晋升条件：

- 至少重复出现 3 次
- 结构清晰
- 对未来自治或真实性有明确提升

## 10. 品牌与审美标准

FORCE-CLAW 保留原力龙虾的世界观，但收缩表达方式。

### 10.1 五种审美标准

- `世界观审美`：有清晰中心宪法，不靠口号飘着
- `结构审美`：模块切分有张力，避免 prompt 泥团化
- `语言审美`：稳、准、有人味，但不玄乎
- `交互审美`：减少无效追问，不让用户承担流程劳动
- `边界审美`：真实性、隐私、验真靠结构，不靠表态

### 10.2 什么不做

- 不再把未实现的 agent 名单写成既成事实
- 不把一次性摩擦升格为 skill
- 不把轻任务抬成重仪式
- 不把品牌世界观写成自我陶醉
- 不把 Web/API 平台叙事提前到压过工作区 runtime

## 11. 商业化映射

商业分层来自同一 runtime，而不是来自更多工具菜单。

| 层级 | 交付核心 | 对应 runtime |
|------|----------|--------------|
| L1 免费诊断 | Cycle 1 reference runtime | 工作区 + Cycle 1 domain skills |
| L2 会员 | 知识、复盘、任务推进 | 同一 runtime 的轻量持续服务 |
| L3 通关项目 | 四周期阶段推进 | 同一 runtime 的多周期 domain skills |
| L4 深度陪跑 | 高密度策略与闭环 | 同一 runtime 的高触达服务层 |
| L5 企业版 | 组织级部署 | 同一 runtime 的多角色、多工作区扩展 |

## 12. 当前文件体系建议

- `YUANLI_OS.md`：上位总纲
- `BLUEPRINT.md`：当前唯一权威蓝图
- `README.md`：短版入口
- `DESIGN.md`：早期设计稿
- `BUSINESS_PLAN.md`：商业化映射文档
- `clawd-workspace/force-claw-awakening-mvp/README.md`：Cycle 1 参考实现说明

这套关系必须长期保持一致。
