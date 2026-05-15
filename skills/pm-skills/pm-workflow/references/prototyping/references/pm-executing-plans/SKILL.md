---
name: pm-executing-plans
description: 计划执行（内部子 skill，由 prototyping 调度）— 逐步骤执行、阻塞即停、验证不跳过
---

# PM Executing Plans

## 当由 prototyping 调度时

prototyping 在子阶段 3（骨架构建）使用 Skill 工具调用此 skill。

### 交接参数

| 参数 | 值 |
|------|------|
| **Input Plan** | docs/prototype/<feature>/plan.md（子阶段 2 产出） |
| **Output** | 骨架代码 + docs/prototype/<feature>/scaffold-index.md |
| **PM 上下文** | 原型 scope：任务产出 stubs/mocks/scaffolds，不是生产实现。骨架原则：接口定义优先，mock数据返回优先，可编译可运行优先。 |
| **知识写回** | .pm-wiki/constraints/ + .pm-wiki/_working/ + .pm-wiki/decisions/ |

### 交接声明

```
我正在使用 pm-executing-plans skill 来执行这个原型的实施计划。

输入：docs/prototype/<feature>/plan.md
输出：骨架代码 + docs/prototype/<feature>/scaffold-index.md

原型上下文：任务产出 stubs/mocks/scaffolds，不是生产实现。
骨架原则：接口定义优先，mock数据返回优先，可编译可运行优先。
```

## Overview

Load plan, review critically, execute all tasks, report when complete.

**Announce at start:** "I'm using the pm-executing-plans skill to execute the implementation plan for this prototype."

In prototype scope, tasks create stubs/mocks/scaffolds, not production implementations. "Follow each step exactly" still applies -- but GREEN phase produces stubs, not full implementations.

**Note:** Tell your human partner that PM Skills works much better with access to subagents. The quality of its work will be significantly higher if run on a platform with subagent support (such as Claude Code or Codex). If subagents are available, use **planned: pm-subagent-driven-development** instead of this skill.

## PM Pipeline Context

This skill operates within the **prototyping** sub-phase flow:

- **Sub-phase 1** (pm-brainstorming): Requirements exploration and design
- **Sub-phase 2** (pm-writing-plans): Creates the implementation plan
- **Sub-phase 3** (pm-executing-plans): **This skill** -- executes the plan to build scaffold code

**Input:** `docs/prototype/<feature>/plan.md` (produced by pm-writing-plans in Sub-phase 2)

**Output:** Scaffold code in project source directories + `docs/prototype/<feature>/scaffold-index.md`

## The Process

### Step 1: Load and Review Plan

1. Read plan file (`docs/prototype/<feature>/plan.md`)
2. Review critically -- identify any questions or concerns about the plan
3. If concerns: Raise them with your human partner before starting
4. If no concerns: Create TodoWrite and proceed

### Step 2: Execute Tasks

For each task:
1. Mark as in_progress
2. Follow each step exactly (plan has bite-sized steps)
3. Run verifications as specified
4. Mark as completed

During execution, write back discovered knowledge:
- **New constraints discovered** --> `.pm-wiki/constraints/`
- **Temporary notes** --> `.pm-wiki/_working/`
- **Execution decisions** --> `.pm-wiki/decisions/`

### Step 3: Complete Development

After all tasks complete and verified:
- Announce: "I'm using the pm-branch-management skill to complete this prototype branch."
- **REQUIRED SUB-SKILL:** Use pm-branch-management
- Follow that skill to verify tests, present options, execute choice

## When to Stop and Ask for Help

**STOP executing immediately when:**
- Hit a blocker (missing dependency, test fails, instruction unclear)
- Plan has critical gaps preventing starting
- You don't understand an instruction
- Verification fails repeatedly

**Ask for clarification rather than guessing.**

## When to Revisit Earlier Steps

**Return to Review (Step 1) when:**
- Partner updates the plan based on your feedback
- Fundamental approach needs rethinking

**Don't force through blockers** -- stop and ask.

## Remember

- Review plan critically first
- Follow plan steps exactly
- Don't skip verifications
- Reference skills when plan says to
- Stop when blocked, don't guess
- Write back knowledge to `.pm-wiki/` as you discover it
- Never start implementation on main/master branch without explicit user consent

## Integration

**Required PM workflow skills:**
- **pm-using-worktrees** -- Ensures isolated workspace (creates one or verifies existing)
- **pm-writing-plans** -- Creates the plan this skill executes
- **pm-branch-management** -- Complete development after all tasks