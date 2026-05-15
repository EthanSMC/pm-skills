---
name: pm-knowledge
description: "PM 知识引擎（内部子 skill，由 pm-workflow 调度）— 文档摄入、知识检索、知识组织"
---

# PM Knowledge — 产品经理知识引擎

为 PM 工作流提供知识基础设施。负责摄入各种格式的文档，按 PM 维度组织知识、支持语义检索和 wiki 维护，为 pm-brainstorming 和需求分析提供知识支撑。

## 当由 pm-workflow 调度时

pm-workflow 在阶段 0（知识准备）使用 Skill 工具调用此 skill。

### 交接参数

| 参数 | 值 |
|------|------|
| **输入** | 用户任务描述 + raw/ 目录状态 + manifest 变化检测结果 |
| **输出** | 知识摘要（传递给阶段1 pm-brainstorming） |
| **知识写回** | .pm-wiki/ 各子目录 + raw-manifest 更新 |

### 执行后交接

完成后，向 pm-workflow 汇报：
- 知识库新增/修改的文件路径和摘要
- 知识摘要要点（3-5条关键发现）
- 知识缺口说明

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
| qmd 未安装 | 纯文件系统操作 — 直接读写 `.pm-wiki/` markdown 文件 |

降级检测：在 skill 启动时执行 `qmd --version`，如果失败则标记为 "降级模式"，后续操作自动切换到文件系统方式。

## 双库架构

PM 知识分两层存储，维度不同、职责不同：

```
个人知识库: ~/.pm-wiki/ 维度：你这个人 — 跨项目积累，随你走
  ├── skills/                     我掌握的技能、能力模型、成长记录
  ├── insights/                   行业洞察、产品思考、经验教训
  ├── industry/                   行业知识、市场数据、趋势报告
  ├── templates/                  我积累的模板、框架、checklist
  ├── methods/                    PM 方法论、工作流、最佳实践
  ├── tools/                      工具使用心得、配置、对比
  └── reusable/                   可复用的知识片段（跨项目引用）

项目知识库: <project>/.pm-wiki/ 维度：这个项目 — 项目专属，聚焦具体产品
  ├── context/                    项目背景、目标、愿景、干系人
  ├── requirements/               需求文档、用户故事、验收标准
  ├── constraints/                技术约束、业务约束、假设、依赖
  ├── decisions/                  产品决策记录（ADR）
  ├── (market/)                   项目相关市场、赛道、规模（按需）
  ├── (competitors/)              项目相关竞品分析（按需）
  ├── (users/)                    项目目标用户、画像、痛点（按需）
  ├── (synthesis/)                综合分析、机会点、风险评估（按需）
  ├── (references/)               → 链接到个人知识库（按需）
  ├── _working/                   L0: 工作记忆（当前会话临时草稿）
  ├── _semantic/                  L2: 语义记忆（跨模式提炼的通用知识）
  ├── _procedural/                L3: 程序记忆（内化的操作规程）
  └── _generated/                 自动产出索引（勿手动编辑）

原始文档: <project>/raw/  维度：知识摄入队列（进入即摄入，不是归档）
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
  → 1. 项目知识库 (<project>/.pm-wiki/)  项目上下文最相关
  → 2. 个人知识库 (~/.pm-wiki/) 个人积累兜底
  → 3. 原始文档 Deep Read (回源)             回到源头
```

## Raw 管理 — 源文件组织与追踪

`raw/` 目录是知识摄入的**暂存队列**，不是归档仓库。每个进入 `raw/` 的文件都必须被摄入。

### 0.1 Raw Discovery — 散落文件识别

当用户有散落在项目各处的文件时，帮助识别哪些应该进入 `raw/`：

**扫描范围**：
- 项目根目录及一级子目录中的文档文件（.pdf, .docx, .pptx, .md）
- 排除明显非 PM 相关的文件（代码文件、配置文件、.git/、node_modules/ 等）

