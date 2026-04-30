---
name: pm-knowledge
description: "PM 知识管理模块 — 摄入、组织、检索产品相关知识，为需求分析和 brainstorming 提供知识基础。基于 MinerU Document Explorer (qmd)，支持 MCP/CLI/文件系统三级降级。"
---

# PM Knowledge — 产品经理知识引擎

为 PM 工作流提供知识基础设施。负责摄入各种格式的文档，按 PM 维度组织知识、支持语义检索和 wiki 维护，为 brainstorming 和需求分析提供知识支撑。

## 前置依赖

本 skill 依赖 MinerU Document Explorer (qmd)。

### 安装

```bash
npm install mineru-document-explorer
# 安装后全局可用 qmd 命令
# 也可单独全局安装：
npm install -g mineru-document-explorer
# 验证
qmd --version
```

### 初始化（首次使用或新项目中）

每次在新项目中使用 pm-knowledge 前，执行以下初始化：

```bash
# 1. 验证 qmd 可用
qmd --version

# 2. 检查/创建项目知识库 collection
qmd collection list | grep pm-project
# 如果不存在，手动创建（注意：qmd 会将 collection name 解析为相对于 cwd 的路径）
# 推荐使用 qmd collection add pm-project 在当前目录下创建子目录

# 3. 检查/创建个人知识库 collection
qmd collection list | grep pm-personal

# 4. 生成向量嵌入（启用语义搜索）
qmd embed

# 5. 验证 MCP 连通性
echo '{"jsonrpc":"2.0","id":1,"method":"initialize","params":{"protocolVersion":"2024-11-05","capabilities":{},"clientInfo":{"name":"test","version":"1.0"}}}' | qmd mcp 2>/dev/null | head -1
# 应返回 {"jsonrpc":"2.0","id":1,"result":{...}}
```

### MCP 配置

确保 `.claude/settings.json` 中已配置：

```json
{
  "mcpServers": {
    "qmd": {
      "command": "qmd",
      "args": ["mcp"]
    }
  }
}
```

### 降级策略

当 MCP 不可用时，按以下优先级降级：

| 可用性 | 使用方式 |
|--------|---------|
| MCP 连接正常 | 通过 MCP 工具调用（推荐） |
| MCP 不可用，CLI 可用 | Bash 调用 `qmd query`、`qmd wiki` 等命令 |
| qmd 未安装 | 纯文件系统操作 — 直接读写 `.project-wiki/` markdown 文件 |

降级检测：在 skill 启动时执行 `qmd --version`，如果失败则标记为 "降级模式"，后续操作自动切换到文件系统方式。

## 双库架构

PM 知识分两层存储，维度不同、职责不同：

```
个人知识库: %USERPROFILE%/.personal-wiki/ 维度：你这个人 — 跨项目积累，随你走
  ├── skills/                     我掌握的技能、能力模型、成长记录
  ├── insights/                   行业洞察、产品思考、经验教训
  ├── industry/                   行业知识、市场数据、趋势报告
  ├── templates/                  我积累的模板、框架、checklist
  ├── methods/                    PM 方法论、工作流、最佳实践
  ├── tools/                      工具使用心得、配置、对比
  └── reusable/                   可复用的知识片段（跨项目引用）

项目知识库: <project>/.project-wiki/ 维度：这个项目 — 项目专属，聚焦具体产品
  ├── context/                    项目背景、目标、愿景、干系人
  ├── requirements/               需求文档、用户故事、验收标准
  ├── constraints/                技术约束、业务约束、假设、依赖
  ├── decisions/                  产品决策记录（ADR）
  ├── (market/)                   项目相关市场、赛道、规模（按需）
  ├── (competitors/)              项目相关竞品分析（按需）
  ├── (users/)                    项目目标用户、画像、痛点（按需）
  ├── (synthesis/)                综合分析、机会点、风险评估（按需）
  └── (references/)               → 链接到个人知识库（按需）

原始文档: <project>/raw/  维度：待摄入的原始材料
```

### 两库的关系

