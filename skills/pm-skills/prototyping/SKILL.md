---
name: prototyping
description: "原型构建 — 基于 PRD 创建技术规格、实施计划和骨架代码（接口定义、脚手架、mock 数据）。验证架构可行性，不追求完整实现。Make sure to use this skill after PRD is approved and you want to validate the design through a working prototype."
---

# Prototyping — 原型构建

基于已审核的 PRD，创建原型来验证设计方案。产出三件套：技术规格、实施计划、骨架代码。目标是验证架构可行性，不追求完整实现。

**核心区分：原型是走通架构的骨架，不是可部署的生产代码。**

## 产出目录

所有原型产出保存到 `docs/prototype/<feature-name>/`：

```
docs/prototype/<feature-name>/
  ├── spec.md              ← 技术规格（接口、数据模型、API契约）
  ├── ui-spec.md           ← UI 规格（仅前端原型时产出）
  ├── plan.md              ← 实施计划（bite-sized TDD任务，供未来完整实现使用）
  └── scaffold-index.md    ← 骨架代码索引（哪些源码文件是stub/mock/scaffold）
```

骨架代码的源码文件放在项目源码目录中，scaffold-index.md 记录清单。

## 子阶段总览

| 子阶段 | 名称 | 方式 | 使用的 Skill |
|--------|------|------|------------|
| 1 | 技术规格 | 内联 | 无（PM 专属：PRD→spec 翻译） |
| 1.5 | 前端设计 | **REQUIRED SUB-SKILL（可选）** | `pm-frontend-design`（仅前端原型时） |
| 2 | 实施计划 | **REQUIRED SUB-SKILL** | `pm-writing-plans`（内部引用 `pm-tdd`） |
| 3 | 骨架构建 | **REQUIRED SUB-SKILL** | `pm-executing-plans` |
| 4 | 审查 | 内联 | 无（原型专属审查） |
| 5 | 验证 | **REQUIRED SUB-SKILL** | `pm-verification` |
| 6 | 分支管理 | **REQUIRED SUB-SKILL** | `pm-branch-management` |

子阶段 1、4 是 PM 专属工作，保留内联指令。子阶段 2、3、5、6 托给专门的 pm- skill，由各 skill 的 Iron Law、合理化防御表、红旗清单等机制保证执行纪律。子阶段 1.5 仅在原型涉及前端 UI 时执行。

---

## 子阶段 1：技术规格（内联）

从 PRD 衍生技术层面的规格文档。不是重新写需求，是把产品需求翻译成技术语言。

### 输入
- 已审核的 PRD（`docs/pm/prds/<filename>.md`）

### 输出
- `docs/prototype/<feature>/spec.md`

### spec.md 结构

```markdown
# <Feature Name> Technical Spec

**Goal:** [从PRD]
**Architecture:** [2-3句描述方法]
**Tech Stack:** [关键技术/库]

---

## Interfaces
[接口定义：函数签名、输入输出类型]

## Data Models
[实体定义：字段、关系、约束]

## API Contracts
[端点定义：路径、请求/响应schema]

## Component Boundaries
[哪些文件负责哪些职责]

## Mock Data Strategy
[什么数据需要mock，mock数据放哪里]
```

### 自审
写完 spec 后：
1. **PRD覆盖** — 每个PRD功能需求都有对应接口？列缺口。
2. **占位符扫描** — 无TBD/TODO/"implement later"。
3. **类型一致性** — 接口定义的数据类型前后一致。

### 知识写回
- 架构决策 → `.pm-wiki/decisions/`
- 新约束 → `.pm-wiki/constraints/`

---

## 子阶段 1.5：前端设计（REQUIRED SUB-SKILL（可选）→ pm-frontend-design）

仅当原型涉及前端 UI 时执行。后端纯 API 原型跳过此阶段。

### 判断标准

是否需要前端设计？以下任一为真则执行：
- PRD 包含用户界面需求（页面、组件、交互）
- 技术规格 (spec.md) 的 Component Boundaries 包含 UI 组件
- 原型需要可交互的界面来验证用户体验

### 交接参数

| 参数 | 值 |
|------|------|
| **Input** | `docs/prototype/<feature>/spec.md`（子阶段 1 产出）+ PRD 中 UI 相关描述 |
| **Output** | `docs/prototype/<feature>/ui-spec.md` |
| **PM 上下文** | 原型 scope：产出组件骨架 + CSS 变量定义 + 关键页面完整设计，不是生产级组件库 |
| **知识写回** | UI 设计决策 → `.pm-wiki/decisions/`，交互约束 → `.pm-wiki/constraints/`，设计资源 → `.pm-wiki/_working/` |

