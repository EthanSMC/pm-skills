---
name: pm-workflow
description: PM 工作流总控入口 — 唯一用户入口，内部调度所有子 skill。支持阶段跳转和门控确认。
---

# PM 工作流

用户唯一入口。内部调度 pm-knowledge → pm-brainstorming → write-prd → prototyping 等子 skill。

## 调用方式

```
/pm-workflow [任务描述]                  → 默认从阶段0开始全流程
/pm-workflow 从需求探索开始 [任务描述]     → 跳到阶段1
/pm-workflow 直接写PRD                   → 跳到阶段2
/pm-workflow 原型验证                    → 跳到阶段3
/pm-workflow 继续                        → 从上次中断的阶段恢复
```

自然语言也支持路由：用户说"帮我整理一下知识"、"讨论一下需求"、"写PRD"、"做原型"等，路由机制自动解析到对应阶段。

## 路由机制

### 路由解析

收到用户输入后，解析意图定位目标阶段：

| 用户表达 | 目标阶段 | 前置条件检查 |
|---------|---------|------------|
| [任务描述]（无阶段关键词） | 阶段0 | 无 |
| "整理知识/摄入文档" | 阶段0 | 无 |
| "从需求探索/脑暴开始" | 阶段1 | .pm-wiki/ 中是否有知识摘要 |
| "讨论需求/设计" | 阶段1 | .pm-wiki/ 中是否有知识摘要 |
| "直接写PRD" | 阶段2 | docs/pm/specs/ 中是否有设计文档 |
| "原型验证/做原型" | 阶段3 | docs/pm/prds/ 中是否有PRD |
| "继续/恢复" | 上次中断阶段 | 检查已有产出判断进度 |

### 前置条件补足

目标阶段的前置条件不满足时：
- 向用户说明缺失什么产出物
- 自动从缺失阶段开始补起
- 例：用户说"直接写PRD"但没有设计文档 → 从阶段1开始，告知用户

### 阶段恢复

检查已有产出文件判断当前进度：

| 产出物存在 | 对应阶段已完成 |
|-----------|--------------|
| `.pm-wiki/` 有内容且不是空壳 | 阶段0 |
| `docs/pm/specs/` 有设计文档 | 阶段1 |
| `docs/pm/prds/` 有PRD | 阶段2 |
| `docs/prototype/` 有原型产出 | 阶段3（进行中） |

找到最近的已完成阶段，从下一阶段恢复。

## 阶段门控

每个阶段完成后执行门控流程，**不可跳过**：

### 门控三步

1. **汇报**：展示该阶段产出
   - 列出新增/修改的文件路径
   - 用2-3句总结关键产出内容
   - 标注知识库新增条目

2. **决策点**：向用户提问（必须等待用户明确回复）：

   > "阶段 X 已完成。接下来：
   > - **继续** → 进入下一阶段
   > - **跳过下一阶段** → 跳到更后面的阶段（需说明理由）
   > - **回退** → 回到上一阶段修改
   > - **结束** → 保留当前产出，工作流结束"

3. **确认后执行**：只有用户明确回复后才进入下一阶段。不回复 = 停止。

### 特殊门控

- **阶段 2→3 门控**（PRD 完成后）：保持现有设计 — 明确问用户是否进入原型验证，"否"则工作流结束
- **阶段 3 子阶段门控**：由 prototyping skill 内部管理，pm-workflow 不干预

## 阶段定义

### 阶段 0: 知识准备

**内联检查**（调用 pm-knowledge 前执行）：

1. 检查 `<project>/raw/` 是否存在，不存在则创建
2. 检查 `.pm-wiki/_generated/raw-manifest.md` 是否存在，不存在则创建
3. 执行 Raw Discovery：扫描项目中的散落文档文件，向用户呈现候选列表确认
4. 对比 manifest 与实际 `raw/` 目录，发现 pending/changed 文件 → 标记为需要摄入

**调度**：使用 Skill 工具调用 `pm-knowledge`

**交接参数**：

| 参数 | 值 |
|------|------|
| 输入 | 用户任务描述 + raw/ 目录状态 + manifest 变化检测结果 |
| 输出 | 知识摘要（传递给阶段1） |
| 知识写回 | .pm-wiki/ 各子目录 + raw-manifest 更新 |

**特殊情况**：如果用户有多份PRD/需求文档需要合并，使用 Skill 工具调用 `prd-reconcile`

**门控汇报内容**：
- 知识库新增条目列表
- 知识摘要要点（3-5条关键发现）
- 知识缺口说明

### 阶段 0a: 多文档合并（按需）

**触发条件**：用户有多份PRD/需求文档需要合并

**调度**：使用 Skill 工具调用 `prd-reconcile`

**交接参数**：

| 参数 | 值 |
|------|------|
| 输入 | 需合并的文档列表 |
| 输出 | 合并后的全局PRD + 完整度报告 |
| 知识写回 | synthesis/ + decisions/ |

### 阶段 1: 需求探索

**调度**：使用 Skill 工具调用 `pm-brainstorming`

**交接参数**：

| 参数 | 值 |
|------|------|
| 输入 | 阶段0的知识摘要 + 用户任务描述 |
| 输出 | 设计文档（docs/pm/specs/）+ 设计决策（.pm-wiki/decisions/） |
| 知识写回 | decisions/ + log.md |

**门控汇报内容**：
- 设计文档路径
- 设计方案要点（核心功能、关键交互）
- 重要决策及替代方案（WHY NOT）

### 阶段 2: 撰写 PRD

**调度**：使用 Skill 工具调用 `write-prd`

