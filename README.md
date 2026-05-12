<!--
# Agent Setup Guide

## 快速安装

如果用户的项目还没有配置 pm-skills，执行以下步骤：

1. 找到项目根目录下的 `.claude/settings.json`（不存在则创建）
2. 根据安装方式写入 skills source：

npm 安装：
```json
{
  "skills": {
    "sources": [
      { "type": "npm", "package": "pm-skills" }
    ]
  }
}
```

本地安装（将 path 替换为实际路径）：
```json
{
  "skills": {
    "sources": [
      { "type": "local", "path": "/absolute/path/to/pm-skills/skills/pm-skills" }
    ]
  }
}
```

3. 验证：重启 Claude Code 后，输入 `/pm-workflow` 应能触发 skill

## 可选：MCP 配置

知识引擎依赖 MinerU Document Explorer (qmd) 进行文档解析和检索。
在同一 `settings.json` 中追加：

```json
{
  "skills": { ... },
  "mcpServers": {
    "qmd": { "command": "qmd", "args": ["mcp"] }
  }
}
```

未配置 qmd 时自动降级为文件系统检索，不影响基本使用。

## 可选：Python 工具脚本

知识图谱/置信度/结晶 三个脚本位于 `scripts/`，需 Python 依赖：

```bash
pip install pyyaml pytest
```

脚本命令：
- `python scripts/pm-wiki-graph.py build` — 构建 `.pm-wiki/` 知识图谱
- `python scripts/pm-wiki-lint.py confidence` — 计算页面置信度评分
- `python scripts/pm-wiki-crystallize.py session-end` — 从工作笔记提取知识页

## Skill 触发词

用户说以下内容时，调用对应 skill：

| 用户意图 | skill | 调用方式 |
|---------|-------|---------|
| "帮我做产品流程" / "我要设计xxx" / `/pm-workflow` | pm-workflow | `Skill("pm-workflow")` |
| "整理这些需求" / "讨论一下xxx设计" / `/pm-brainstorming` | pm-brainstorming | `Skill("pm-brainstorming")` |
| "写PRD" / `/write-prd` | write-prd | `Skill("write-prd")` |
| "合并这几份PRD" / `/prd-reconcile` | prd-reconcile | `Skill("prd-reconcile")` |
| "做个原型验证" / `/prototyping` | prototyping | `Skill("prototyping")` |
| "摄入这个文档" / `/pm-knowledge ingest <path>` | pm-knowledge | `Skill("pm-knowledge")` |

## 工作流编排规则

pm-workflow 是唯一编排器。各 skill 不互相 invoke，由 pm-workflow 控制流转：

```
Phase 0:  pm-knowledge.query → 知识摘要注入 Phase 1
Phase 0a: prd-reconcile（仅多文档时触发）
Phase 1:  pm-brainstorming ← 知识摘要
Phase 2:  write-prd ← spec（增量，不重复已有内容）
Phase 2 end: 问用户"是否原型验证？" → 否则结束
Phase 3:  prototyping（仅用户明确选择后）
```

## 产出路径

各阶段写入位置：

- pm-brainstorming → `docs/pm/specs/YYYY-MM-DD-<topic>-design.md`
- write-prd → `docs/pm/prds/<filename>.md`
- prototyping → `docs/prototype/<feature>/` (spec.md, plan.md, scaffold-index.md)
- knowledge → `.pm-wiki/` 各子目录

知识库目录自动创建，无需手动建。
-->

# PM Skills

> 你不需要懂编程、不需要懂 AI。只要能跟着一步步操作，就能用。

## 这是什么？

PM Skills 是一个**产品经理助手**。你把需求、文档、想法告诉它，它帮你：

- 把乱七八糟的需求整理清楚
- 写出正式的 PRD（产品需求文档）
- 生成可跑的原型骨架代码

整个过程就像和一个很专业的产品经理聊天。

## 安装

