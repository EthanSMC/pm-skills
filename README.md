# PM Skills v2.0.0

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

**方式 A：Marketplace 安装（推荐）**

```bash
claude plugin marketplace add https://github.com/EthanSMC/pm-skills
claude plugin install pm-skills
```

重启 Claude Code，输入 `/` 应能看到 pm-workflow skill。

**方式 B：npm 安装**

```bash
npm install @ethansmc/pm-skills
```

安装后把 `skills/pm-skills/pm-workflow/` 目录复制到项目里：

```
你的项目/.claude/skills/pm-workflow/
  SKILL.md                       ← 主入口
  references/                    ← 所有子 skill
    pm-knowledge/SKILL.md + scripts/
    pm-brainstorming/SKILL.md
    write-prd/SKILL.md
    prd-reconcile/SKILL.md
    pm-personalize/SKILL.md
    visual-companion/SKILL.md + scripts/
    prototyping/SKILL.md + references/...
```

只需复制 `pm-workflow/` 整个目录，所有子 skill 都在里面。

**方式 C：手动复制**

```bash
git clone https://github.com/EthanSMC/pm-skills.git
cp -r pm-skills/skills/pm-skills/pm-workflow  你的项目/.claude/skills/pm-workflow
```

### Codex CLI（OpenAI）

Codex CLI 使用 `.agents/skills/` 目录，SKILL.md 格式完全兼容：

```bash
git clone https://github.com/EthanSMC/pm-skills.git
cp -r pm-skills/skills/pm-skills/pm-workflow  你的项目/.agents/skills/pm-workflow
```

目录结构：

```
你的项目/.agents/skills/pm-workflow/
  SKILL.md
  references/pm-knowledge/SKILL.md + scripts/
  references/pm-brainstorming/SKILL.md
  ...
```

### OpenCode / Crush / Kimi Code

直接兼容 `.claude/skills/` 目录，和 Claude Code 手动复制相同：

```bash
git clone https://github.com/EthanSMC/pm-skills.git
cp -r pm-skills/skills/pm-skills/pm-workflow  你的项目/.claude/skills/pm-workflow
```

### Gemini CLI

Gemini CLI 使用 `.gemini/skills/` 目录，每个 skill 是一个 `.md` 文件：

```bash
git clone https://github.com/EthanSMC/pm-skills.git
```

然后逐个复制 SKILL.md 到 `.gemini/skills/`：

```bash
cp pm-skills/skills/pm-skills/pm-workflow/SKILL.md                     你的项目/.gemini/skills/pm-workflow.md
cp pm-skills/skills/pm-skills/pm-workflow/references/pm-knowledge/SKILL.md     你的项目/.gemini/skills/pm-knowledge.md
cp pm-skills/skills/pm-skills/pm-workflow/references/pm-brainstorming/SKILL.md 你的项目/.gemini/skills/pm-brainstorming.md
cp pm-skills/skills/pm-skills/pm-workflow/references/write-prd/SKILL.md        你的项目/.gemini/skills/write-prd.md
cp pm-skills/skills/pm-skills/pm-workflow/references/prd-reconcile/SKILL.md    你的项目/.gemini/skills/prd-reconcile.md
cp pm-skills/skills/pm-skills/pm-workflow/references/pm-personalize/SKILL.md   你的项目/.gemini/skills/pm-personalize.md
cp pm-skills/skills/pm-skills/pm-workflow/references/visual-companion/SKILL.md 你的项目/.gemini/skills/visual-companion.md
cp pm-skills/skills/pm-skills/pm-workflow/references/prototyping/SKILL.md      你的项目/.gemini/skills/prototyping.md
cp pm-skills/skills/pm-skills/pm-workflow/references/prototyping/references/pm-writing-plans/SKILL.md      你的项目/.gemini/skills/pm-writing-plans.md
cp pm-skills/skills/pm-skills/pm-workflow/references/prototyping/references/pm-tdd/SKILL.md                你的项目/.gemini/skills/pm-tdd.md
cp pm-skills/skills/pm-skills/pm-workflow/references/prototyping/references/pm-executing-plans/SKILL.md    你的项目/.gemini/skills/pm-executing-plans.md
cp pm-skills/skills/pm-skills/pm-workflow/references/prototyping/references/pm-verification/SKILL.md       你的项目/.gemini/skills/pm-verification.md
cp pm-skills/skills/pm-skills/pm-workflow/references/prototyping/references/pm-branch-management/SKILL.md  你的项目/.gemini/skills/pm-branch-management.md
cp pm-skills/skills/pm-skills/pm-workflow/references/prototyping/references/pm-using-worktrees/SKILL.md    你的项目/.gemini/skills/pm-using-worktrees.md
cp pm-skills/skills/pm-skills/pm-workflow/references/prototyping/references/pm-frontend-design/SKILL.md    你的项目/.gemini/skills/pm-frontend-design.md
```

同时把 `pm-knowledge/scripts/` 和 `visual-companion/scripts/` 也复制到项目中。

### 其他 Agent

SKILL.md 的 Markdown 正文是通用的，任何能读取项目级指令的 agent 都能用：

| Agent 类型 | 安装方式 |
|-----------|---------|
| 支持 Agent Skills 标准的 | 复制 pm-workflow/ 整个目录到对应 skills 目录 |
| 用单文件指令的（AGENTS.md、kmi.md 等） | 合并所有 SKILL.md 到指令文件，删除 frontmatter |

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

Claude Code 用户可以输入 `/`，看到 pm-workflow 就说明装好了。

## 开始使用

**唯一入口：**

```
/pm-workflow [任务描述]
```