```
个人知识库                          项目知识库
┌──────────────┐                   ┌──────────────┐
│ skills       │←──── 引用 ────────│ context      │
│ insights     │←──── 引用 ────────│ requirements │
│ industry     │←──── 引用 ────────│ constraints  │
│ templates    │←──── 复用 ────────│ decisions    │
│ methods      │←──── 应用 ────────│ (market)     │
│ tools        │←──── 使用 ────────│ (competitors)│
│ reusable     │←──── 嵌入 ────────│ (users)      │
└──────────────┘                   │ (synthesis)  │
                                   │ (references) │──→ 指向个人知识库
                                   └──────────────┘

写入规则：
- 通用性知识 → 个人知识库（行业数据、方法论、模板）
- 项目特异性知识 → 项目知识库（需求、决策、竞品对比）
- 不确定时 → 先写项目知识库，后续提炼到个人知识库

引用规则：
- 项目知识库通过 references/ 目录链接到个人知识库的具体页面
- 引用格式：→ [个人知识库] <分类>/<页面名>.md
- 项目知识库不复制个人知识库的内容，只引用
```

### 查询优先级

```
用户提问
  → 1. 项目知识库 (<project>/.project-wiki/)  项目上下文最相关
  → 2. 个人知识库 (%USERPROFILE%/.personal-wiki/) 个人积累兜底
  → 3. 原始文档 Deep Read (回源)             回到源头
```

## 三大操作

### 1. Ingest — 知识摄入

当用户提供新文档时，按以下流程处理：

**支持格式：** Markdown (.md), PDF (.pdf), Word (.docx), PowerPoint (.pptx)

#### Step 0: 保存原始文档

所有待摄入的文档先保存到 `<project>/raw/` 目录：
- 保留原始文件名
- 文件路径用于 `wiki_ingest` 的 source 参数
- 摄入完成后，raw 目录的文档作为溯源依据保留

#### Step 1: 确定目标库
- 项目特异性内容（竞品对比、目标用户、需求）→ 项目知识库
- 通用性内容（行业数据、方法论、工具心得）→ 个人知识库
- 可复用结论（跨项目通用的模式、模板）→ 先写项目库，提炼后归档到个人库
- 不确定时询问用户

#### Step 2: 分析文档 (wiki_ingest)

分析文档内容，为 wiki 页面创建提供上下文：

**MCP 模式：** 调用 `wiki_ingest(source, wiki=<collection_name>)`
**CLI 模式：** `qmd wiki ingest <source_file> --wiki <collection>`

