---
name: pm-branch-management
description: "分支收尾（内部子 skill，由 prototyping 调度）— 环境检测、4/3选项菜单、provenance 清理"
---

# PM Branch Management

## Overview

Guide completion of prototype development work by presenting clear options and handling chosen workflow.

**Core principle:** Verify tests → Detect environment → Present options → Execute choice → Clean up.

**Announce at start:** "I'm using the pm-branch-management skill to complete this prototype branch."

In prototype context, the feature branch contains scaffold/stub code, not production implementations. Merge decisions should consider whether the prototype is ready for production or needs further implementation.

## 当由 prototyping 调度时

prototyping 在子阶段 6（分支管理）使用 Skill 工具调用此 skill。

### 交接参数

| 参数 | 值 |
|------|------|
| **前提** | pm-verification 已确认原型通过 |
| **PM 上下文** | 特性分支包含骨架/stub代码，合并决策需评估原型是否 ready for production |
| **知识写回** | .pm-wiki/log.md + .pm-wiki/synthesis/ |

### 交接声明

```
我正在使用 pm-branch-management skill 来完成这个原型分支。

前提：pm-verification 已确认原型通过。
原型上下文：分支包含骨架/stub代码，合并决策需评估是否 ready for production。
```

## PM Pipeline Context

This skill is used in **prototyping Sub-phase 6 (收尾)** of the PM workflow. It is invoked after pm-verification (Sub-phase 5) confirms the prototype passes all verification gates. It handles the final step of the prototyping workflow -- deciding how to integrate the prototype branch.

**Prerequisite:** pm-verification has confirmed all prototype claims (compilation, runtime, walkthrough, PRD coverage) with fresh evidence.

**Sub-phase flow:**
- **Sub-phase 1** (pm-brainstorming): Requirements exploration and design
- **Sub-phase 2** (pm-writing-plans): Creates the implementation plan
- **Sub-phase 3** (pm-executing-plans): Executes the plan to build scaffold code
- **Sub-phase 4** (pm-tdd): TDD-driven refinement of stubs
- **Sub-phase 5** (pm-verification): Verify all prototype claims with evidence
- **Sub-phase 6** (pm-branch-management): **This skill** -- finalize and integrate the branch

## The Process

### Step 1: Verify Tests

**Before presenting options, verify tests pass:**

```bash
# Run project's test suite
npm test / cargo test / pytest / go test ./...
```

**If tests fail:**
```
Tests failing (<N> failures). Must fix before completing:

[Show failures]

Cannot proceed with merge/PR until tests pass.
```

Stop. Don't proceed to Step 2.

**If tests pass:** Continue to Step 2.

### Step 2: Detect Environment

**Determine workspace state before presenting options:**

```bash
GIT_DIR=$(cd "$(git rev-parse --git-dir)" 2>/dev/null && pwd -P)
GIT_COMMON=$(cd "$(git rev-parse --git-common-dir)" 2>/dev/null && pwd -P)
```

This determines which menu to show and how cleanup works:

| State | Menu | Cleanup |
|-------|------|---------|
| `GIT_DIR == GIT_COMMON` (normal repo) | Standard 4 options | No worktree to clean up |
| `GIT_DIR != GIT_COMMON`, named branch | Standard 4 options | Provenance-based (see Step 6) |
| `GIT_DIR != GIT_COMMON`, detached HEAD | Reduced 3 options (no merge) | No cleanup (externally managed) |

### Step 3: Determine Base Branch

```bash
# Try common base branches
git merge-base HEAD main 2>/dev/null || git merge-base HEAD master 2>/dev/null
```

Or ask: "This branch split from main - is that correct?"

### Step 4: Present Options

**Normal repo and named-branch worktree — present exactly these 4 options:**

```
Implementation complete. What would you like to do?

1. Merge back to <base-branch> locally
2. Push and create a Pull Request
3. Keep the branch as-is (I'll handle it later)
4. Discard this work

Which option?
```

**Detached HEAD — present exactly these 3 options:**

```
Implementation complete. You're on a detached HEAD (externally managed workspace).

1. Push as new branch and create a Pull Request
2. Keep as-is (I'll handle it later)
3. Discard this work

Which option?
```

**Don't add explanation** - keep options concise.

### Step 5: Execute Choice

#### Option 1: Merge Locally

```bash
# Get main repo root for CWD safety
MAIN_ROOT=$(git -C "$(git rev-parse --git-common-dir)/.." rev-parse --show-toplevel)
cd "$MAIN_ROOT"

# Merge first — verify success before removing anything
git checkout <base-branch>
git pull
git merge <feature-branch>

# Verify tests on merged result
<test command>

# Only after merge succeeds: cleanup worktree (Step 6), then delete branch
```

Then: Cleanup worktree (Step 6), then delete branch:

```bash
git branch -d <feature-branch>
```

**Knowledge write-back:** Write workflow summary to `.pm-wiki/log.md` and lessons to `.pm-wiki/synthesis/`.

#### Option 2: Push and Create PR

