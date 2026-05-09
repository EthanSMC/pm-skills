---
name: writing-plans
description: "实施规划 — 基于设计文档创建详细的实施计划。分解为bite-sized TDD任务，无占位符，每步有完整代码和验证命令。Make sure to use this skill whenever you have a spec or design document ready for implementation, before writing any code — even if you think 'this is simple enough to just start coding'."
---

# Writing Plans — 实施规划

基于已审核的设计文档，创建详细的实施计划。假设执行者对你的项目没有上下文、对工具不熟悉——每个任务包含精确文件路径、完整代码、验证命令。

## 前置条件

- brainstorming skill 已完成，设计文档已通过用户审核
- 设计文档位于 `docs/pm/specs/YYYY-MM-DD-<topic>-design.md`

**保存计划到：** `docs/pm/plans/YYYY-MM-DD-<feature-name>.md`

## 范围检查

如果 spec 覆盖多个独立子系统，建议拆成多个计划——每个计划产出可独立测试的工作软件。

## 文件结构

在定义任务之前，先列出所有要创建/修改的文件及职责：

- 每个文件应有单一明确职责，接口定义清晰
- 小而聚焦的文件优于大而杂的文件——你能同时hold在上下文里的代码更可靠
- 一起变化的文件应该放在一起——按职责分，不按技术层分
- 在已有代码库中遵循已有模式，不要擅自重构

## Bite-Sized 任务粒度

**每个步骤是一个动作（2-5分钟）：**
- "写失败测试" — 一个步骤
- "运行确认它失败" — 一个步骤
- "写最小实现让测试通过" — 一个步骤
- "运行确认测试通过" — 一个步骤
- "提交" — 一个步骤

## 计划文档头部

**每个计划必须以这个头部开始：**

```markdown
# [Feature Name] Implementation Plan

**Goal:** [一句话描述构建什么]

**Architecture:** [2-3句描述方法]

**Tech Stack:** [关键技术/库]

---
```

## 任务结构

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

## 无占位符规则

每个步骤必须包含执行者需要的实际内容。以下都是**计划失败**——绝对不写：

- "TBD", "TODO", "implement later", "fill in details"
- "Add appropriate error handling" / "add validation" / "handle edge cases"
- "Write tests for the above"（不附带实际测试代码）
- "Similar to Task N"（必须重复代码——执行者可能按非顺序阅读）
- 只描述做什么不展示怎么做（代码步骤必须有代码块）
- 引用未在任何任务中定义的类型、函数或方法

## 自审

写完计划后，用全新眼光重新审视：

1. **Spec覆盖**：逐一扫描spec每个section/需求——能指出实现它的任务吗？列出缺口。
2. **占位符扫描**：搜索上面的红标模式，修复。
3. **类型一致性**：后面任务中用的类型、方法签名、属性名是否与前面任务中定义的一致？Task 3中叫 `clearLayers()` 但 Task 7中叫 `clearFullLayers()` 就是bug。

发现问题直接修复。spec需求没有对应任务？添加任务。

## 执行交接

保存计划后，提供执行选择：

**"计划完成并保存到 `docs/pm/plans/<filename>.md`。两种执行方式：**

**1. 逐任务执行** — 按顺序执行每个任务，checkpoint检查

**2. 按当前节奏执行** — 继续在当前session中逐步实现

**选择哪种？"**

## 与 pm-knowledge 的衔接

规划完成后：
- 将实施计划的关键架构决策写入 `.pm-wiki/decisions/`
- 新发现的约束写入 `.pm-wiki/constraints/`
- 在 `.pm-wiki/log.md` 中记录规划活动

## 使用 TodoWrite 跟踪进度

为每个任务创建 todo 条目。状态：pending → in_progress → completed

## 关键原则

- **精确文件路径** — 总是给出完整路径
- **每步完整代码** — 如果步骤修改代码，展示代码
- **精确命令+预期输出** — 每个验证步骤都有
- **DRY, YAGNI, TDD, frequent commits**
- **无占位符** — 每步都有实际内容，不能"后面再补"