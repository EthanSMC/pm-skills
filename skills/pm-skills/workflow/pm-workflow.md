---
name: pm-workflow
description: 完整的 PM 工作流 - 从知识摄入到需求分析到代码审查
---

# PM 工作流 Plugin

组合 pm-knowledge + brainstorming + write-prd + 实施 + review 的完整产品经理工作流。

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
- 输出知识摘要，作为 brainstorming 的输入

### 阶段 1: 需求探索 (brainstorming)

调用 brainstorming skill 进行需求分析和探索：
- **前置**：接收 pm-knowledge 输出的知识摘要
- 理解用户意图，收集功能需求，探索设计选项
- **后置**：
  - 将设计决策写入 `.project-wiki/decisions/<主题>.md`
  - 在 `.project-wiki/log.md` 中记录摘要

### 阶段 2: 撰写 PRD (write-prd)

调用 write-prd skill 将设计转化为产品需求文档：
- **前置**：brainstorming 设计文档已通过审核（位于 `docs/superpowers/specs/`）
- PRD 只写 spec 中**没有**的内容：功能需求表、验收标准、优先级、非功能需求
- 背景、用户、场景等已有信息用一句话引用 spec
- **后置**：将功能需求摘要写入 `.project-wiki/requirements/<主题>.md`

### 阶段 3: 实施规划

将设计拆解为可执行的实施计划：
- 读取设计文档和 PRD，识别实施单元
- 每个单元可独立理解和测试
- 确定依赖关系，规划实施顺序
- 为每个任务定义验收标准
- 使用 TodoWrite 工具跟踪任务进度

### 阶段 4: 代码实施

按实施计划逐步执行：
- 一个任务一个焦点，一个提交
- 边写边测，保持简洁
- 遵循项目现有模式和风格
- 遇到问题时：计划有误→暂停讨论；新需求→记录不实施；技术阻碍→尝试替代方案

### 阶段 5: 代码审查 (Review)

调用 review skill：
- 对照设计文档检查一致性
- 代码质量、安全性、测试覆盖
- 输出审查报告，严重问题立即修复

### 知识沉淀（各阶段各自负责）

不需要独立的"知识回写"阶段，每个阶段负责写自己的知识：

| 阶段 | 写入路径 | 内容 |
|------|---------|------|
| brainstorming | `decisions/` | 设计决策（WHY/WHAT/WHY NOT） |
| write-prd | `requirements/` | 功能需求摘要 + 优先级 |
| 实施中 | `constraints/` | 新发现的约束/假设 |
| review | `synthesis/` | 问题模式、成功经验 |

所有阶段完成后，在 `.project-wiki/log.md` 中记录本次工作流摘要。

## 知识库目录

项目知识库位于 `<project>/.project-wiki/`，原始文档位于 `<project>/raw/`。

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
用户提问 → pm-knowledge.query → 知识摘要 → brainstorming → 设计决策 → decisions/
                                                          ↓
                                                    write-prd → PRD → requirements/
                                                          ↓
                                              规划 → 实施 → review → synthesis/
```
