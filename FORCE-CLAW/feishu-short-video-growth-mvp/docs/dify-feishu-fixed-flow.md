# Dify -> 飞书固定追加工作流

这套固定工作流现在有两层：

- 低层：`run artifact -> 飞书追加`
- 高层：`阶段结果 -> run artifact -> 飞书追加`

以后我跑完一轮 Dify 闭环后，会默认先把阶段产物收口成标准 run artifact，再自动把这轮结果追加到飞书。

## 当前落地物

- 规范化 run artifact 示例：
  - [demo-20260310-001.json](/Users/liming/AI%20Project/codex-force-claw/output/dify-runs/demo-20260310-001.json)
- 阶段产物目录示例：
  - [output/dify-cycles/demo-20260310-001](/Users/liming/AI%20Project/codex-force-claw/output/dify-cycles/demo-20260310-001/radar_candidates.json)
- 高层收口脚本：
  - [finalize_dify_cycle_to_feishu.py](/Users/liming/AI%20Project/codex-force-claw/scripts/finalize_dify_cycle_to_feishu.py)
- 追加同步脚本：
  - [sync_dify_cycle_to_feishu.py](/Users/liming/AI%20Project/codex-force-claw/scripts/sync_dify_cycle_to_feishu.py)

## 固定约定

未来每轮都按这个约定：

1. 先把 Dify 一轮的 7 个阶段结果保存到：
   - `/Users/liming/AI Project/codex-force-claw/output/dify-cycles/<run_id>/`
2. 阶段文件名固定为：
   - `radar_candidates.json`
   - `selected_topic.json`
   - `creative_package.json`
   - `orchestrator_after_script.json`
   - `feedback_record.json`
   - `feedback_analysis.json`
   - `orchestrator_after_feedback.json`
3. 默认执行高层收口脚本：

```bash
python3 "/Users/liming/AI Project/codex-force-claw/scripts/finalize_dify_cycle_to_feishu.py" \
  --run-id "<run_id>"
```

它会自动完成两步：

- 收口生成 `output/dify-runs/<run_id>.json`
- 调用低层同步脚本把结果写入飞书

如果只想验证收口而不写飞书，可以加：

```bash
python3 "/Users/liming/AI Project/codex-force-claw/scripts/finalize_dify_cycle_to_feishu.py" \
  --run-id "<run_id>" \
  --dry-run
```

低层脚本仍然保留，适合直接拿一份已有 `run artifact` 重新同步：

```bash
python3 "/Users/liming/AI Project/codex-force-claw/scripts/sync_dify_cycle_to_feishu.py" \
  --run-json "/Users/liming/AI Project/codex-force-claw/output/dify-runs/<run_id>.json"
```

## 一次性授权捕获

第一次需要把 Dify 和飞书登录态保存成 Playwright storage state：

```bash
python3 "/Users/liming/AI Project/codex-force-claw/scripts/sync_dify_cycle_to_feishu.py" \
  --bootstrap-auth
```

执行后会打开两个页面：

- `http://154.9.254.79:8090/apps`
- `https://h52xu4gwob.feishu.cn/wiki/UCFJwrGYJiOk52k1NYFcPkIon9b`

你只需要：

- 确认两个页面都已登录
- 回到终端按一次回车

脚本会把登录态保存到：

- `output/auth/dify_feishu_storage_state.json`

之后默认不需要重复登录，除非会话过期。

## 写入目标

高层脚本最终固定追加到这 4 张表：

- `闭环总览`
- `选题候选`
- `脚本包`
- `反馈复盘`

其中：

- `闭环总览` 每轮 `1` 行
- `选题候选` 每轮 `3` 行
- `脚本包` 每轮 `1` 行
- `反馈复盘` 每轮 `1` 行

## 去重与失败关闭

高层收口和低层写表都不是盲写：

- 缺任何阶段文件，直接失败
- 阶段文件之间 `run_id` 不一致，直接失败
- 缺 `feedback_record` 或 `feedback_analysis`，直接失败
- 如果某张表里该 `run_id` 已经存在完整行数，就直接跳过
- 如果只存在部分行数，脚本会直接报错并停止，不会继续补写造成重复

这是故意的 fail-closed 策略。

## 本地审计账

每次同步完成后，会把结果记到：

- `output/feishu-sync/sync-ledger.json`

这个 ledger 只是公开工作账，方便你和我回看什么时候同步过哪些 `run_id`。
飞书多维表本身仍然是真实主账。

## 最小验收

建议每次跑完至少看三件事：

1. `闭环总览` 里出现新的 `run_id`
2. `选题候选` 对应新增 `3` 行
3. `反馈复盘` 里平台和指标没有被改写

## 当前边界

- 这版已经把“我执行一轮后自动收口并追加飞书”固化了
- 所以现在的固定工作流是：
  - `Dify 阶段结果 -> cycle folder -> run artifact -> 飞书追加`

不是：

- `外部触发 -> 自动跑 Dify -> 自动发布 -> 自动抓数 -> 自动回写`
