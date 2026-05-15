# CLAUDE.md - PM Skills 项目

PM 工作流 skill plugin — 从知识摄入到需求探索到 PRD 撰写，可选原型验证。

## 项目结构

```
PM_skills/
├── .claude-plugin/
│   ├── plugin.json              # Claude Code plugin 定义
│   └── marketplace.json         # Marketplace 展示信息
├── skills/pm-skills/
│   └── pm-workflow/             # 唯一用户入口
│       ├── SKILL.md             # 主编排 skill（路由+门控+调度）
│       └── references/          # pm-workflow 直接调度的子 skill
│           ├── pm-knowledge/
│           │   ├── SKILL.md     # 知识引擎
│           │   └── scripts/     # Python 工具脚本
│           ├── pm-brainstorming/SKILL.md  # 需求探索与设计
│           ├── write-prd/SKILL.md         # PRD 撰写
│           ├── prd-reconcile/SKILL.md     # 多文档合并与消歧
│           ├── pm-personalize/SKILL.md    # 个人知识提炼
│           ├── visual-companion/
│           │   ├── SKILL.md     # 浏览器可视化辅助
│           │   └── scripts/     # 可视化伴侣服务端
│           └── prototyping/     # 原型验证（编排器）
│               ├── SKILL.md
│               ├── spec-document-reviewer-prompt.md
│               └── references/  # prototyping 调度的子 skill
│                   ├── pm-writing-plans/SKILL.md     # 实施计划编写
│                   ├── pm-tdd/
│                   │   ├── SKILL.md                  # 测试驱动开发
│                   │   └── testing-anti-patterns.md
│                   ├── pm-executing-plans/SKILL.md   # 计划执行
│                   ├── pm-verification/SKILL.md      # 验证门控
│                   ├── pm-branch-management/SKILL.md # 分支收尾
│                   ├── pm-using-worktrees/SKILL.md   # 工作树管理
│                   └── pm-frontend-design/SKILL.md   # 前端设计
├── raw/                         # 知识摄入队列（进入即摄入，workflow 自动检测变化）
└── README.md
```

## 可用 Skill

**唯一用户入口**：`/pm-workflow`

pm-workflow 是总控入口，内部自动调度所有子 skill。支持阶段跳转和门控确认。

```
/pm-workflow [任务描述]                  → 默认从阶段0开始全流程
/pm-workflow 从需求探索开始 [任务描述]     → 跳到阶段1
/pm-workflow 直接写PRD                   → 跳到阶段2
/pm-workflow 原型验证                    → 跳到阶段3
/pm-workflow 继续                        → 从上次中断的阶段恢复
```

### 内部子 skill（由 pm-workflow 自动调度，无需单独调用）

**pm-workflow 直接调度**：

| 子 skill | 阶段 | 说明 |
|---------|------|------|
| pm-knowledge | 阶段0 | 知识摄入、检索、组织 |
| prd-reconcile | 阶段0a（按需） | 多份PRD/需求文档合并与消歧 |
| pm-brainstorming | 阶段1 | 需求探索与设计 |
| write-prd | 阶段2 | PRD 撰写（增量，不重复 spec） |
| prototyping | 阶段3（可选） | 原型验证（技术规格+实施计划+骨架代码） |
| pm-personalize | 按需 | 从项目库提炼通用知识到个人库 |
| visual-companion | 阶段1内部 | 浏览器端可视化辅助 |

**prototyping 内部调度**：

| 子 skill | 子阶段 | 说明 |
|---------|--------|------|
| pm-writing-plans | 3.2 | 实施计划编写（bite-sized TDD、无占位符铁律） |
| pm-tdd | 3.2/3.3 内部引用 | 测试驱动开发（Iron Law、合理化防御） |
| pm-executing-plans | 3.3 | 计划执行（逐步骤、阻塞即停） |
| pm-frontend-design | 3.1.5（可选） | 前端设计（UI组件结构/视觉方向/交互模式） |
| pm-verification | 3.5 | 验证门控（证据先行、5步门控函数） |
| pm-branch-management | 3.6 | 分支收尾（环境检测、4/3选项、provenance清理） |
| pm-using-worktrees | 3.2/3.3 引用 | 工作树管理（隔离工作空间） |

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