# PM Skills v2.0.5

> 你不需要懂编程、不需要懂 AI。只要能跟着一步步操作，就能用。

## 这是什么？

PM Skills 是一个叫申名翀的产品因为自己太菜，做了一个**产品经理助手**。你把需求、文档、想法告诉它，它帮你：

- 把乱七八糟的需求整理清楚
- 写出正式的 PRD（产品需求文档）
- 生成可跑的原型骨架代码

整个过程就像和一个很专业的产品经理聊天。

## 安装

PM Skills 采用 [Agent Skills 开放标准](https://agentskills.io) 格式（YAML frontmatter + Markdown 正文）。越来越多 AI coding agent 直接支持此格式，选你用的那个：

### Claude Code

**方式 A：npm 安装（推荐）**

```bash
npm install @ethansmc/pm-skills
```

安装后把 `node_modules/@ethansmc/pm-skills/skills/pm-skills/pm-workflow/` 复制到项目里：

```bash
cp -r node_modules/@ethansmc/pm-skills/skills/pm-skills/pm-workflow  你的项目/.claude/skills/pm-workflow
```

重启 Claude Code，输入 `/` 应能看到 pm-workflow skill。

**方式 B：Marketplace 安装**

```bash
claude plugin marketplace add https://github.com/EthanSMC/pm-skills
claude plugin install pm-skills
```

重启 Claude Code，输入 `/` 应能看到 pm-workflow skill。

**方式 C：手动复制**

```bash
git clone https://github.com/EthanSMC/pm-skills.git
cp -r pm-skills/skills/pm-skills/pm-workflow  你的项目/.claude/skills/pm-workflow
```

只需复制 `pm-workflow/` 整个目录，所有子 skill 都在里面。

### Codex CLI（OpenAI）

Codex CLI 使用 `.agents/skills/` 目录，SKILL.md 格式完全兼容：

```bash
npm install @ethansmc/pm-skills
cp -r node_modules/@ethansmc/pm-skills/skills/pm-skills/pm-workflow  你的项目/.agents/skills/pm-workflow
```

或手动克隆：

```bash
git clone https://github.com/EthanSMC/pm-skills.git
cp -r pm-skills/skills/pm-skills/pm-workflow  你的项目/.agents/skills/pm-workflow
```

### OpenCode / Crush / Kimi Code

直接兼容 `.claude/skills/` 目录，和 Claude Code npm 安装方式相同：

```bash
npm install @ethansmc/pm-skills
cp -r node_modules/@ethansmc/pm-skills/skills/pm-skills/pm-workflow  你的项目/.claude/skills/pm-workflow
```

或手动克隆：

```bash
git clone https://github.com/EthanSMC/pm-skills.git
cp -r pm-skills/skills/pm-skills/pm-workflow  你的项目/.claude/skills/pm-workflow
```

### Gemini CLI

Gemini CLI 使用 `.gemini/skills/` 目录，每个 skill 是一个 `.md` 文件：

```bash
npm install @ethansmc/pm-skills
```

然后逐个复制 SKILL.md：

```bash
PKG=node_modules/@ethansmc/pm-skills/skills/pm-skills/pm-workflow
cp $PKG/SKILL.md                                          你的项目/.gemini/skills/pm-workflow.md
cp $PKG/references/pm-knowledge/SKILL.md                  你的项目/.gemini/skills/pm-knowledge.md
cp $PKG/references/pm-brainstorming/SKILL.md              你的项目/.gemini/skills/pm-brainstorming.md
cp $PKG/references/pm-personalize/SKILL.md                你的项目/.gemini/skills/pm-personalize.md
cp $PKG/references/prd-reconcile/SKILL.md                 你的项目/.gemini/skills/prd-reconcile.md
cp $PKG/references/visual-companion/SKILL.md              你的项目/.gemini/skills/visual-companion.md
cp $PKG/references/write-prd/SKILL.md                     你的项目/.gemini/skills/write-prd.md
cp $PKG/references/prototyping/SKILL.md                   你的项目/.gemini/skills/prototyping.md
cp $PKG/references/prototyping/references/pm-writing-plans/SKILL.md      你的项目/.gemini/skills/pm-writing-plans.md
cp $PKG/references/prototyping/references/pm-tdd/SKILL.md                你的项目/.gemini/skills/pm-tdd.md
cp $PKG/references/prototyping/references/pm-executing-plans/SKILL.md   你的项目/.gemini/skills/pm-executing-plans.md
cp $PKG/references/prototyping/references/pm-verification/SKILL.md      你的项目/.gemini/skills/pm-verification.md
cp $PKG/references/prototyping/references/pm-branch-management/SKILL.md 你的项目/.gemini/skills/pm-branch-management.md
cp $PKG/references/prototyping/references/pm-using-worktrees/SKILL.md   你的项目/.gemini/skills/pm-using-worktrees.md
cp $PKG/references/prototyping/references/pm-frontend-design/SKILL.md   你的项目/.gemini/skills/pm-frontend-design.md
```

同时把 `pm-knowledge/scripts/` 和 `visual-companion/scripts/` 也复制到项目中。

### 其他 Agent

SKILL.md 的 Markdown 正文是通用的，任何能读取项目级指令的 agent 都能用：

| Agent 类型 | 安装方式 |
|-----------|---------|
| 支持 Agent Skills 标准的 | `npm install @ethansmc/pm-skills` → 复制 pm-workflow/ 到对应 skills 目录 |
| 用单文件指令的（AGENTS.md、kimi.md 等） | 合并所有 SKILL.md 到指令文件，删除 frontmatter |

如果你的 agent 不识别 YAML frontmatter（`---` 包裹的 3 行），删除即可。Markdown 正文任何 agent 都能理解。

### 可选增强：MinerU Document Explorer (qmd)

知识引擎的增强模式依赖 qmd。**不装也能用**（自动降级为文件系统检索），但装了检索更精准：

```bash
npm install -g mineru-document-explorer
pip install pymupdf python-docx python-pptx
```

验证：`qmd --version`

Claude Code 用户还需在项目的 `.claude/settings.json` 中追加：

```json
{
  "mcpServers": {
    "qmd": { "command": "qmd", "args": ["mcp"] }
  }
}
```

其他 agent 用户：qmd 通过 CLI 调用（`qmd query`、`qmd wiki` 等），无需额外配置。

### 可选：Python 工具脚本

pm-knowledge 自带 scripts/，需 Python 依赖：

```bash
pip install pyyaml pytest
```

脚本命令：
- `python pm-wiki-graph.py build` — 构建 `.pm-wiki/` 知识图谱
- `python pm-wiki-lint.py confidence` — 计算页面置信度评分
- `python pm-wiki-crystallize.py session-end` — 从工作笔记提取知识页

### 验证

启动你的 agent，输入 PM 相关的问题（如"帮我写一个任务管理系统的 PRD"），看它是否按 PM Skills 的流程引导你。

Claude Code 用户可以输入 `/`，看到 pm-workflow、pm-brainstorming 等 skill 名字就说明装好了。

## 开始使用

| 你想做什么 | 输入什么 |
|-----------|---------|
| 完整产品经理流程 | `/pm-workflow 我要做xxx功能` |
| 讨论需求 | `/pm-brainstorming xxx的设计` |
| 写 PRD | `/write-prd` |
| 合并多份 PRD | `/prd-reconcile` |
| 原型验证 | `/prototyping` |
| 摄入文档到知识库 | `/pm-knowledge ingest raw/xxx.docx` |
| 提炼个人知识 | `/pm-personalize` |

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

**Skill/命令不生效** → 检查指令文件是否在正确的目录下

**知识检索不够精准** → 安装 MinerU (qmd)，见"可选增强"

**合并多份 PRD** → 直接说"合并这几份 PRD"，agent 会自动调用对应流程

**"待审"提示** → agent 标记了分析性内容，你看一下告诉它"确认"或"修改xxx"

**YAML frontmatter 是什么？** → 每个 SKILL.md 开头有 3 行 `---` 包裹的内容（name 和 description），这是 [Agent Skills 开放标准](https://agentskills.io) 格式。大多数 agent 支持；如果你的 agent 不识别，删除这 3 行即可。

---

## 技术细节

<details>
<summary>展开查看 Skill 列表、工作流、知识架构等技术细节</summary>

### 包含的 Skills

| Skill | 说明 | 触发时机 |
|-------|------|---------|
| `pm-workflow` | 主编排 skill，串联所有阶段 | `/pm-workflow [任务描述]` |
| `pm-knowledge` | 知识引擎（摄入、检索、组织） | 知识摄入/查询时自动调用 |
| `pm-personalize` | 从项目库提炼通用知识到个人库 | 显式调用或 ingest 后自动建议 |
| `prd-reconcile` | 多文档消歧（冲突分析→决策→合并） | 多份PRD/需求文档需合并时 |
| `pm-brainstorming` | 需求探索与设计 | 创建新功能/组件前 |
| `visual-companion` | 浏览器端可视化辅助 | brainstorming 中视觉问题 |
| `write-prd` | PRD 撰写（增量，不重复 spec） | 设计文档通过后 |
| `prototyping` | 原型验证（编排器，委托 pm-* 子 skill） | PRD 通过后用户选择进入 |
| `pm-writing-plans` | 实施计划编写（TDD 铁律 + 无占位符） | prototyping 子阶段 2 |
| `pm-tdd` | 测试驱动开发（Iron Law + 合理化防御） | pm-writing-plans/pm-executing-plans 内部引用 |
| `pm-executing-plans` | 计划执行（逐步骤 + 阻塞即停） | prototyping 子阶段 3 |
| `pm-verification` | 验证门控（证据先行 + 5步门控函数） | prototyping 子阶段 5 |
| `pm-branch-management` | 分支收尾（操作手册 + provenance 清理） | prototyping 子阶段 6 |
| `pm-using-worktrees` | 工作树管理（隔离工作空间） | pm-writing-plans/pm-executing-plans 引用 |
| `pm-frontend-design` | 前端设计（UI组件/视觉/交互） | prototyping 子阶段 1.5（可选，仅前端原型） |

### 工作流

```
阶段0: pm-knowledge    知识准备（检索已有知识）
阶段0a: prd-reconcile  消歧分支（冲突分析→决策→合并，不重复摄入）
阶段1: pm-brainstorming   需求探索（基于知识基础）
阶段2: write-prd       PRD 撰写（增量补充 spec） ← 默认终点
阶段3: prototyping     原型验证（可选，用户选择后进入）
  子阶段: 技术规格 → [前端设计] → 实施计划 → 骨架构建 → 审查 → 验证 → 分支管理
    ↳ 前端设计仅 UI 原型时执行（pm-frontend-design）
    ↳ 实施计划/骨架构建/验证/分支管理 委托 pm-* skill（Iron Law 执行纪律）
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

多份PRD → prd-reconcile → 冲突分析 → 决策 → 全局PRD（产出由 pm-knowledge ingest 管理）
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

### 降级策略

pm-knowledge 支持三级降级，不装 qmd 也能用：

| 可用性 | 使用方式 |
|--------|---------|
| MCP 连接正常（推荐） | 通过 MCP 工具调用 |
| MCP 不可用，CLI 可用 | Bash 调用 qmd 命令 |
| qmd 未安装 | 纯文件系统操作 — 直接读写 `.pm-wiki/` |

### 项目文件结构

```
skills/pm-skills/
  pm-workflow/
    SKILL.md
  pm-knowledge/
    SKILL.md
    scripts/
      pm-wiki-graph.py        知识图谱构建
      pm-wiki-lint.py          知识健康检查
      pm-wiki-crystallize.py   知识蒸馏固化
      conftest.py
      requirements.txt
      test_*.py
  pm-personalize/
    SKILL.md
  prd-reconcile/
    SKILL.md
  pm-brainstorming/
    SKILL.md
  visual-companion/
    SKILL.md
    scripts/
      server.cjs               可视化伴侣服务端
      helper.js
      frame-template.html
      start-server.sh
      stop-server.sh
  write-prd/
    SKILL.md
  prototyping/
    SKILL.md
  pm-writing-plans/
    SKILL.md
  pm-tdd/
    SKILL.md
    testing-anti-patterns.md
  pm-executing-plans/
    SKILL.md
  pm-verification/
    SKILL.md
  pm-branch-management/
    SKILL.md
  pm-using-worktrees/
    SKILL.md
  pm-frontend-design/
    SKILL.md
```

</details>

## Acknowledgments

- [rohitg00](https://gist.github.com/rohitg00/2067ab416f7bbe447c1977edaaa681e2) — 记忆生命周期机制
- [karpathy](https://gist.github.com/karpathy/442a6bf555914893e9891c11519de94f) — 知识库管理
- [MinerU Document Explorer](https://github.com/opendatalab/MinerU) — 知识引擎的文档解析与检索底层
- [Superpowers](https://github.com/anthropics/claude-plugins-official) — Claude Code plugin 架构参考与实施类 skill 补充
- [Rykii](https://github.com/Rykii) — 使用 wiki 做项目知识管理的idea

## License

MIT