支持阶段跳转：

| 你想做什么 | 输入什么 |
|-----------|---------|
| 完整产品经理流程 | `/pm-workflow 我要做xxx功能` |
| 从需求探索开始 | `/pm-workflow 从需求探索开始 xxx的设计` |
| 直接写 PRD | `/pm-workflow 直接写PRD` |
| 原型验证 | `/pm-workflow 原型验证` |
| 恢复上次中断 | `/pm-workflow 继续` |

**最常用：**

```
/pm-workflow 我需要设计一个任务管理系统，支持创建、分配、跟踪任务状态
```

Claude 会引导你走完整个流程：整理知识 → 讨论需求 → 写 PRD → 问你要不要做原型。每一步都汇报产出并等你确认。

**退出：** 按 `Ctrl + C`

## 产出文件

| 产出 | 位置 | 说明 |
|------|------|------|
| 设计文档 | `docs/pm/specs/` | 设计规格 |
| PRD | `docs/pm/prds/` | 产品需求文档 |
| 原型 | `docs/prototype/<功能名>/` | 技术规格+实施计划+骨架代码 |
| 知识库 | `.pm-wiki/` | 自动积累的项目知识 |

## 常见问题

**Skill/命令不生效** → 检查 pm-workflow/ 整个目录是否在正确的 skills 目录下

**知识检索不够精准** → 安装 MinerU (qmd)，见"可选增强"

**合并多份 PRD** → `/pm-workflow 合并这几份 PRD`，路由自动识别

**"待审"提示** → agent 标记了分析性内容，你看一下告诉它"确认"或"修改xxx"

**YAML frontmatter 是什么？** → 每个 SKILL.md 开头有 3 行 `---` 包裹的内容（name 和 description），这是 [Agent Skills 开放标准](https://agentskills.io) 格式。大多数 agent 支持；如果你的 agent 不识别，删除这 3 行即可。

---

## 技术细节

<details>
<summary>展开查看 Skill 列表、工作流、知识架构等技术细节</summary>

### Skill 层级

pm-workflow 是唯一用户入口，内部按层级调度子 skill：

```
pm-workflow（唯一用户入口）
  ├─ pm-knowledge        知识引擎（阶段0）
  ├─ prd-reconcile       多文档合并（阶段0a，按需）
  ├─ pm-brainstorming    需求探索（阶段1）
  ├─ visual-companion    可视化辅助（阶段1内部，按需）
  ├─ pm-personalize      个人知识提炼（按需）
  ├─ write-prd           PRD 撰写（阶段2）
  └─ prototyping          原型验证（阶段3，可选）
      ├─ pm-writing-plans      实施计划（子阶段2）
      │   └ pm-tdd             TDD 铁律（内部引用）
      ├─ pm-executing-plans    骨架构建（子阶段3）
      │   └ pm-tdd             TDD 铁律（内部引用）
      │   └ pm-using-worktrees  工作树（内部引用）
      ├─ pm-frontend-design    前端设计（子阶段1.5，可选）
      ├─ pm-verification       验证门控（子阶段5）
      ├─ pm-branch-management  分支收尾（子阶段6）
      └─ pm-using-worktrees    工作树（内部引用）
```

### 工作流

```
阶段0: pm-knowledge    知识准备（检索已有知识）     ← 门控：汇报知识发现，确认进入
阶段0a: prd-reconcile  多文档合并与消歧（按需）
阶段1: pm-brainstorming   需求探索（基于知识基础） ← 门控：汇报设计方案，确认进入
阶段2: write-prd       PRD 撰写（增量补充 spec）   ← 门控：汇报PRD，确认进入或结束
阶段3: prototyping     原型验证（可选，用户选择后进入）
  子阶段: 技术规格 → [前端设计] → 实施计划 → 骨架构建 → 审查 → 验证 → 分支管理
    ↳ 前端设计仅 UI 原型时执行（pm-frontend-design）
    ↳ 实施计划/骨架构建/验证/分支管理 委托 pm-* skill（Iron Law 执行纪律）
```

每个阶段完成后，pm-workflow 执行门控：汇报产出 → 等用户决策（继续/跳过/回退/结束）→ 确认后才进入下一阶段。

知识流：

```
文档/URL/文件 → pm-knowledge.ingest → wiki
                                            ↓
用户提问 → pm-knowledge.query → 三流检索 → 知识摘要 → pm-brainstorming → decisions/
                                                          ↓
                                                    write-prd → PRD → requirements/
                                                          ↓
                                                [门控决策: 是否原型验证?]
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

### 降级策略

pm-knowledge 支持三级降级，不装 qmd 也能用：

| 可用性 | 使用方式 |
|--------|---------|
| MCP 连接正常（推荐） | 通过 MCP 工具调用 |
| MCP 不可用，CLI 可用 | Bash 调用 qmd 命令 |
| qmd 未安装 | 纯文件系统操作 — 直接读写 `.pm-wiki/` |

### 项目文件结构

```
skills/pm-skills/pm-workflow/
  SKILL.md                        ← 唯一用户入口
  references/                      ← pm-workflow 直接调度
    pm-knowledge/
      SKILL.md
      scripts/
        pm-wiki-graph.py           知识图谱构建
        pm-wiki-lint.py            知识健康检查
        pm-wiki-crystallize.py     知识蒸馏固化
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
        server.cjs                 可视化伴侣服务端
        helper.js
        frame-template.html
        start-server.sh
        stop-server.sh
    write-prd/
      SKILL.md
    prototyping/
      SKILL.md
      spec-document-reviewer-prompt.md
      references/                  ← prototyping 调度
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