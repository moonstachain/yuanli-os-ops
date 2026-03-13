# Environment Checklist

## GitHub

- `gh auth status` shows an active account
- `repo` scope is available
- private repo access for `yuanli-os-ops` is confirmed
- private repo access for `yuanli-os-skills-pack` is confirmed

## Codex

- `$CODEX_HOME` is set or defaults to `~/.codex`
- `ai-da-guan-jia` exists under `$CODEX_HOME/skills`
- `os-yuanli` exists under `$CODEX_HOME/skills`
- the private method organs exist under `$CODEX_HOME/skills`
  - `intent-grounding`
  - `skill-router`
  - `jiyao-youyao-haiyao-zaiyao`
  - `evidence-gate`
  - `closure-evolution`

## Remote Control

- the target Mac has `Remote Login` enabled
- the target Mac has `Screen Sharing` or `Remote Management` enabled
- the source machine can reach the target Mac over the LAN by hostname or static IP

## Feishu

- `~/.openclaw/openclaw.json` contains the target Feishu account
- app id and app secret are present for the account used by the bridge
- the target base link opens in the logged-in browser session

## Content And Growth Chain

- `wechat-style-profiler`
- `wechat-topic-outline-planner`
- `wechat-draft-writer`
- `wechat-title-generator`
- `wechat-article-writer`

## Research And Audit Chain

- `feishu-reader`
- `openai-docs`
- `pdf`
- `spreadsheet`

## Do Not Copy

- browser cookies
- auth storage dumps
- `.codex` as a full folder mirror
- noisy runtime outputs without stable contracts