**识别流程**：
1. 扫描项目目录，列出所有潜在的源文件
2. 排除已在 `raw/`、`.pm-wiki/`、`docs/pm/` 等目录中的文件
3. 对每个候选文件给出简短说明（文件名、大小、类型）
4. 向用户呈现候选列表，让用户确认哪些需要进入 `raw/`
5. 用户确认后，将文件复制到 `raw/`（保留原位置，不移动）

**排除规则**（自动跳过，不呈现给用户）：

| 模式 | 原因 |
|------|------|
| `*.js`, `*.ts`, `*.py`, `*.go` 等 | 代码文件，非 PM 知识 |
| `*.json`, `*.yaml`, `*.toml` | 配置文件 |
| `.git/`, `node_modules/`, `.claude/` | 工具/依赖目录 |
| `README.md`, `CLAUDE.md` | 项目元文件，已有独立用途 |
| `*.log`, `*.tmp` | 临时文件 |

### 0.2 Raw Manifest — 变化检测

使用 `.pm-wiki/_generated/raw-manifest.md` 追踪 `raw/` 中每个文件的摄入状态：

```markdown
## Raw Manifest

| 文件 | 状态 | 摄入时间 | 文件修改时间 | docid |
|------|------|---------|------------|-------|
| 竞品分析报告.pdf | ingested | 2026-05-07 | 2026-05-06 | #abc123 |
| 用户调研Q1.docx | ingested | 2026-05-07 | 2026-05-05 | #def456 |
| 新需求文档.md | pending | - | 2026-05-14 | - |
```

**变化检测逻辑**（每次 pm-workflow 启动时执行）：
1. 读取 raw-manifest.md，获取已摄入文件列表
2. 扫描当前 `raw/` 目录，获取实际文件列表
3. 对比两者：
   - manifest 中不存在 → **新文件**，标记为 `pending`
   - manifest 中文件修改时间与实际不同 → **文件有变化**，标记为 `changed`
   - manifest 中 `pending` → **尚未摄入**，需要处理
4. 如有 pending/changed 文件，自动触发 ingest 流程

### 0.3 自动创建 raw/

每次 pm-workflow 启动时：
- 检查 `<project>/raw/` 是否存在，不存在则自动创建
- 检查 `.pm-wiki/_generated/raw-manifest.md` 是否存在，不存在则自动创建
- 执行变化检测，发现 pending/changed 文件时自动触发 ingest

### 0.4 设计原则

- **进入即摄入** — 每个进入 `raw/` 的文件都必须走 ingest 流程
- **溯源不删** — 摄入完成后，文件保留在 `raw/` 作为溯源依据，manifest 标记为 `ingested`
- **变化重摄入** — 源文件有更新时（修改时间变化），自动重新摄入
- **不在 raw 就不摄入** — 只有 `raw/` 中的文件才会被摄入，散落文件需先经 Raw Discovery 识别

## 三大操作

### 1. Ingest — 知识摄入

当用户提供新文档时，按以下流程处理：

**支持格式：** Markdown (.md), PDF (.pdf), Word (.docx), PowerPoint (.pptx)

#### Step 0: 确认文档在 raw/ 中

所有待摄入的文档必须在 `<project>/raw/` 目录中（见 Raw 管理）：
- 如文档不在 `raw/` 中，先通过 Raw Discovery 流程让用户确认后复制进来
- 文件路径用于 `wiki_ingest` 的 source 参数
- 摄入完成后更新 raw-manifest.md，文件保留在 `raw/` 作为溯源依据

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

#### Step 7: 更新 Raw Manifest

摄入完成后，更新 `.pm-wiki/_generated/raw-manifest.md`：
- 将文件状态从 `pending`/`changed` 更新为 `ingested`
- 记录摄入时间、docid、文件修改时间
- 下次 pm-workflow 启动时，manifest 与实际 `raw/` 对比即可发现变化

### 2. Query — 知识检索