### 交接声明

```
我正在使用 pm-frontend-design skill 来设计这个原型的前端界面。

输入：docs/prototype/<feature>/spec.md + PRD UI 描述
输出：docs/prototype/<feature>/ui-spec.md

原型上下文：产出组件骨架 + CSS 变量 + 关键页面完整设计，不是生产级组件库。
```

### 对后续子阶段的影响

- **子阶段 2 (pm-writing-plans)**：实施计划应参考 ui-spec.md，将前端组件拆为 bite-sized TDD 任务，任务中包含 CSS 变量定义和组件骨架构建
- **子阶段 3 (pm-executing-plans)**：骨架构建时遵循 ui-spec.md 的视觉系统和交互模式
- **子阶段 4 (审查)**：审查维度增加「UI 设计一致性」检查

---

## 子阶段 2：实施计划（REQUIRED SUB-SKILL → pm-writing-plans）

委托给 `pm-writing-plans` skill 执行。该 skill 包含完整的执行纪律：scope check、bite-sized 粒度、无占位符铁律、自审清单、执行交接选项。

### 交接参数

| 参数 | 值 |
|------|---|
| **Input Spec** | `docs/prototype/<feature>/spec.md`（子阶段 1 产出） |
| **Output** | `docs/prototype/<feature>/plan.md` |
| **PM 上下文** | 原型 scope：GREEN 阶段产出 stub/mock returns，不是生产实现 |
| **知识写回** | 架构决策 → `.pm-wiki/decisions/`，新约束 → `.pm-wiki/constraints/` |

### 交接声明

```
我正在使用 pm-writing-plans skill 来编写这个原型的实施计划。

输入：docs/prototype/<feature>/spec.md
输出：docs/prototype/<feature>/plan.md

原型上下文：minimal implementation = stub/mock returns，不是生产逻辑。
```

### 执行后交接

pm-writing-plans 完成后会提供执行选项。在原型 scope 内推荐 Inline Execution（`pm-executing-plans`），因为原型任务量较小。

---

## 子阶段 3：骨架构建（REQUIRED SUB-SKILL → pm-executing-plans）

委托给 `pm-executing-plans` skill 执行。该 skill 包含完整的执行纪律：计划预审、逐步骤执行、验证不跳过、阻塞即停。

### 交接参数

| 参数 | 值 |
|------|------||
| **Input Plan** | `docs/prototype/<feature>/plan.md`（子阶段 2 产出） |
| **Output** | 项目源码目录中的骨架文件 + `docs/prototype/<feature>/scaffold-index.md` |
| **PM 上下文** | 原型 scope：任务产出 stubs/mocks/scaffolds，不是生产实现 |
| **知识写回** | 新约束 → `.pm-wiki/constraints/`，临时笔记 → `.pm-wiki/_working/`，执行决策 → `.pm-wiki/decisions/` |

### 骨架原则（pm-executing-plans 执行时需遵循）

| 优先 | 不优先 |
|------|--------|
| 接口定义 | 接口实现 |
| mock数据返回 | 真实数据查询 |
| 路由/scaffold | 完整业务逻辑 |
| 类型定义 | 运行时校验 |
| 可编译/可运行 | 生产级质量 |

每个函数体要么是：
- stub 返回 mock 数据：`return MOCK_DATA[request.id]`
- 空接口 + TODO标记（供未来实现）
- scaffold 可编译运行但不做实质工作

骨架必须可编译/可运行，这样才能走通关键场景验证架构。

### scaffold-index.md 格式

```markdown
# <Feature Name> Scaffold Index

## Created Files
| File | Path | Type | Description |
|------|------|------|-------------|
| user-service.ts | src/services/user-service.ts | stub | Interface + mock returns |
| user-model.ts | src/models/user-model.ts | scaffold | Type definitions |

## Walk-through Scenarios
| Scenario | Entry Point | Mock Data | Verified? |
|----------|-------------|-----------|-----------|
| User login | POST /auth/login | mock-users.ts | pending |
```

### 交接声明

```
我正在使用 pm-executing-plans skill 来执行这个原型的实施计划。

输入：docs/prototype/<feature>/plan.md
输出：骨架代码 + docs/prototype/<feature>/scaffold-index.md

原型上下文：任务产出 stubs/mocks/scaffolds，不是生产实现。
骨架原则：接口定义优先，mock数据返回优先，可编译可运行优先。
```

---

## 子阶段 4：审查（内联）

原型视角的审查，不是生产代码审查。关注原型与PRD的一致性和接口完整性。