```bash
# Push branch
git push -u origin <feature-branch>

# Create PR
gh pr create --title "<title>" --body "$(cat <<'EOF'
## Summary
<2-3 bullets of what changed>

## Test Plan
- [ ] <verification steps>
EOF
)"
```

**Do NOT clean up worktree** — user needs it alive to iterate on PR feedback.

**Knowledge write-back:** Write workflow summary to `.pm-wiki/log.md`.

#### Option 3: Keep As-Is

Report: "Keeping branch <name>. Worktree preserved at <path>."

**Don't cleanup worktree.**

No knowledge write-back needed.

#### Option 4: Discard

**Confirm first:**
```
This will permanently delete:
- Branch <name>
- All commits: <commit-list>
- Worktree at <path>

Type 'discard' to confirm.
```

Wait for exact confirmation.

If confirmed:
```bash
MAIN_ROOT=$(git -C "$(git rev-parse --git-common-dir)/.." rev-parse --show-toplevel)
cd "$MAIN_ROOT"
```

Then: Cleanup worktree (Step 6), then force-delete branch:
```bash
git branch -D <feature-branch>
```

No knowledge write-back needed (work is discarded).

### Step 6: Cleanup Workspace

**Only runs for Options 1 and 4.** Options 2 and 3 always preserve the worktree.

```bash
GIT_DIR=$(cd "$(git rev-parse --git-dir)" 2>/dev/null && pwd -P)
GIT_COMMON=$(cd "$(git rev-parse --git-common-dir)" 2>/dev/null && pwd -P)
WORKTREE_PATH=$(git rev-parse --show-toplevel)
```

**If `GIT_DIR == GIT_COMMON`:** Normal repo, no worktree to clean up. Done.

**If worktree path is under `.worktrees/`, `worktrees/`, `~/.config/superpowers/worktrees/`, or `~/.config/pm-skills/worktrees/`:** Superpowers or PM Skills created this worktree — we own cleanup.

```bash
MAIN_ROOT=$(git -C "$(git rev-parse --git-common-dir)/.." rev-parse --show-toplevel)
cd "$MAIN_ROOT"
git worktree remove "$WORKTREE_PATH"
git worktree prune  # Self-healing: clean up any stale registrations
```

**Otherwise:** The host environment (harness) owns this workspace. Do NOT remove it. If your platform provides a workspace-exit tool, use it. Otherwise, leave the workspace in place.

## Knowledge Write-Back

### Workflow Summary → `.pm-wiki/log.md`

When knowledge write-back is triggered (per Option in Step 5), record a timestamped entry including:
- Which branch management option was chosen
- Branch name and base branch
- Worktree path (if applicable)
- Outcome (merged, PR created, kept, or discarded)

### Lessons Learned → `.pm-wiki/synthesis/`

When Option 1 (Merge) is chosen, also extract lessons to `.pm-wiki/synthesis/`:
- Prototype readiness assessment (production-ready or needs further work)
- Merge conflicts encountered and resolution patterns
- Verification outcomes from the merged result

## Quick Reference

| Option | Merge | Push | Keep Worktree | Cleanup Branch |
|--------|-------|------|---------------|----------------|
| 1. Merge locally | yes | - | - | yes |
| 2. Create PR | - | yes | yes | - |
| 3. Keep as-is | - | - | yes | - |
| 4. Discard | - | - | - | yes (force) |

## Common Mistakes

**Skipping test verification**
- **Problem:** Merge broken code, create failing PR
- **Fix:** Always verify tests before offering options

**Open-ended questions**
- **Problem:** "What should I do next?" is ambiguous
- **Fix:** Present exactly 4 structured options (or 3 for detached HEAD)

**Cleaning up worktree for Option 2**
- **Problem:** Remove worktree user needs for PR iteration
- **Fix:** Only cleanup for Options 1 and 4

**Deleting branch before removing worktree**
- **Problem:** `git branch -d` fails because worktree still references the branch
- **Fix:** Merge first, remove worktree, then delete branch

**Running git worktree remove from inside the worktree**
- **Problem:** Command fails silently when CWD is inside the worktree being removed
- **Fix:** Always `cd` to main repo root before `git worktree remove`

**Cleaning up harness-owned worktrees**
- **Problem:** Removing a worktree the harness created causes phantom state
- **Fix:** Only clean up worktrees under `.worktrees/`, `worktrees/`, `~/.config/superpowers/worktrees/`, or `~/.config/pm-skills/worktrees/`

**No confirmation for discard**
- **Problem:** Accidentally delete work
- **Fix:** Require typed "discard" confirmation

## Red Flags

**Never:**
- Proceed with failing tests
- Merge without verifying tests on result
- Delete work without confirmation
- Force-push without explicit request
- Remove a worktree before confirming merge success
- Clean up worktrees you didn't create (provenance check)
- Run `git worktree remove` from inside the worktree

**Always:**
- Verify tests before offering options
- Detect environment before presenting menu
- Present exactly 4 options (or 3 for detached HEAD)
- Get typed confirmation for Option 4
- Clean up worktree for Options 1 & 4 only
- `cd` to main repo root before worktree removal
- Run `git worktree prune` after removal