**触发时机：**
- 用户直接提问
- pm-brainstorming skill 开始前自动调用（见衔接逻辑）

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
1. 使用 Grep/Glob 工具在 `.pm-wiki/` 目录中搜索
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
1. 检查 `.pm-wiki/` 下是否存在 `[待审]` 标记的页面
2. 列出没有 `---` frontmatter 的页面（格式不规范）
3. 检查 `references/` 中的链接是否指向有效文件
4. 报告超过 30 天未更新的页面

**PM 维度额外检查（工具脚本可用时）**：
- `pm-wiki-lint.py confidence` — 重算置信度分数
- `pm-wiki-lint.py supersession` — 检查矛盾对建议取代
- `pm-wiki-lint.py stale` — 列出>90天未确认页面
- `pm-wiki-lint.py orphans` — 列出无引用孤立页面
- `pm-wiki-lint.py broken_refs` — 检查关系引用有效性

## 4. Graph层 + Typed Relations

### 4.1 Relations语法

Relations 作为元数据放在 frontmatter（不在正文）。5种PM专用关系类型：

| 类型 | 语义 | 方向 |
|------|------|------|
| `references` | 引用/参考 | 单向 |
| `depends_on` | 依赖/前置 | 单向 |
| `derived_from` | 推导来源 | 单向 |
| `supersedes` | 取代 | 单向 |
| `contradicts` | 矛盾 | 双向 |

实体类型6种：`decision` / `concept` / `person` / `project` / `document` / `component`

示例 frontmatter：
```yaml
---
relations:
  references: ["checkpoint-form-mapping"]
  depends_on: ["prd-conflict-analysis"]
  derived_from: ["运营管理平台-PRD.docx"]
  supersedes: ["旧版状态体系"]
  contradicts: []
entities:
  - {type: decision, name: "C12-节点挂起主任务不回退"}
---
```

Wiki link不带 `.md` 扩展名，脚本自动匹配实际文件。

### 4.2 目录新增

- `_generated/` — 自动产出索引，勿手动编辑
  - `entities.md` — pm-wiki-graph.py build 产出
  - `relations.md` — pm-wiki-graph.py build 产出
  - `raw-manifest.md` — raw/ 文件摄入状态追踪（pm-knowledge 维护）

### 4.3 工具脚本：pm-wiki-graph.py

| 命令 | 用途 | 调用方式 |
|------|------|---------|
| `build` | 解析所有页面frontmatter → 生成 `_generated/` 索引 | `python scripts/pm-wiki-graph.py --wiki .pm-wiki build` |
| `traverse <entity>` | 从实体出发走图 → 返回关联页面 | `python scripts/pm-wiki-graph.py --wiki .pm-wiki traverse "C12决策"` |
| `traverse <entity> --relation <type>` | 限定关系类型走图 | 加 `--relation references` |
| `query <topic>` | build + traverse 扩展 | `python scripts/pm-wiki-graph.py --wiki .pm-wiki query "挂起规则"` |

**降级**：脚本不可用时，Grep扫描 frontmatter 的 `relations:` 字段，手动构建关联。

### 4.4 检索流程（更新Section 2）

原流程：BM25 + vector → rerank → 返回

新流程（三流RRF融合）：
```
用户提问
  → Stream 1: qmd query (BM25 + vector + rerank) → 命中 S1
  → Stream 2: pm-wiki-graph.py traverse → 从 S1 沿关系扩展 → 命中 S2
  → RRF融合: score = 1/(k + rank_S1) + 1/(k + rank_S2), k=60
  → 去重排序 → 返回（标注来源：BM25/Vector/Graph）
```

检索时 confidence < 0.3 的页面默认不返回。superseded 页面默认排除。

**模式A增强（Graph层可用时）**：
1. 先执行上述 qmd query 流程 → 得到候选页面 S1
2. 执行 `python scripts/pm-wiki-graph.py --wiki .pm-wiki traverse <key_entity>` → 从 S1 沿关系扩展得到 S2
3. RRF融合：`score = 1/(k + rank_S1) + 1/(k + rank_S2)`，k=60
4. 去重排序返回，标注来源（BM25/Vector/Graph）

