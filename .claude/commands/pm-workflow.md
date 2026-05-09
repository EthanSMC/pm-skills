---
name: pm-workflow
description: 完整的 PM 工作流 - 从知识摄入到需求分析到代码审查
---

# PM 工作流 Plugin

组合 pm-knowledge + prd-reconcile + brainstorming + write-prd + writing-plans + execute + review + verification + finishing 的完整产品经理工作流。

## 工作流步骤

当用户调用 `/pm-workflow` 时，按以下顺序执行：

### 阶段 0: 知识准备 (pm-knowledge)
首先调用 pm-knowledge skill 建立知识基础：
- 检索项目知识库和全局知识库中的相关知识
- 识别知识缺口
- 如有新文档需要摄入，执行 ingest 流程
- 输出知识摘要，作为 brainstorming 的输入

**特殊情况**：如果用户有多份PRD/需求文档需要合并，调用 prd-reconcile skill 执行冲突分析和合并。

### 阶段 1: 需求探索 (brainstorming)
调用 brainstorming skill 进行需求分析和探索：
- **前置**：接收 pm-knowledge 输出的知识摘要
- 理解用户意图，收集功能需求，探索设计选项
- **后置**：
  - 将设计决策写入 `.pm-wiki/decisions/<主题>.md`
  - 在 `.pm-wiki/log.md` 中记录摘要

### 阶段 2: 撰写 PRD (write-prd)
调用 write-prd skill 将设计转化为产品需求文档：
- **前置**：brainstorming 设计文档已通过审核
- PRD 只写 spec 中**没有**的内容：功能需求表、验收标准、优先级、非功能需求
- **后置**：将功能需求摘要写入 `.pm-wiki/requirements/<主题>.md`

### 阶段 3: 实施规划 (writing-plans)
调用 writing-plans skill 创建详细的bite-sized实施计划：
- 读取设计文档和 PRD，识别实施单元
- 每个单元2-5分钟，TDD步骤
- 无占位符规则——每步必须有完整代码和验证命令
- 使用 TodoWrite 工具跟踪任务进度

### 阶段 4: 代码实施 (execute)
按实施计划逐步执行：
- 一个任务一个焦点，一个提交
- 边写边测，保持简洁
- 遵循项目现有模式和风格

### 阶段 5: 代码审查 (review)
调用 review skill：
- 对照设计文档检查一致性
- 代码质量、安全性、测试覆盖
- 输出审查报告，严重问题立即修复

### 阶段 6: 验证先行 (verification-before-completion)
**在任何完成声明之前**：
- 运行验证命令，读取输出
- 证据先行，不信任口头声明
- 逐条验证验收标准

### 阶段 7: 收尾分支 (finishing-a-development-branch)
验证通过后，引导工作收尾：
- 确认测试全部通过
- 提供4选项：本地合并 / 推送PR / 保持 / 丢弃
- 执行选择并清理

## 使用方式

```
/pm-workflow [任务描述]
```

## 配置

此工作流组合了以下 skills：
- pm-knowledge: 知识摄入、检索、组织
- prd-reconcile: 多文档合并与消歧
- brainstorming: 需求探索与设计
- write-prd: PRD 撰写
- writing-plans: 实施规划（bite-sized TDD任务）
- execute: 代码实施
- review: 代码审查
- verification-before-completion: 验证先行
- finishing-a-development-branch: 收尾分支

## 知识流

```
[文档/URL/文件] → pm-knowledge.ingest → wiki
                                            ↓
用户提问 → pm-knowledge.query → 知识摘要 → brainstorming → 设计决策 → decisions/
                                                          ↓
                                                    write-prd → PRD → requirements/
                                                          ↓
                                              writing-plans → 实施计划 → execute → review → synthesis/
                                                          ↓
                                              verification → evidence-based completion → finishing

多份PRD → prd-reconcile → 冲突分析 → 决策 → 全局PRD → requirements/
```