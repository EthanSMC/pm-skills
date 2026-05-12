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
  ├── plan.md              ← 实施计划（bite-sized TDD任务，供未来完整实现使用）
  └── scaffold-index.md    ← 骨架代码索引（哪些源码文件是stub/mock/scaffold）
```

骨架代码的源码文件放在项目源码目录中，scaffold-index.md 记录清单。

## 子阶段 1：技术规格

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

## 子阶段 2：实施计划

为未来完整实现创建 bite-sized TDD 任务规划。原型本身是骨架，plan 是描述怎么从骨架到完整实现。

### 输入
- spec.md（子阶段 1 产出）

### 输出
- `docs/prototype/<feature>/plan.md`

### 计划文档头部

```markdown
# [Feature Name] Implementation Plan

**Goal:** [一句话描述构建什么]

**Architecture:** [2-3句描述方法]

**Tech Stack:** [关键技术/库]

---
```

### Bite-Sized 任务粒度

每个步骤是一个动作（2-5分钟）：
- "写失败测试" — 一个步骤
- "运行确认失败" — 一个步骤
- "写最小实现让测试通过" — 一个步骤
- "运行确认通过" — 一个步骤
- "提交" — 一个步骤

### 无占位符规则

每个步骤必须包含实际内容。以下都是**计划失败**：
- "TBD", "TODO", "implement later"
- "Add appropriate error handling" / "handle edge cases"
- "Write tests for the above"（不附实际测试代码）
- "Similar to Task N"（必须重复代码）
- 引用未在任何任务中定义的类型、函数或方法

### 知识写回
- 架构决策 → `.pm-wiki/decisions/`
- 新约束 → `.pm-wiki/constraints/`

---

## 子阶段 3：骨架构建

基于计划生成骨架代码。不是完整实现，是可以走通的骨架。

### 输入
- plan.md（子阶段 2 产出）

### 输出
- 项目源码目录中的骨架文件
- `docs/prototype/<feature>/scaffold-index.md`

### 骨架原则

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

### 执行原则

1. 按顺序执行计划中的任务
2. 一个任务一个提交
3. 遇到问题时：计划有误→暂停讨论；新需求→记录不实施；阻碍→尝试替代

### 知识写回
- 新约束 → `.pm-wiki/constraints/`
- 临时笔记 → `.pm-wiki/_working/`

---

## 子阶段 4：审查

原型视角的审查，不是生产代码审查。关注原型与PRD的一致性和接口完整性。

### 审查维度

1. **PRD一致性** — 每个PRD需求都有对应stub？
2. **接口完整性** — 接口定义是否覆盖所有关键场景？
3. **Mock数据覆盖度** — mock数据是否够走通所有关键场景？
4. **代码质量** — stub不冗余，接口定义清晰
5. **安全性** — 标记为"原型暂不处理"即可，但需记录到plan中

### 审查报告格式

```
## 原型审查报告

**审查范围**: <骨架文件列表>
**对照PRD**: <PRD路径>

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

## 子阶段 5：验证

证据先行，永远如此。验证目标是原型特有的。

### 验证目标

| 声明 | 需要的证据 |
|------|----------|
| 骨架可编译 | 构建命令：exit 0 |
| 骨架可运行 | 启动命令：无崩溃 |
| 关键场景可走通 | 每个场景的运行输出 |
| PRD需求有对应stub | 逐条对照清单 |

### 门控函数

```
1. 识别：什么命令能证明这个声明？
2. 运行：执行完整命令（新鲜的）
3. 读取：完整输出，检查退出码
4. 验证：输出是否确认了声明？
   - 如果否：用证据陈述实际状态
   - 如果是：用证据声明
5. 只有然后：才能做出声明
```

### 红旗

- 使用"应该"、"大概"、"看起来"
- 验证之前表达满意
- 准备提交但没有验证

### 知识写回
- 验证结果 → `.pm-wiki/log.md`

---

## 子阶段 6：分支管理

验证通过后，引导原型分支收尾。

### 流程

1. 确认验证通过（不可跳过）
2. 检测环境（普通repo / worktree / detached HEAD）
3. 提供精确选项：
   - 普通repo/worktree：4选项（本地合并 / PR / 保持 / 丢弃）
   - detached HEAD：3选项（PR / 保持 / 丢弃）
4. 执行选择
5. 清理worktree（仅选项1和4）

### 红旗

- 测试失败时继续
- 不验证就合并
- 不确认就删除工作
- 未经请求force-push

### 知识写回
- 工作流摘要 → `.pm-wiki/log.md`
- 成功经验 → `.pm-wiki/synthesis/`

---

## 知识写回汇总

| 子阶段 | 写回路径 | 内容 |
|--------|---------|------|
| 技术规格 | `decisions/` + `constraints/` | 架构决策 + 新约束 |
| 实施计划 | `decisions/` + `constraints/` | 计划中的决策 + 约束 |
| 骨架构建 | `constraints/` + `_working/` | 新发现的约束 + 临时笔记 |
| 审查 | `synthesis/` | 问题模式、成功经验 |
| 验证 | `log.md` | 验证结果记录 |
| 分支管理 | `log.md` + `synthesis/` | 工作流摘要 + 成功经验 |