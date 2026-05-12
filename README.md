# PM Skills

> 你不需要懂编程、不需要懂 AI。只要能跟着一步步操作，就能用。

## 这是什么？

PM Skills 是一个**产品经理助手**。你把需求、文档、想法告诉它，它帮你：

- 把乱七八糟的需求整理清楚
- 写出正式的 PRD（产品需求文档）
- 生成可跑的原型骨架代码

整个过程就像和一个很专业的产品经理聊天。

## 安装

一台电脑（Windows 或 Mac），能上网。下面 3 步按顺序装好：

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

1. 打开 https://github.com/EthanSMC/pm-skills
2. 点击绿色 **Code** 按钮 → **Download ZIP**
3. 解压到你喜欢的地方
4. 把 `skills/pm-skills/` 下的所有文件夹复制到你的项目里：

```
你的项目/.claude/skills/
  pm-workflow/SKILL.md
  pm-knowledge/SKILL.md          + scripts/
  pm-personalize/SKILL.md
  prd-reconcile/SKILL.md
  pm-brainstorming/SKILL.md
  visual-companion/SKILL.md      + scripts/
  write-prd/SKILL.md
  prototyping/SKILL.md           + spec-document-reviewer-prompt.md
```

> 每个 skill 是一个文件夹，里面有一个 `SKILL.md`。`pm-knowledge` 和 `visual-companion` 还有各自的 `scripts/` 子目录，一起复制过去就行。

5. 重启 Claude Code，输入 `/` 应能看到这些 skill

### 第 4 步（可选增强）：装 MinerU Document Explorer

知识引擎的增强模式依赖 qmd。**不装也能用**（自动降级为文件系统检索），但装了检索更精准：

```bash
npm install -g mineru-document-explorer
pip install pymupdf python-docx python-pptx
```

验证：`qmd --version`

装好后，在你的项目的 `.claude/settings.json` 中追加：

```json
{
  "mcpServers": {
    "qmd": { "command": "qmd", "args": ["mcp"] }
  }
}
```

### 第 5 步（可选）：Python 工具脚本

pm-knowledge 自带 scripts/，需 Python 依赖：

```bash
pip install pyyaml pytest
```

脚本命令：
- `python .claude/skills/pm-knowledge/scripts/pm-wiki-graph.py build` — 构建 `.pm-wiki/` 知识图谱
- `python .claude/skills/pm-knowledge/scripts/pm-wiki-lint.py confidence` — 计算页面置信度评分
- `python .claude/skills/pm-knowledge/scripts/pm-wiki-crystallize.py session-end` — 从工作笔记提取知识页

### 验证

进入你的项目文件夹，启动 Claude Code：

```
cd 你的项目路径
claude
```

输入 `/`，看到 pm-workflow、pm-brainstorming 等 skill 名字就说明装好了。

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

**"command not found"** → 检查 Node.js 和 Claude Code 是否装好

**Claude Code 无响应** → 网络问题，需联网访问 Anthropic 服务

**Skill 命令不生效** → 检查 `.claude/skills/` 下是否有 `SKILL.md` 文件，文件夹名是否正确

**知识检索不够精准** → 安装 MinerU (qmd)，见"第 4 步（可选增强）"

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
| `pm-personalize` | 从项目库提炼通用知识到个人库 | 显式调用或 ingest 后自动建议 |
| `prd-reconcile` | 多文档合并与消歧 | 多份PRD/需求文档需合并时 |
| `pm-brainstorming` | 需求探索与设计 | 创建新功能/组件前 |
| `visual-companion` | 浏览器端可视化辅助 | brainstorming 中视觉问题 |
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
    spec-document-reviewer-prompt.md
```

</details>

## License

MIT