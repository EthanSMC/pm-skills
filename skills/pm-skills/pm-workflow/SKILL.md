---
name: pm-workflow
description: PM 工作流 - 从知识摄入到需求分析到 PRD，可选原型验证
---

# PM 工作流 Plugin

组合 pm-knowledge + prd-reconcile + pm-brainstorming + write-prd 的产品经理工作流。PRD 完成后可选进入原型验证阶段 (prototyping)。

## 工作流步骤

当用户调用 `/pm-workflow` 时，按以下顺序执行：

### 阶段 0: 知识准备 (pm-knowledge)

**初始化检查**：
- 执行 `qmd --version` 验证工具可用性
- 如不可用，降级为文件系统检索模式

**常规流程**：
- 检索项目知识库和全局知识库中的相关知识
- 识别知识缺口
- 如有新文档需要摄入，执行 ingest 流程
- 输出知识摘要，作为 pm-brainstorming 的输入

**特殊情况**：如果用户有多份PRD/需求文档需要合并，调用 prd-reconcile skill 执行冲突分析和合并。

### 阶段 1: 需求探索 (pm-brainstorming)

调用 pm-brainstorming skill 进行需求分析和探索：
- **前置**：接收 pm-knowledge 输出的知识摘要
- 理解用户意图，收集功能需求，探索设计选项
- **后置**：
  - 将设计决策写入 `.pm-wiki/decisions/<主题>.md`
  - 在 `.pm-wiki/log.md` 中记录摘要

### 阶段 2: 撰写 PRD (write-prd)

调用 write-prd skill 将设计转化为产品需求文档：
- **前置**：pm-brainstorming 设计文档已通过审核（位于 `docs/pm/specs/`）
- PRD 只写 spec 中**没有**的内容：功能需求表、验收标准、优先级、非功能需求
- 背景、用户、场景等已有信息用一句话引用 spec
- **后置**：将功能需求摘要写入 `.pm-wiki/requirements/<主题>.md`

### 阶段 2 完成：PRD 交付

PRD 审核通过后，向用户提问：

> "PRD 已完成并保存到 `docs/pm/prds/<filename>.md`。是否需要创建原型来验证设计方案？
>
> - **是** — 进入原型验证阶段 (prototyping)，产出技术规格、实施计划和骨架代码
> - **否** — 工作流结束，PRD 即为最终交付物"

等待用户明确回复。只有用户回复"是"时才进入阶段 3。

### 阶段 3: 原型验证 (prototyping) — 可选

**仅在用户明确选择后进入此阶段。**

调用 prototyping skill，基于 PRD 创建原型：
- 子阶段 3.1: 技术规格 — 从 PRD 衍生接口定义、数据模型、API 契约
- 子阶段 3.2: 实施计划 — 创建 bite-sized TDD 任务规划（供未来完整实现使用）
- 子阶段 3.3: 骨架构建 — 生成脚手架、空接口、mock 数据（可运行但不完整）
- 子阶段 3.4: 审查 — 检查原型与 PRD 的一致性
- 子阶段 3.5: 验证 — 证据先行，确认骨架可编译/运行/走通关键场景
- 子阶段 3.6: 分支管理 — 提供 merge/PR/keep/discard 选项

原型产出保存到 `docs/prototype/<feature>/`，包含 spec.md、plan.md、scaffold-index.md。

### 知识沉淀（各阶段各自负责）

不需要独立的"知识回写"阶段，每个阶段负责写自己的知识：

| 阶段 | 写入路径 | 内容 |
|------|---------|------|
| prd-reconcile | `synthesis/` + `decisions/` | 冲突分析 + 决策记录 |
| pm-brainstorming | `decisions/` | 设计决策（WHY/WHAT/WHY NOT） |
| write-prd | `requirements/` | 功能需求摘要 + 优先级 |
| prototyping (技术规格) | `decisions/` + `constraints/` | 架构决策 + 新约束 |
| prototyping (实施计划) | `decisions/` + `constraints/` | 计划中的决策 + 约束 |
| prototyping (骨架构建) | `constraints/` + `_working/` | 新发现的约束/假设 + 临时笔记 |
| prototyping (审查) | `synthesis/` | 问题模式、成功经验 |
| prototyping (验证) | `log.md` | 验证结果记录 |
| prototyping (分支管理) | `log.md` + `synthesis/` | 工作流摘要 + 成功经验 |

所有阶段完成后，在 `.pm-wiki/log.md` 中记录本次工作流摘要。

## 知识库目录

项目知识库位于 `<project>/.pm-wiki/`，原始文档位于 `<project>/raw/`。

**核心目录**（工作流自动创建）：
- `context/` — 项目背景、目标、干系人
- `requirements/` — 需求文档、用户故事
- `constraints/` — 技术/业务约束、假设
- `decisions/` — 产品决策记录
- `raw/` — 原始文档（PDF/DOCX/PPTX/MD）

**按需创建**（相关场景触发时创建）：
- `market/` — 市场/行业数据（用户提到市场分析时）
- `competitors/` — 竞品分析（用户提到竞品时）
- `users/` — 用户研究（用户提供用户调研时）
- `synthesis/` — 综合分析（review 发现模式时）
- `references/` — 链接到个人知识库（需要跨项目引用时）

## 使用方式

```
/pm-workflow [任务描述]
```

## 知识流

```
[文档/URL/文件] → pm-knowledge.ingest → wiki
                                            ↓
用户提问 → pm-knowledge.query → 三流检索(BM25+Vector+Graph) → 知识摘要 → pm-brainstorming → 设计决策 → decisions/
                                                          ↓
                                                    write-prd → PRD → requirements/
                                                          ↓
                                                [用户选择: 是否原型验证?]
                                                 ↓ (是)                ↓ (否)
                                         prototyping → 原型产出       工作流结束

多份PRD → prd-reconcile → 冲突分析 → 决策 → 全局PRD → requirements/
```