### 审查维度

1. **PRD一致性** — 每个PRD需求都有对应stub？
2. **接口完整性** — 接口定义是否覆盖所有关键场景？
3. **Mock数据覆盖度** — mock数据是否够走通所有关键场景？
4. **代码质量** — stub不冗余，接口定义清晰
5. **安全性** — 标记为"原型暂不处理"即可，但需记录到plan中

### 强制审查循环

审查发现问题 → 修复 → **重新审查**（不是一次通过就完）：

- 发现严重问题 → 必须修复后重新审查
- 发现建议级问题 → 修复或记录到 plan，重新审查确认
- 重新审查仍发现问题 → 继续修复→审查循环，直到通过

### 审查报告格式

```
## 原型审查报告

**审查范围**: <骨架文件列表>
**对照PRD**: <PRD路径>
**审查轮次**: 第 N 轮

### 通过项
- ✅ ...

### 问题项
- ❌ [严重] <问题描述> → <修复建议>
- ⚠️ [建议] <问题描述> → <改进建议>
```

### 审查通过标准

- 0个严重问题
- PRD需求100%有对应stub
- 关键场景可走通

### 知识写回
- 问题模式 → `.pm-wiki/synthesis/`

---

## 子阶段 5：验证（REQUIRED SUB-SKILL → pm-verification）

委托给 `pm-verification` skill 执行。该 skill 包含完整的 Iron Law："NO COMPLETION CLAIMS WITHOUT FRESH VERIFICATION EVIDENCE"、5步门控函数、合理化防御表、常见失败对照表。

### 交接参数

| 参数 | 值 |
|------|------|
| **验证目标** | 原型专属（见下表） |
| **PM 上下文** | 验证原型可编译、可运行、可走通场景，不是验证生产代码 |
| **知识写回** | 验证结果 → `.pm-wiki/log.md` |

### 原型专属验证目标

| 声明 | 需要的证据 |
|------|----------|
| 骨架可编译 | 构建命令：exit 0 |
| 骨架可运行 | 启动命令：无崩溃 |
| 关键场景可走通 | 每个场景的运行输出 |
| PRD需求有对应stub | 逐条对照清单 |

这些验证目标会被 pm-verification skill 的 Common Failures 表和 Key Patterns 覆盖。

### 交接声明

```
我正在使用 pm-verification skill 来验证这个原型。

验证目标：骨架可编译、可运行、关键场景可走通、PRD需求有对应stub。
原型上下文：验证原型骨架，不是验证生产代码。
```

---

## 子阶段 6：分支管理（REQUIRED SUB-SKILL → pm-branch-management）

委托给 `pm-branch-management` skill 执行。该 skill 包含完整的操作手册：环境检测、4/3选项菜单、具体bash命令、provenance清理逻辑、typed确认机制、7 Never + 7 Always 红旗清单。

### 交接参数

| 参数 | 值 |
|------|------|
| **前提** | pm-verification 已确认原型通过 |
| **PM 上下文** | 特性分支包含骨架/stub代码，不是生产实现；合并决策需评估原型是否 ready for production |
| **知识写回** | 工作流摘要 → `.pm-wiki/log.md`，经验教训 → `.pm-wiki/synthesis/` |

### 交接声明

```
我正在使用 pm-branch-management skill 来完成这个原型分支。

前提：pm-verification 已确认原型通过。
原型上下文：分支包含骨架/stub代码，合并决策需评估是否 ready for production。
```

### 各选项的知识写回

| 选项 | 知识写回 |
|------|---------|
| 1. 本地合并 | `.pm-wiki/log.md` + `.pm-wiki/synthesis/` |
| 2. 推送+PR | `.pm-wiki/log.md` |
| 3. 保持现状 | 无 |
| 4. 丢弃 | 无 |

---

## 知识写回汇总

| 子阶段 | 写回路径 | 内容 |
|--------|---------|------|
| 技术规格 | `decisions/` + `constraints/` | 架构决策 + 新约束 |
| 前端设计 | `decisions/` + `constraints/` + `_working/` | UI 设计决策 + 交互约束 + 设计资源 |
| 实施计划 | `decisions/` + `constraints/` | 计划中的决策 + 约束 |
| 骨架构建 | `constraints/` + `_working/` + `decisions/` | 新约束 + 临时笔记 + 执行决策 |
| 审查 | `synthesis/` | 问题模式、成功经验 |
| 验证 | `log.md` | 验证结果记录 |
| 分支管理 | `log.md` + `synthesis/` | 工作流摘要 + 成功经验 |