**交接参数**：

| 参数 | 值 |
|------|------|
| 输入 | 设计文档（docs/pm/specs/） |
| 输出 | PRD（docs/pm/prds/） |
| 知识写回 | requirements/ |

**门控汇报内容**：
- PRD 文件路径
- 功能需求表摘要（功能名 + 优先级）
- 验收标准概览

**特殊决策点**：

> "PRD 已完成并保存到 `docs/pm/prds/<filename>.md`。是否需要创建原型来验证设计方案？
> - **是** → 进入阶段 3（原型验证）
> - **否** → 工作流结束，PRD 即为最终交付物"

只有用户回复"是"才进入阶段 3。

### 阶段 3: 原型验证（可选）

**调度**：使用 Skill 工具调用 `prototyping`

**交接参数**：

| 参数 | 值 |
|------|------|
| 输入 | PRD（docs/pm/prds/） |
| 输出 | 技术规格 + 实施计划 + 骨架代码 + scaffold-index.md |
| 知识写回 | decisions/ + constraints/ + _working/ + log.md + synthesis/ |

prototyping 内部调度 pm-writing-plans、pm-executing-plans、pm-verification、pm-branch-management 等子 skill，pm-workflow 不干预子阶段门控。

**阶段 3 完成后**：门控汇报 prototyping 总产出，然后工作流结束。

## 知识沉淀（各阶段各自负责）

| 阶段 | 写入路径 | 内容 |
|------|---------|------|
| pm-knowledge | .pm-wiki/ 各子目录 | 知识摘要 + raw manifest |
| prd-reconcile | synthesis/ + decisions/ | 冲突分析 + 决策记录 + 完整度报告 |
| pm-brainstorming | decisions/ + log.md | 设计决策 + 工作日志 |
| write-prd | requirements/ | 功能需求摘要 + 优先级 |
| prototyping (技术规格) | decisions/ + constraints/ | 架构决策 + 新约束 |
| prototyping (前端设计) | decisions/ + constraints/ + _working/ | UI 设计决策 + 交互约束 + 设计资源 |
| prototyping (实施计划) | decisions/ + constraints/ | 计划中的决策 + 约束 |
| prototyping (骨架构建) | constraints/ + _working/ + decisions/ | 新约束 + 临时笔记 + 执行决策 |
| prototyping (审查) | synthesis/ | 问题模式、成功经验 |
| prototyping (验证) | log.md | 验证结果记录 |
| prototyping (分支管理) | log.md + synthesis/ | 工作流摘要 + 成功经验 |

## 知识库目录

项目知识库位于 `<project>/.pm-wiki/`，原始文档位于 `<project>/raw/`。

**核心目录**（工作流自动创建）：
- `context/` — 项目背景、目标、干系人
- `requirements/` — 需求文档、用户故事
- `constraints/` — 技术/业务约束、假设
- `decisions/` — 产品决策记录
- `raw/` — 知识摄入队列（进入即摄入，参见 pm-knowledge Raw 管理）

**按需创建**（相关场景触发时创建）：
- `market/` — 市场/行业数据（用户提到市场分析时）
- `competitors/` — 竞品分析（用户提到竞品时）
- `users/` — 用户研究（用户提供用户调研时）
- `synthesis/` — 综合分析（review 发现模式时）
- `references/` — 链接到个人知识库（需要跨项目引用时）

## 知识流

```
[文档/URL/文件] → pm-knowledge.ingest → wiki
                                            ↓
用户提问 → pm-knowledge.query → 三流检索 → 知识摘要 → pm-brainstorming → 设计决策 → decisions/
                                                          ↓
                                                    write-prd → PRD → requirements/
                                                          ↓
                                                [门控决策: 是否原型验证?]
                                                 ↓ (是)                ↓ (否)
                                         prototyping → 原型产出       工作流结束

多份PRD → prd-reconcile → 冲突分析 → 决策 → 全局PRD → requirements/
```

## References（子 skill 索引）

pm-workflow 是唯一用户入口，以下子 skill 位于 `references/` 目录中，由 pm-workflow 或其子 skill 自动调度：

**直接调度（references/）**：

| 子 skill | 阶段 | 说明 |
|---------|------|------|
| pm-knowledge | 阶段0 | 知识摄入、检索、组织 |
| prd-reconcile | 阶段0a（按需） | 多份PRD/需求文档合并与消歧 |
| pm-brainstorming | 阶段1 | 需求探索与设计 |
| write-prd | 阶段2 | PRD 撰写（增量，不重复 spec） |
| prototyping | 阶段3（可选） | 原型验证（内部调度7个子 skill） |
| pm-personalize | 按需 | 从项目库提炼通用知识到个人库 |
| visual-companion | 阶段1内部 | 浏览器端可视化辅助 |

**prototyping 内部调度（references/prototyping/references/）**：

| 子 skill | 子阶段 | 说明 |
|---------|--------|------|
| pm-writing-plans | 3.2 | 实施计划编写（TDD 铁律 + 无占位符） |
| pm-tdd | 3.2/3.3 内部 | 测试驱动开发（Iron Law、合理化防御） |
| pm-executing-plans | 3.3 | 骨架构建（逐步骤、阻塞即停） |
| pm-frontend-design | 3.1.5（可选） | 前端设计（UI组件/视觉/交互） |
| pm-verification | 3.5 | 验证门控（证据先行、5步门控） |
| pm-branch-management | 3.6 | 分支收尾（环境检测、4/3选项） |
| pm-using-worktrees | 3.2/3.3 内部 | 工作树管理（隔离工作空间） |