`wiki_ingest` 是**增量**的：如果文档未变化，会跳过。首次摄入会返回文档的 `docid` (#abc123)，后续步骤用这个 ID。

#### Step 3: 深度阅读 (doc_toc + doc_read)

对于大型文档（PDF、长 MD），先获取结构，再按需读取章节：

**MCP 模式：** `doc_toc(docid)` → 获取章节地址 → `doc_read(docid, [addresses])`
**CLI 模式：** `qmd doc-toc <docid>` → `qmd doc-read <docid> <addr>`

不同格式的寻址方式不同：
- Markdown: `line:45-120`（行号范围）
- PDF: `page:3`（页码）
- PPTX: `slide:5`（幻灯片）
- DOCX: `section:heading_name`（按标题分段）

需要提取表格、图表、公式时：
- MCP: `doc_elements(docid, types=["table", "figure"])`
- CLI: `qmd doc-read` 配合 `doc_grep` 提取结构化内容

#### Step 4: 按 PM Schema 分类整理 (doc_write)

从文档中提取知识，按 PM 维度生成 wiki 页面内容，然后写入：

**MCP 模式：** 调用 `doc_write(wiki=<collection>, path="<category>/<page>.md", content="<markdown_with_frontmatter>", source="<docid>")`
**CLI 模式：** `echo "<content>" | qmd wiki write <collection> <path> --source <docid>`

页面内容必须符合 PM Wiki Schema（见下方），frontmatter 必须包含 `source`、`type`、`status`、`ingested`。

分类映射参考：
| 文档内容 | 写入路径 |
|---------|---------|
| 竞品分析 | `competitors/<竞品名>.md` |
| 用户画像/调研 | `users/<主题>.md` |
| 市场/行业数据 | `market/<主题>.md` |
| 项目背景/目标 | `context/<主题>.md` |
| 需求/用户故事 | `requirements/<主题>.md` |
| 约束/假设 | `constraints/<主题>.md` |
| 产品决策 | `decisions/<决策名>.md` |

#### Step 5: 审核分流

| 内容类型 | 处理方式 | 示例 |
|---------|---------|------|
| 事实性 | 自动写入 | 数据指标、功能列表、用户原话、文档引用 |
| 结构性 | 自动写入 | 目录更新、索引、交叉链接、日志条目 |
| 分析性 | **草稿待审** | 竞品对比结论、痛点归纳、趋势判断 |
| 推荐性 | **草稿待审** | 优先级建议、风险评估、Go/No-Go 判断 |

审核流程：
- 分析性/推荐性内容写入 wiki 时，在页面顶部标记 `> [待审]` 标签
- 向用户呈现待审内容摘要，等待确认或修改
- 用户确认后移除待审标签

#### Step 6: 健康检查 (wiki_lint)

**MCP 模式：** `wiki_lint()`
**CLI 模式：** `qmd wiki lint`

检查孤儿页面、过时页面、待审状态。

### 2. Query — 知识检索

**触发时机：**
- 用户直接提问
- brainstorming skill 开始前自动调用（见衔接逻辑）

**检索流程：**

#### 模式 A：MCP 可用
1. `query(text, intent="<context>", minScore=0.5)` — 混合搜索（BM25 + vector + rerank）
2. 精确需求时可用高级模式：`query(searches=[{type:"lex", query:"关键词"}, {type:"vec", query:"语义"}])`
3. 找到相关文档后，`get(docid_or_path)` 读取全文
4. 大型文档走深读：`doc_toc(docid)` → `doc_read(docid, [addresses])`
5. 按优先级路由：项目库 → 全局库

#### 模式 B：CLI 可用（MCP 不可用时）
1. 解析用户意图，提取关键词和概念
2. 执行 `qmd query "<query>" -n 5` — 混合检索（BM25 + vector + rerank）
3. 如果需要更精确：`qmd query $'lex: <关键词>\nvec: <语义>' -n 5`
4. 按优先级路由：项目库 → 全局库
5. 如果 wiki 知识不足以回答，回源到原始文档：
   - `qmd doc-toc <docid>` 获取文档结构（PDF 显示 pages，MD 显示 headings）
   - `qmd doc-read <docid> <addr>` 读取具体章节
   - `qmd doc-grep <docid> <pattern>` 在文档内搜索关键词
6. 综合结果，附上来源引用返回

#### 模式 C：纯文件系统（qmd 不可用时）
1. 使用 Grep/Glob 工具在 `.project-wiki/` 目录中搜索
2. 直接读取相关 markdown 文件
3. 按 frontmatter 的 tags、type 字段过滤

**输出格式：**
```
## 回答

[综合回答内容]

**来源：**
- [项目知识库] competitors/产品A.md — 竞品功能对比
- [个人知识库] industry/趋势2026.md — 市场数据
- [原始文档] reports/用户调研Q1.pdf §3.2 — 用户原话

**检索模式：** MCP | CLI | 文件系统
```

### 3. Lint — 知识健康检查

定期（或用户主动触发）执行：

**MCP/CLI 可用时：**
1. MCP: `wiki_lint()` / CLI: `qmd wiki lint` — 检查 wiki 结构健康
2. PM 维度额外检查：
   - 孤儿页面（没有被引用的知识页）
   - 过时数据（超过时效的事实性内容）
   - 未处理的待审内容
   - 跨库引用是否有效
3. `wiki_log()` / `qmd wiki log` — 查看最近的操作日志
4. 建议新的摄入方向（基于已有知识缺口）

**文件系统降级（qmd 不可用时）：**
1. 检查 `.project-wiki/` 下是否存在 `[待审]` 标记的页面
2. 列出没有 `---` frontmatter 的页面（格式不规范）
3. 检查 `references/` 中的链接是否指向有效文件
4. 报告超过 30 天未更新的页面

## PM Wiki Schema

每个 wiki 页面应包含以下 frontmatter：

```markdown
---
type: fact | analysis | recommendation | reference
status: confirmed | pending-review | draft
source: <原始文档路径或链接>
ingested: YYYY-MM-DD
updated: YYYY-MM-DD
project: <项目名 | personal>
tags: [market, competitor, user-research, ...]
---
```

### 页面模板

**竞品页面** (`competitors/<名称>.md`)：
```markdown
---
type: fact
status: confirmed
tags: [competitor]
---
# <竞品名称>

## 概述
[一句话描述]

## 核心功能
[功能列表]

## 定价
[定价信息]

## 优劣势
| 优势 | 劣势 |
|------|------|
| ... | ... |

## 与我方对比
[对比分析] (待审标记如适用)

## 来源
- [原始文档引用]
```

**用户研究页面** (`users/<主题>.md`)：
```markdown
---
type: fact | analysis
status: confirmed | pending-review
tags: [user-research]
---
# <研究主题>

## 用户画像
[画像描述]

## 核心发现
[发现列表，每条附来源]

## 痛点
[痛点列表]

## 引用
> "用户原话" — 来源

## 来源
- [原始文档引用]
```

**综合分析页面** (`synthesis/<主题>.md`)：
```markdown
---
type: analysis | recommendation
status: pending-review
tags: [synthesis]
---
# <分析主题>

> [待审] 本页包含分析性内容，请审核后确认

## 要点
[分析要点]

## 机会点
[机会列表]

## 风险
[风险列表]

## 建议
[建议列表]

## 来源
- [引用的知识库页面]
```

## 与 Brainstorming 的衔接

### 知识注入（Brainstorming 前置）

当 brainstorming skill 启动时，自动执行以下步骤：

1. **识别主题** — 从用户的任务描述中提取关键概念
2. **知识检索** — 按 Query 流程检索项目库 + 全局库中的相关知识
3. **知识摘要** — 将检索结果整理为摘要，注入到 brainstorming 的上下文中
4. **标注来源** — 明确标注哪些是已有知识，哪些是需要探索的新领域

输出格式（注入到 brainstorming 上下文）：
```
## 已有知识基础

### 市场背景
[从 wiki 检索的市场知识摘要]

### 竞品情况
[从 wiki 检索的竞品知识摘要]

### 用户洞察
[从 wiki 检索的用户知识摘要]

### 知识缺口
- [ ] 尚未研究的竞品：XXX
- [ ] 缺少目标用户群的调研数据
- [ ] 未找到 XXX 方面的市场数据
```

### 知识回写（各阶段各自负责）

不需要集中的"知识回写"阶段，各阶段直接写入对应目录：

| 阶段 | 写入路径 | 内容 |
|------|---------|------|
| brainstorming | `decisions/` | 设计决策（WHY/WHAT/WHY NOT） |
| write-prd | `requirements/` | 功能需求摘要 + 优先级 |
| 实施中 | `constraints/` | 新发现的约束/假设 |
| review | `synthesis/` | 问题模式、成功经验 |

每次写入后，在 `.project-wiki/log.md` 中追加记录。

## 操作日志

每次 ingest/query/lint 操作都在对应的 wiki 目录下追加 `log.md`：

```markdown
## [YYYY-MM-DD HH:mm] ingest | <文档名>
- 目标库: 项目 / 全局
- 分类: market/competitors/users/requirements/synthesis
- 状态: 自动写入 / 待审
- 摘要: <一句话描述摄入了什么>

## [YYYY-MM-DD HH:mm] query | <查询内容>
- 命中: 项目库 X 条 / 全局库 Y 条
- 回源: <是否需要回源到原始文档>

## [YYYY-MM-DD HH:mm] lint
- 发现问题: <问题列表>
- 建议: <建议列表>
```

## 关键原则

- **项目优先** — 查询时项目知识库优先于个人知识库
- **两库分离** — 项目知识是项目的，个人知识是你的；项目结束，个人知识留下
- **引用不复制** — 项目知识库通过 references/ 链接个人知识库，不复制内容
- **事实自动，分析待审** — 事实性内容自动写入，分析性内容需要用户确认
- **来源可溯** — 每条知识都要附上来源引用
- **知识缺口显式化** — 主动识别和标注知识盲区
- **知识提炼** — 当一次 ingest 后新增或修改超过 3 个页面时，主动建议用户调用 `/pm-personalize` 提炼通用知识到个人库
- **不重复造轮子** — 所有文档解析、检索、wiki 维护的底层工作委托给 MinerU (qmd)
- **三级降级** — MCP → CLI → 文件系统，任一层级可用即可工作
