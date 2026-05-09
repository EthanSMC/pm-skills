# CLAUDE.md - PM Skills 项目

这是一个组合多个 skills 的工作流 plugin 项目。

## 项目结构

```
PM_skills/
├── .claude/
│   ├── settings.json          # Claude Code 配置（MCP + skills source）
│   ├── settings.local.json    # 本地配置
│   └── commands/              # 本地 commands
│       └── pm-workflow.md     # /pm-workflow 命令入口
├── skills/                    # NPM 包形式的 skills
│   └── pm-skills/
│       ├── package.json       # 包元信息 + skills 路径注册
│       ├── README.md
│       ├── workflow/          # 工作流编排
│       │   └── pm-workflow.md
│       ├── knowledge/         # 知识管理
│       │   ├── pm-knowledge.md
│       │   ├── pm-personalize.md
│       │   └── prd-reconcile.md
│       ├── product/           # PRD 撰写
│       │   └── write-prd.md
│       ├── design/            # 需求探索
│       │   ├── brainstorming.md
│       │   ├── visual-companion.md
│       │   └── scripts/       # 可视化伴侣服务端
│       └── implementation/    # 代码实施
│           ├── writing-plans.md              # 实施规划（bite-sized TDD任务）
│           ├── execute.md                    # 代码实施
│           ├── review.md                     # 代码审查
│           ├── verification-before-completion.md  # 验证先行
│           ├── finishing-a-development-branch.md  # 收尾分支
│           └── spec-document-reviewer-prompt.md
├── .pm-wiki/             # 项目知识库目录
├── raw/                     # 原始文档（待摄入）
└── CLAUDE.md
```

## 可用 Skills

| Skill | 触发方式 | 说明 |
|-------|---------|------|
| `/pm-workflow` | 显式调用 | 主编排，串联知识→脑暴→规划→实施→审查 |
| `/pm-knowledge` | 显式调用或 workflow 自动调用 | 知识摄入、检索、组织 |
| `/pm-personalize` | 显式调用或定时运行 | 从项目库提炼通用知识到个人库 |
| `/prd-reconcile` | 显式调用 | 多份PRD/需求文档合并与消歧 |
| `/brainstorming` | 显式调用或 workflow 自动调用 | 需求探索与设计 |
| `/write-prd` | workflow 内部调用 | PRD 撰写（增量，不重复 spec） |
| `/writing-plans` | workflow 内部调用 | 实施规划（bite-sized TDD任务分解） |
| `/execute` | workflow 内部调用 | 代码实施（按计划执行） |
| `/review` | workflow 内部调用 | 代码质量审查 |
| `/verification-before-completion` | 声称完成前 | 验证先行（证据>声称） |
| `/finishing-a-development-branch` | 实施完成后 | 收尾分支（merge/PR/keep/discard） |

## 如何使用

```
/pm-workflow [任务描述]
```

或单独调用任意 skill：

```
/brainstorming [需求描述]
/pm-knowledge query [查询内容]
```

## 如何扩展

### 添加新 Skill

在对应分类目录下创建 `.md` 文件：

1. 在 `skills/pm-skills/{workflow,knowledge,design,implementation}/` 下创建文件
2. 添加 frontmatter（`name` + `description`）
3. 在 `package.json` 的 `skills` 数组中添加路径

### 组合现有 Skills

在 skill 中使用 Skill 工具调用其他 skills。

## 配置说明

settings.json 中的 skills 配置：

```json
{
  "skills": {
    "sources": [
      { "type": "local", "path": "./skills/pm-skills" }
    ]
  },
  "mcpServers": {
    "qmd": {
      "command": "qmd",
      "args": ["mcp"]
    }
  }
}
```

## 前置依赖

- **MinerU Document Explorer (qmd)** — 知识引擎的文档解析/检索底层
  - `npm install mineru-document-explorer`（安装后全局可用 `qmd` 命令）
  - `pip install pymupdf python-docx python-pptx`
