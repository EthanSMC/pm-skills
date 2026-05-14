---
name: pm-writing-plans
description: PM 实施计划编写 — 基于 PRD 技术规格编写 bite-sized TDD 实施计划。在 prototyping 子阶段 2 使用。
---

# Writing Plans (PM Adaptation)

## Overview

Write comprehensive implementation plans assuming the engineer has zero context for our codebase and questionable taste. Document everything they need to know: which files to touch for each task, code, testing, docs they might need to check, how to test it. Give them the whole plan as bite-sized tasks. DRY. YAGNI. TDD. Frequent commits.

Assume they are a skilled developer, but know almost nothing about our toolset or problem domain. Assume they don't know good test design very well.

**In prototype scope, "minimal implementation" means stub/mock returns for scaffold code, not production-ready implementations. The TDD cycle still applies but GREEN phase produces stubs.**

**Announce at start:** "I'm using the pm-writing-plans skill to create the implementation plan for this prototype."

**Context:** If working in an isolated worktree, it should have been created via the `pm-using-worktrees` skill at execution time.

**Save plans to:** `docs/prototype/<feature>/plan.md`
- (User preferences for plan location override this default)

**Knowledge write-back:**
- Architecture decisions discovered during planning → `.pm-wiki/decisions/`
- New constraints discovered during planning → `.pm-wiki/constraints/`

## PM Pipeline Context

This skill is used in **prototyping Sub-phase 2** — implementation plan writing. It runs **after** the prototype technical specification (`docs/prototype/<feature>/spec.md`) has been created in **Sub-phase 1** by the `prototyping` skill. The spec.md input is derived from the PRD through the prototyping skill's Sub-phase 1 analysis.

**Pipeline position:**
```
pm-workflow → pm-brainstorming → write-prd → prototyping
  ├── Sub-phase 1: spec.md (input for this skill)
  └── Sub-phase 2: plan.md (output of this skill) ← YOU ARE HERE
  └── Sub-phase 3: scaffold code execution
```

**Input:** `docs/prototype/<feature>/spec.md` — the technical specification produced by prototyping Sub-phase 1.

**Output:** `docs/prototype/<feature>/plan.md` — the bite-sized TDD implementation plan this skill produces.

## Scope Check

If the spec covers multiple independent subsystems, it should have been broken into sub-project specs during brainstorming. If it wasn't, suggest breaking this into separate plans — one per subsystem. Each plan should produce working, testable software on its own.

## File Structure

Before defining tasks, map out which files will be created or modified and what each one is responsible for. This is where decomposition decisions get locked in.

- Design units with clear boundaries and well-defined interfaces. Each file should have one clear responsibility.
- You reason best about code you can hold in context at once, and your edits are more reliable when files are focused. Prefer smaller, focused files over large ones.
- Files that change together should live together. Split by responsibility, not by technical layer.
- In existing codebases, follow established patterns. If the codebase uses large files, don't unilaterally restructure - but if a file you're modifying has grown unwieldy, including a split in the plan is reasonable.

**Knowledge write-back:** After mapping the file structure, write any architectural decomposition decisions to `.pm-wiki/decisions/` — e.g., why a file was split, which module owns which responsibility, interface boundary choices.

This structure informs the task decomposition. Each task should produce self-contained changes that make sense independently.

## Bite-Sized Task Granularity

**Each step is one action (2-5 minutes):**
- "Write the failing test" - step
- "Run it to make sure it fails" - step
- "Implement the minimal code to make the test pass" - step (prototype: stub/mock return is acceptable)
- "Run the tests and make sure they pass" - step
- "Commit" - step

## Plan Document Header

**Every plan MUST start with this header:**

```markdown
# [Feature Name] Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use planned: pm-subagent-driven-development (recommended) or pm-executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** [One sentence describing what this builds]

**Architecture:** [2-3 sentences about approach]

**Tech Stack:** [Key technologies/libraries]

**Input Spec:** `docs/prototype/<feature>/spec.md`

---
```

## Task Structure

````markdown
### Task N: [Component Name]

**Files:**
- Create: `exact/path/to/file.py`
- Modify: `exact/path/to/existing.py:123-145`
- Test: `tests/exact/path/to/test.py`

- [ ] **Step 1: Write the failing test**

```python
def test_specific_behavior():
    result = function(input)
    assert result == expected
```

- [ ] **Step 2: Run test to verify it fails**

Run: `pytest tests/path/test.py::test_name -v`
Expected: FAIL with "function not defined"

- [ ] **Step 3: Write minimal implementation**

```python
def function(input):
    return expected
```

- [ ] **Step 4: Run test to verify it passes**

Run: `pytest tests/path/test.py::test_name -v`
Expected: PASS

- [ ] **Step 5: Commit**

```bash
git add tests/path/test.py src/path/file.py
git commit -m "feat: add specific feature"
```
````

**Knowledge write-back:** At each task boundary where a significant design decision is made (e.g., choosing a data structure, defining an interface contract, deciding on a stub strategy), write the decision to `.pm-wiki/decisions/`. At each task boundary where a new constraint is discovered (e.g., a library limitation, a platform requirement, a dependency version lock), write it to `.pm-wiki/constraints/`.

## No Placeholders

Every step must contain the actual content an engineer needs. These are **plan failures** — never write them:
- "TBD", "TODO", "implement later", "fill in details"
- "Add appropriate error handling" / "add validation" / "handle edge cases"
- "Write tests for the above" (without actual test code)
- "Similar to Task N" (repeat the code — the engineer may be reading tasks out of order)
- Steps that describe what to do without showing how (code blocks required for code steps)
- References to types, functions, or methods not defined in any task

## Remember
- Exact file paths always
- Complete code in every step — if a step changes code, show the code
- Exact commands with expected output
- DRY, YAGNI, TDD, frequent commits
- Prototype stubs are acceptable GREEN-phase implementations
- Write architecture decisions → `.pm-wiki/decisions/`
- Write new constraints → `.pm-wiki/constraints/`

## Self-Review

After writing the complete plan, look at the spec with fresh eyes and check the plan against it. This is a checklist you run yourself — not a subagent dispatch.

**1. Spec coverage:** Skim each section/requirement in the spec. Can you point to a task that implements it? List any gaps.

**2. Placeholder scan:** Search your plan for red flags — any of the patterns from the "No Placeholders" section above. Fix them.

**3. Type consistency:** Do the types, method signatures, and property names you used in later tasks match what you defined in earlier tasks? A function called `clearLayers()` in Task 3 but `clearFullLayers()` in Task 7 is a bug.

If you find issues, fix them inline. No need to re-review — just fix and move on. If you find a spec requirement with no task, add the task.

## Execution Handoff

After saving the plan, offer execution choice:

**"Plan complete and saved to `docs/prototype/<feature>/plan.md`. Two execution options:**

**1. Subagent-Driven (recommended)** - I dispatch a fresh subagent per task, review between tasks, fast iteration

**2. Inline Execution** - Execute tasks in this session using pm-executing-plans, batch execution with checkpoints

**Which approach?"**

**If Subagent-Driven chosen:**
- **REQUIRED SUB-SKILL:** Use planned: pm-subagent-driven-development
- Fresh subagent per task + two-stage review

**If Inline Execution chosen:**
- **REQUIRED SUB-SKILL:** Use pm-executing-plans
- Batch execution with checkpoints for review