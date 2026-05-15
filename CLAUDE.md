# CLAUDE.md - PM Skills 项目

PM 工作流 skill plugin — 从知识摄入到需求探索到 PRD 撰写，可选原型验证。

## 项目结构

```
PM_skills/
├── .claude-plugin/
│   ├── plugin.json              # Claude Code plugin 定义
│   └── marketplace.json         # Marketplace 展示信息
├── skills/pm-skills/            # Skills 目录
│   ├── pm-workflow/SKILL.md     # 主编排 skill
│   ├── pm-knowledge/
│   │   ├── SKILL.md             # 知识引擎
│   │   └── scripts/             # Python 工具脚本
│   ├── pm-personalize/SKILL.md  # 个人知识提炼
│   ├── prd-reconcile/SKILL.md   # 多文档合并与消歧
│   ├── pm-brainstorming/SKILL.md # 需求探索与设计
│   ├── visual-companion/
│   │   ├── SKILL.md             # 浏览器可视化辅助
│   │   └── scripts/             # 可视化伴侣服务端
│   ├── write-prd/SKILL.md       # PRD 撰写
│   ├── prototyping/
│   │   ├── SKILL.md             # 原型验证（编排器）
│   │   └── spec-document-reviewer-prompt.md
│   ├── pm-writing-plans/SKILL.md # 实施计划编写（TDD 铁律）
│   ├── pm-tdd/
│   │   ├── SKILL.md             # 测试驱动开发（Iron Law）
│   │   └── testing-anti-patterns.md
│   ├── pm-executing-plans/SKILL.md # 计划执行（阻塞即停）
│   ├── pm-verification/SKILL.md  # 验证门控（证据先行）
│   ├── pm-branch-management/SKILL.md # 分支收尾（操作手册）
│   ├── pm-using-worktrees/SKILL.md # 工作树管理（隔离工作空间）
│   └── pm-frontend-design/SKILL.md # 前端设计（UI组件/视觉/交互）
├── raw/                         # 知识摄入队列（进入即摄入，workflow 自动检测变化）
└── README.md
```

## 可用 Skills

| Skill | 触发方式 | 说明 |
|-------|---------|------|
| `/pm-workflow` | 显式调用 | 主编排，串联知识→脑暴→PRD→可选原型 |
| `/pm-knowledge` | 显式调用或 workflow 自动调用 | 知识摄入、检索、组织 |
| `/pm-personalize` | 显式调用或 ingest 后自动建议 | 从项目库提炼通用知识到个人库 |
| `/prd-reconcile` | 显式调用 | 多份PRD/需求文档合并与消歧 |
| `/pm-brainstorming` | 显式调用或 workflow 自动调用 | 需求探索与设计 |
| `/visual-companion` | workflow 内部调用 | 浏览器端可视化辅助 |
| `/write-prd` | workflow 内部调用 | PRD 撰写（增量，不重复 spec） |
| `/prototyping` | workflow 内部调用（可选） | 原型验证（技术规格+实施计划+骨架代码） |
| `/pm-writing-plans` | prototyping 子阶段 2 自动调用 | 实施计划编写（bite-sized TDD、无占位符铁律） |
| `/pm-tdd` | pm-writing-plans/pm-executing-plans 内部引用 | 测试驱动开发（Iron Law、合理化防御） |
| `/pm-executing-plans` | prototyping 子阶段 3 自动调用 | 计划执行（逐步骤、阻塞即停、TodoWrite） |
| `/pm-verification` | prototyping 子阶段 5 自动调用 | 验证门控（证据先行、5步门控函数） |
| `/pm-branch-management` | prototyping 子阶段 6 自动调用 | 分支收尾（环境检测、4/3选项、provenance清理） |
| `/pm-using-worktrees` | pm-writing-plans/pm-executing-plans 引用 | 工作树管理（隔离工作空间） |
| `/pm-frontend-design` | prototyping 子阶段 1.5（可选，仅前端原型） | 前端设计（UI组件结构/视觉方向/交互模式） |

## 知识自动路由

当项目存在 `.pm-wiki/` 知识库时，回答任何与项目相关的问题前，**必须先检索知识库**：

1. 检查 `.pm-wiki/` 是否存在且有内容
2. 如果存在，使用 Grep/Glob 在 `.pm-wiki/` 中搜索相关内容（或使用 Skill 工具调用 pm-knowledge 的 Query 流程）
3. 将知识库中的发现作为回答的基础，标注来源
4. 标注知识缺口（wiki 中没有覆盖的部分）

**不检索的情况**：纯技术问题（代码语法、工具使用）、无关项目的问题。

这条规则确保知识库不会沉没 — 用户建了 wiki 之后，任何提问都会自动利用已有知识，而不是每次重新从零开始。

## 使用方式

```
/pm-workflow [任务描述]
```

或单独调用任意 skill：

```
/pm-brainstorming [需求描述]
/pm-knowledge ingest [文件路径]
/pm-knowledge query [查询内容]
```

## 可选依赖

- **MinerU Document Explorer (qmd)** — 知识引擎的文档解析/检索底层
  - 安装：`npm install -g mineru-document-explorer`
  - Python 依赖：`pip install pymupdf python-docx python-pptx`
  - 未安装时自动降级为文件系统检索，不影响基本使用

- **Python 工具脚本**（pm-knowledge/scripts/）
  - `pip install pyyaml pytest`
  - 脚本命令：
    - `pm-wiki-graph.py build` — 构建知识图谱
    - `pm-wiki-lint.py confidence` — 计算置信度评分
    - `pm-wiki-crystallize.py session-end` — 从工作笔记提取知识页