## 5. 置信度与 Supersession

### 5.1 Frontmatter新增字段

```yaml
confidence: 0.8          # 0-1，多源+近期=高，单一+久未验证=低
superseded_by: null       # null=当前有效，有值=已被取代
last_confirmed: 2026-05-07  # 最近确认日期
```

新字段可选。缺省时：confidence按单一来源(0.4)计算，superseded_by=null，last_confirmed=写入日期。

### 5.2 置信度计算

| 因素 | 影响 |
|------|------|
| 多源确认（每+1独立来源） | +0.2 |
| 单一来源 | 基础 0.4 |
| 30天内确认 | +0.2 |
| 90天未确认 | -0.2 |
| 有 contradicts 关系 | -0.3 |
| 已被取代（superseded_by有值） | 置0 |

范围 [0, 1]。confidence < 0.3 默认不返回。

### 5.3 Supersession流程

1. 新页面写入 → 检查 `contradicts` 关系
2. 发现矛盾 → 提示用户："[[A]] 与 [[B]] 矛盾，是否确认 A取代B？"
3. 用户确认 → 旧页面写入 `superseded_by: "A"`，confidence置0
4. 旧页面顶部加：`> [已取代] 此页面已被 [[A]] 取代 (日期)`
5. 旧页面保留不删除，检索时默认排除

### 5.4 工具脚本：pm-wiki-lint.py

| 命令 | 用途 | 调用方式 |
|------|------|---------|
| `confidence` | 重算置信度 → 更新frontmatter | `python scripts/pm-wiki-lint.py --wiki .pm-wiki confidence` |
| `supersession` | 检查矛盾对 → 建议取代 | `python scripts/pm-wiki-lint.py --wiki .pm-wiki supersession` |
| `stale` | 列出>90天未确认页面 | `python scripts/pm-wiki-lint.py --wiki .pm-wiki stale` |
| `orphans` | 列出无引用的孤立页面 | `python scripts/pm-wiki-lint.py --wiki .pm-wiki orphans` |
| `broken_refs` | 检查关系引用是否有效 | `python scripts/pm-wiki-lint.py --wiki .pm-wiki broken_refs` |

**降级**：脚本不可用时，Grep扫描frontmatter手动检查。

## 6. 分层记忆与 Crystallization

### 6.1 四层架构

```
L0 _working/     — 工作记忆（当前会话临时草稿）
L1 (已有目录)    — 插曲记忆（项目事实、决策、约束）
L2 _semantic/    — 语义记忆（跨模式提炼的通用知识）
L3 _procedural/  — 程序记忆（内化的操作规程）
```

### 6.2 升级路径

| 触发条件 | 升级 | 执行 |
|---------|------|------|
| 会话结束 | L0→L1 | pm-wiki-crystallize.py session-end |
| 同tags出现≥3次 | L1→L2 | pm-wiki-crystallize.py distill |
| 模式多次成功应用 | L2→L3 | pm-wiki-crystallize.py codify |

### 6.3 _working/生命周期

- 会话开始：创建 `session-YYYY-MM-DD.md`
- 会话中：追加临时笔记、未定结论
- 会话结束：session-end → 写入L1 → 清理（保留最近1次）

### 6.4 _semantic/ 和 _procedural/ 内容

`_semantic/`: patterns.md / heuristics.md / anti-patterns.md / templates.md
`_procedural/`: checklists.md / workflows.md / decision-frameworks.md

### 6.5 工具脚本：pm-wiki-crystallize.py

| 命令 | 用途 | 调用方式 |
|------|------|---------|
| `session-end` | _working/ → L1提取+清理 | `python scripts/pm-wiki-crystallize.py --wiki .pm-wiki session-end` |
| `distill` | L1 → _semantic/ 蒸馏 | `python scripts/pm-wiki-crystallize.py --wiki .pm-wiki distill` |
| `codify` | _semantic/ → _procedural/ 固化 | `python scripts/pm-wiki-crystallize.py --wiki .pm-wiki codify` |

