# PM Skills

产品经理完整工作流 Skills Plugin — 从知识摄入到需求分析到代码审查。

## 快速开始

```
/pm-workflow [任务描述]
```

## 工作流阶段

```
阶段0: 知识准备     pm-knowledge
阶段1: 需求探索     brainstorming
阶段2: 实施规划     plan
阶段3: 代码实施     execute
阶段4: 代码审查     review
```

## 项目结构

```
PM_skills/
├── .claude/
│   ├── settings.json              # Claude Code 配置
│   └── commands/                  # 本地 skills（可选）
├── skills/
│   └── pm-skills/                 # 核心 Plugin
│       ├── package.json
│       ├── README.md
│       ├── skills/                # 所有 skill 定义
│       │   ├── pm-workflow.md     # 主编排
│       │   ├── pm-knowledge.md    # 知识引擎
│       │   ├── brainstorming.md   # 需求探索
│       │   ├── plan.md
│       │   ├── execute.md
│       │   └── review.md
│       └── scripts/               # 可视化伴侣服务端
├── .project-wiki/                 # 项目知识库（自动创建）
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
