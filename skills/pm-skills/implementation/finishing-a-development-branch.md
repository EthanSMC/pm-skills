---
name: finishing-a-development-branch
description: "收尾分支 — 实施完成、测试通过后，引导工作收尾。验证测试→检测环境→呈现4选项→执行选择→清理。Make sure to use this skill when implementation is complete and you need to decide how to integrate the work — merge, PR, or cleanup."
---

# Finishing a Development Branch — 收尾分支

引导开发工作完成：验证测试 → 检测环境 → 提供选项 → 执行选择 → 清理。

**核心流程：验证测试 → 检测环境 → 提供选项 → 执行选择 → 清理。**

## Step 1: 验证测试

**在提供选项之前，确认测试通过：**

```bash
# 运行项目测试套件
npm test / cargo test / pytest / go test ./...
```

**如果测试失败：**
```
测试失败（<N>个失败）。必须修复才能继续：

[显示失败]

测试通过前不能继续 merge/PR。
```

停止。不进入 Step 2。

**如果测试通过：** 继续 Step 2。

## Step 2: 检测环境

**确定workspace状态：**

```bash
GIT_DIR=$(cd "$(git rev-parse --git-dir)" 2>/dev/null && pwd -P)
GIT_COMMON=$(cd "$(git rev-parse --git-common-dir)" 2>/dev/null && pwd -P)
```

| 状态 | 菜单 | 清理 |
|------|------|------|
| `GIT_DIR == GIT_COMMON`（普通repo） | 标准4选项 | 无worktree需清理 |
| `GIT_DIR != GIT_COMMON`，有命名分支 | 标准4选项 | 按来源处理 |
| `GIT_DIR != GIT_COMMON`，detached HEAD | 3选项（无merge） | 不清理（外部管理） |

## Step 3: 确定基准分支

```bash
git merge-base HEAD main 2>/dev/null || git merge-base HEAD master 2>/dev/null
```

或询问："这个分支从 main 分出来的——对吗？"

## Step 4: 提供选项

**普通repo和命名分支worktree — 精确提供这4个选项：**

```
实施完成。你想怎么做？

1. 合并回 <base-branch>（本地合并）
2. 推送并创建 Pull Request
3. 保持分支现状（你自己处理）
4. 丢弃这次工作

选哪个？
```

**Detached HEAD — 提供这3个选项：**

```
实施完成。你在 detached HEAD（外部管理的workspace）。

1. 推送为新分支并创建 Pull Request
2. 保持现状（你自己处理）
3. 丢弃这次工作

选哪个？
```

**不加解释** — 保持选项简洁。

## Step 5: 执行选择

### 选项 1：本地合并

```bash
# 合并先——验证成功再清理
git checkout <base-branch>
git pull
git merge <feature-branch>

# 验证合并后的测试
<test command>
```

合并成功后：清理worktree（Step 6），删除分支。

```bash
git branch -d <feature-branch>
```

### 选项 2：推送并创建PR

```bash
git push -u origin <feature-branch>

# 创建PR
gh pr create --title "<title>" --body "$(cat <<'EOF'
## Summary
<2-3条变更要点>

## Test Plan
- [ ] <验证步骤>
EOF
)"
```

**不清理worktree** — 用户需要它来迭代PR反馈。

### 选项 3：保持现状

报告："保持分支 <name>。Worktree保留在 <path>。"

**不清理worktree。**

### 选项 4：丢弃

**先确认：**
```
这将永久删除：
- 分支 <name>
- 所有commits: <commit-list>
- Worktree在 <path>

输入 'discard' 确认。
```

等待精确确认。确认后清理worktree（Step 6），强制删除分支。

```bash
git branch -D <feature-branch>
```

## Step 6: 清理Workspace

**仅对选项1和4执行。** 选项2和3永远保留worktree。

```bash
GIT_DIR=$(cd "$(git rev-parse --git-dir)" 2>/dev/null && pwd -P)
GIT_COMMON=$(cd "$(git rev-parse --git-common-dir)" 2>/dev/null && pwd -P)
```

**如果 `GIT_DIR == GIT_COMMON`：** 普通repo，无worktree需清理。完成。

**如果是worktree：** 清理worktree并修剪。

```bash
# 切回主repo根目录
cd <main-repo-root>
git worktree remove <worktree-path>
git worktree prune
```

## 快速参考

| 选项 | 合并 | 推送 | 保留Worktree | 清理分支 |
|------|------|------|-------------|---------|
| 1. 本地合并 | yes | - | - | yes |
| 2. 创建PR | - | yes | yes | - |
| 3. 保持现状 | - | - | yes | - |
| 4. 丢弃 | - | - | - | yes (force) |

## 常见错误

- **跳过测试验证** — 合入坏代码、创建失败PR → 始终验证
- **开放性问题** — "接下来做什么？"太模糊 → 提供精确4选项
- **选项2清理worktree** — 用户需要迭代PR → 只对选项1和4清理
- **先删分支再删worktree** — `git branch -d`会失败 → 先合并，移除worktree，再删分支
- **在worktree内运行remove** — 命令静默失败 → 先切到主repo根目录
- **丢弃无确认** — 意外删除工作 → 要求输入'discard'确认

## 红旗

**永远不要：**
- 测试失败时继续
- 不验证就合并
- 不确认就删除工作
- 未经请求force-push
- 合并成功前移除worktree
- 清理不是你创建的worktree
- 在worktree内运行 `git worktree remove`

**永远要：**
- 提供选项前验证测试
- 提供选项前检测环境
- 提供精确4选项（或detached HEAD 3选项）
- 选项4要求输入确认
- 仅选项1和4清理worktree
- 移除worktree前切到主repo根目录
- 移除后运行 `git worktree prune`

## 与 pm-knowledge 的衔接

收尾完成后：
- 写入 `.pm-wiki/log.md` 记录工作流摘要
- 写入 `.pm-wiki/synthesis/` 记录问题模式和成功经验