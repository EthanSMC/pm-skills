# PM Skills

产品经理完整工作流 Skills Plugin — 从知识摄入到需求分析到代码审查。

## 快速开始

```
/pm-workflow [任务描述]
```

## 工作流阶段

```
阶段0: 知识准备     pm-knowledge / prd-reconcile
阶段1: 需求探索     brainstorming
阶段2: 实施规划     writing-plans
阶段3: 代码实施     execute
阶段4: 代码审查     review
阶段5: 验证先行     verification-before-completion
阶段6: 收尾分支     finishing-a-development-branch
```

## 项目结构

```
PM_skills/
├── .claude/
│   ├── settings.json              # Claude Code 配置
│   └── commands/
│       └── pm-workflow.md         # /pm-workflow 命令入口
├── skills/
│   └── pm-skills/                 # 核心 Plugin
│       ├── package.json
│       ├── README.md
│       ├── workflow/
│       │   └── pm-workflow.md     # 主编排
│       ├── knowledge/
│       │   ├── pm-knowledge.md    # 知识引擎
│       │   ├── pm-personalize.md  # 个人知识提炼
│       │   └── prd-reconcile.md   # 多文档合并与消歧
│       ├── design/
│       │   ├── brainstorming.md   # 需求探索
│       │   ├── visual-companion.md # 可视化伴侣
│       │   └── scripts/           # 可视化伴侣服务端
│       ├── product/
│       │   └── write-prd.md       # PRD 撰写
│       └── implementation/
│           ├── writing-plans.md              # 实施规划
│           ├── execute.md                    # 代码实施
│           ├── review.md                     # 代码审查
│           ├── verification-before-completion.md  # 验证先行
│           └── finishing-a-development-branch.md  # 收尾分支
├── .pm-wiki/                 # 项目知识库（自动创建）
├── raw/                     # 原始文档（待摄入）
├── CLAUDE.md
└── README.md
```

## 前置依赖

```bash
# MinerU Document Explorer（文档解析和检索）
npm install -g mineru-document-explorer
pip install pymupdf python-docx python-pptx
```

## 详细文档

见 [skills/pm-skills/README.md](skills/pm-skills/README.md)

## License

MIT
