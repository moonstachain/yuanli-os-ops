# 原力OS Feishu 审计样例

This directory keeps one successful sample bundle for the 原力OS audit-to-Feishu flow.

## Purpose

- show the expected output shape
- provide a real payload reference for target-machine bring-up
- preserve one evidence-bearing sample without treating Feishu as canonical truth

## Current Sample

- `yuanli-audit-feishu-v1`
  - first successful apply bundle
  - includes bundle payload, score tables, gap tables, action tables, and sync result

## Provenance Rule

Some records in this sample intentionally retain source-machine paths as historical provenance.

Treat those paths as evidence of origin, not as runnable target-machine paths.