**降级**：脚本不可用时，手动读取 `_working/` → 提取 → 写入正式目录。

## 7. Event-driven Hooks

PM workflow执行时自动触发的6个钩子：

| Hook | 触发时机 | 自动动作 | 实现 |
|------|---------|---------|------|
| `on_new_source` | 用户提供新文档 | ingest → extract entities → build graph → check contradictions → suggest supersession | pm-knowledge Ingest流程 |
| `on_session_start` | pm-brainstorming/prototyping启动前 | query项目库 → 注入知识摘要 → 标注缺口 | pm-knowledge→pm-brainstorming衔接（已有） |
| `on_session_end` | 会话结束 | compress → _working/ → crystallize到L1 | pm-wiki-crystallize.py session-end |
| `on_query` | 知识检索后 | 检查是否值得回写wiki | pm-knowledge Query流程 |
| `on_memory_write` | 写入wiki页面时 | 检查contradicts → 建议supersession → 更新confidence | pm-wiki-lint.py supersession |
| `on_schedule` | 定期 | confidence衰减 + stale标记 + distill | CronCreate |

`on_schedule`频率建议：每周confidence衰减 + 每月distill。

## PM Wiki Schema

每个 wiki 页面应包含以下 frontmatter：

```markdown
---
type: fact | analysis | recommendation | reference
status: confirmed | pending-review | draft
confidence: 0.8
superseded_by: null
last_confirmed: 2026-05-07
source: <原始文档路径或链接>
ingested: YYYY-MM-DD
updated: YYYY-MM-DD
project: <项目名 | personal>
tags: [market, competitor, user-research, ...]
entities:
  - {type: decision, name: "C12-节点挂起主任务不回退"}
  - {type: concept, name: "防呆确认"}
relations:
  references: ["checkpoint-form-mapping"]
  depends_on: ["prd-conflict-analysis"]
  derived_from: ["运营管理平台-PRD.docx"]
  supersedes: ["旧版状态体系"]
  contradicts: []
---
```

新增字段（confidence/superseded_by/last_confirmed/entities/relations）为可选，缺省时按旧模式工作。

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

当 pm-brainstorming skill 启动时，自动执行以下步骤：

1. **识别主题** — 从用户的任务描述中提取关键概念
2. **知识检索** — 按 Query 流程检索项目库 + 全局库中的相关知识
3. **知识摘要** — 将检索结果整理为摘要，注入到 pm-brainstorming 的上下文中
4. **标注来源** — 明确标注哪些是已有知识，哪些是需要探索的新领域

输出格式（注入到 pm-brainstorming 上下文）：
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
| prd-reconcile | `synthesis/` + `decisions/` | 冲突分析 + 决策记录 |
| pm-brainstorming | `decisions/` | 设计决策（WHY/WHAT/WHY NOT） |
| write-prd | `requirements/` | 功能需求摘要 + 优先级 |
| prototyping (技术规格) | `decisions/` + `constraints/` | 架构决策 + 新约束 |
| prototyping (实施计划) | `decisions/` + `constraints/` | 计划中的决策 + 约束 |
| prototyping (骨架构建) | `constraints/` + `_working/` | 新发现的约束/假设 + 临时笔记 |
| prototyping (审查) | `synthesis/` | 问题模式、成功经验 |
| prototyping (验证) | `log.md` | 验证结果记录 |
| prototyping (分支管理) | `log.md` + `synthesis/` | 工作流摘要 + 成功经验 |

每次写入后，在 `.pm-wiki/log.md` 中追加记录。

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
- **raw 是队列不是仓库** — 进入 raw/ 的文件必须被摄入，摄入后保留但标记已处理；每次工作流启动检查 raw/ 变化
