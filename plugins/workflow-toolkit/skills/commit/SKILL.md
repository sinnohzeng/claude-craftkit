---
name: commit
description: >
  Use when all changes are ready to be committed and pushed to remote.
  Handles staging, Chinese conventional commit message, SemVer tagging when applicable, and push.
argument-hint: "[额外说明，如：只提交前端改动]"
disable-model-invocation: true
allowed-tools: Bash(git status:*), Bash(git add:*), Bash(git diff:*), Bash(git commit:*), Bash(git tag:*), Bash(git push:*), Bash(git log:*)
---

## Context

- Git status: !`git status`
- Staged and unstaged diff: !`git diff HEAD`
- Current branch: !`git branch --show-current`
- Recent commits: !`git log --oneline -10`
- Existing tags: !`git tag --sort=-v:refname | head -5`

## Task

提交本次改动到远端仓库，在单条消息中完成 stage → commit → push 全流程。

### Commit Message 规范

- 中文撰写，遵循 Conventional Commits：`<type>(<scope>): <subject>`
- type: feat / fix / refactor / docs / chore / perf / test / ci / style
- 正文说明动机、改动范围、影响面
- 必要时附 BREAKING CHANGE 与关联 issue

### 版本与标签

- 如涉及对外接口变更或里程碑发布，按 SemVer 升版本号并打 git tag
- 日常改动无需打 tag，除非 $ARGUMENTS 明确要求

### 工作流

- 独立开发者项目直接提交主分支，无需 PR
- Stage 相关文件（不要 `git add -A`，逐文件确认）
- 不提交 `.env`、credentials、secrets 等敏感文件

## Output

完成后输出：
- Branch: <分支名>
- Commit: <hash> <标题行>
- Tag: <tag>（如有）
- Push: OK / FAIL

$ARGUMENTS
