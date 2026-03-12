# Deployment Checklist

## Context

- `project_name`: `feishu-short-video-growth-mvp`
- `workflow_name`: `原力创业短视频增长MVP`
- `deployment_mode`: `python-service`

## Preflight

- [ ] tenant and app owner are confirmed
- [ ] required Feishu surfaces are confirmed
- [ ] permissions are enumerated
- [ ] runtime owner is named
- [ ] rollback owner is named

## App Setup

- [ ] internal custom app exists
- [ ] app credentials are stored in a secret manager or secure env
- [ ] message, Bitable, approval, task, doc, or calendar scopes match the workflow plan
- [ ] callback or long-connection approach is chosen and documented

## Runtime

- [ ] runtime environment exists
- [ ] `.env` values are set
- [ ] `/health` returns success
- [ ] event or callback endpoint is reachable if used

## Validation

- [ ] controlled test input executed
- [ ] target Feishu object is visible
- [ ] read-after-write or re-list verification passes
- [ ] notification reached the target person or chat

## Rollback

- [ ] disable switch is documented
- [ ] event subscription or scheduler can be paused
- [ ] operator knows how to stop the service

## Acceptance

- [ ] completion evidence is satisfied
- [ ] blockers are empty or explicitly accepted