一台电脑（Windows 或 Mac），能上网。下面 4 步按顺序装好：

### 第 1 步：装 Node.js

1. 打开浏览器，访问 https://nodejs.org
2. 点击左边大按钮（LTS 版本号），下载安装包
3. 双击下载的文件，一路点"下一步"装完
4. 验证：打开终端，输入 `node --version`，看到版本号就 OK

**怎么打开终端？**

| 系统 | 操作 |
|------|------|
| Windows | 按 `Win + R`，输入 `cmd`，回车 |
| Mac | 按 `Cmd + 空格`，输入 `Terminal`，回车 |

### 第 2 步：装 Claude Code

1. 打开终端，输入：

```
npm install -g @anthropic-ai/claude-code
```

2. 验证：`claude --version`，看到版本号就 OK

3. 第一次运行需要登录，输入 `claude`，选 **Anthropic API key**：
   - 去 https://console.anthropic.com 注册账号
   - Settings → API Keys → 创建 key → 复制粘贴到终端

### 第 3 步：装 PM Skills

**npm 安装：**

```
npm install -g pm-skills
```

**本地安装（如果 npm 上没有）：**

1. 打开 https://github.com/EthanSMC/pm-skills
2. 点击绿色 **Code** 按钮 → **Download ZIP**
3. 解压，放到你喜欢的地方
4. 终端进入文件夹：`cd 你放pm-skills的路径`
5. 装依赖：`npm install`

### 第 4 步：连接到 Claude Code

在你的项目文件夹里创建 `.claude/settings.json`：

npm 安装的写法：
```json
{
  "skills": {
    "sources": [
      { "type": "npm", "package": "pm-skills" }
    ]
  }
}
```

本地安装的写法：
```json
{
  "skills": {
    "sources": [
      { "type": "local", "path": "你解压的路径/skills/pm-skills" }
    ]
  }
}
```

## 开始使用

1. 终端进入项目文件夹：`cd 你的项目路径`
2. 启动：`claude`
3. 输入命令：

| 你想做什么 | 输入什么 |
|-----------|---------|
| 完整产品经理流程 | `/pm-workflow 我要做xxx功能` |
| 讨论需求 | `/pm-brainstorming xxx的设计` |
| 写 PRD | `/write-prd` |
| 合并多份 PRD | `/prd-reconcile` |
| 原型验证 | `/prototyping` |

**最常用：**

```
/pm-workflow 我需要设计一个任务管理系统，支持创建、分配、跟踪任务状态
```

Claude 会引导你走完整个流程：整理知识 → 讨论需求 → 写 PRD → 问你要不要做原型。每一步都问你意见，你只需要回答问题。

**把文档给助手看：**

```
/pm-knowledge ingest raw/运营管理平台-PRD.docx
```

助手会读取文档、整理知识。下次提问时自动参考。

**退出：** 按 `Ctrl + C`

## 产出文件

| 产出 | 位置 | 说明 |
|------|------|------|
| 设计文档 | `docs/pm/specs/` | 设计规格 |
| PRD | `docs/pm/prds/` | 产品需求文档 |
| 原型 | `docs/prototype/<功能名>/` | 技术规格+实施计划+骨架代码 |
| 知识库 | `.pm-wiki/` | 自动积累的项目知识 |

## 常见问题

**"command not found"** → 检查 Node.js 和 Claude Code 是否装好，终端里 `node --version` 和 `claude --version` 能运行吗？

**Claude Code 无响应** → 网络问题，需联网访问 Anthropic 服务

**PM Skills 命令不生效** → 检查 `.claude/settings.json` 是否在项目文件夹里、路径是否正确

**合并多份 PRD** → `/prd-reconcile`

**"待审"提示** → 助手标记了分析性内容，你看一下告诉它"确认"或"修改xxx"

---

## 技术细节

<details>
<summary>展开查看 Skill 列表、工作流、知识架构等技术细节</summary>

### 包含的 Skills

| Skill | 说明 | 触发时机 |
|-------|------|---------|
| `pm-workflow` | 主编排 skill，串联所有阶段 | `/pm-workflow [任务描述]` |
| `pm-knowledge` | 知识引擎（摄入、检索、组织） | 知识摄入/查询时自动调用 |
| `pm-personalize` | 从项目库提炼通用知识到个人库 | 手动调用或 ingest 后自动建议 |
| `prd-reconcile` | 多文档合并与消歧 | 多份PRD/需求文档需合并时 |
| `pm-brainstorming` | 需求探索与设计 | 创建新功能/组件前 |
| `write-prd` | PRD 撰写（增量，不重复 spec） | 设计文档通过后 |
| `prototyping` | 原型验证（技术规格+实施计划+骨架代码） | PRD 通过后用户选择进入 |

### 工作流

```
阶段0: pm-knowledge    知识准备（检索已有知识）
阶段0a: prd-reconcile  多文档合并与消歧（按需）
阶段1: pm-brainstorming   需求探索（基于知识基础）
阶段2: write-prd       PRD 撰写（增量补充 spec） ← 默认终点
阶段3: prototyping     原型验证（可选，用户选择后进入）
  子阶段: 技术规格 → 实施计划 → 骨架构建 → 审查 → 验证 → 分支管理
```

知识流：

```
文档/URL/文件 → pm-knowledge.ingest → wiki
                                            ↓
用户提问 → pm-knowledge.query → 三流检索 → 知识摘要 → pm-brainstorming → decisions/
                                                          ↓
                                                    write-prd → PRD → requirements/
                                                          ↓
                                                [用户选择: 是否原型验证?]
                                                 ↓ (是)                ↓ (否)
                                         prototyping → 原型产出       工作流结束

多份PRD → prd-reconcile → 冲突分析 → 决策 → 全局PRD → requirements/
```

### 知识库架构

**双库分离：**

```
个人知识库 ~/.pm-wiki/  项目知识库 <project>/.pm-wiki/
维度：你这个人                   维度：这个项目
跨项目积累，随你走               聚焦具体产品

skills/    技能、成长             raw/          原始文档（待摄入）
insights/  洞察、思考             context/      背景、目标
industry/  行业、趋势             competitors/  竞品分析（按需）
templates/ 模板、框架             users/        目标用户（按需）
methods/   方法论、实践           requirements/ 需求文档
tools/     工具心得               constraints/  约束假设
reusable/  可复用片段             decisions/    决策记录(ADR)
                                synthesis/    综合分析（按需）
                                references/   → 链接到个人知识库（按需）
```

查询优先级：项目知识库 → 个人知识库 → 原始文档

**审核分流：**

| 内容类型 | 处理方式 |
|---------|---------|
| 事实性 | 自动写入 |
| 结构性 | 自动写入 |
| 分析性 | 草稿待审 |
| 推荐性 | 草稿待审 |

### 前置依赖（进阶）

**MinerU Document Explorer (qmd)** — 文档解析和检索引擎：

```bash
npm install -g mineru-document-explorer
pip install pymupdf python-docx python-pptx
```

### 项目结构

```
skills/pm-skills/
├── package.json
├── README.md
├── workflow/
│   └── pm-workflow.md
├── knowledge/
│   ├── pm-knowledge.md
│   ├── pm-personalize.md
│   └── prd-reconcile.md
├── design/
│   ├── pm-brainstorming.md
│   ├── visual-companion.md
│   └── scripts/
├── product/
│   └── write-prd.md
├── implementation/
│   ├── prototyping.md
│   └── spec-document-reviewer-prompt.md
└── scripts/
    ├── pm-wiki-graph.py
    ├── pm-wiki-lint.py
    ├── pm-wiki-crystallize.py
    ├── conftest.py
    ├── requirements.txt
    ├── test_graph.py
    ├── test_lint.py
    └── test_crystallize.py
```

</details>

## License

MIT