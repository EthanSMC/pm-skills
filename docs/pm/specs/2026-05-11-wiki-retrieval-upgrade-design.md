# PM Knowledge Wiki 检索升级设计

**Goal:** 补齐 pm-knowledge 与 LLM Wiki v2 的4项核心差距——知识图谱+Graph遍历、置信度+Supersession、分层记忆+Crystallization、Event-driven Hooks。实现方式：skill文档增量补丁 + 工具脚本。

**Architecture:** 在现有 pm-knowledge.md 上叠加4个新章节（4-7），wiki目录新增 `_generated/`、`_working/`、`_semantic/`、`_procedural/`，新增3个工具脚本（graph/lint/crystallize）。保持向后兼容，qmd MCP仍是主检索引擎，graph脚本作为第三流补充。

**Tech Stack:** Python 3 (工具脚本) + YAML frontmatter (relations/entities/confidence) + qmd MCP (BM25+vector+rerank) + Claude Code CronCreate (event hooks)

---

## 1. Graph层 + Typed Relations

### 1.1 Relations 语法 — YAML frontmatter

Relations 作为元数据放在 frontmatter，不放在正文：

```yaml
---
type: decision
status: confirmed
confidence: 0.8
superseded_by: null
last_confirmed: 2026-05-07
tags: [decision, prd, reconciliation]
entities:
  - {type: decision, name: "C12-节点挂起主任务不回退"}
  - {type: concept, name: "防呆确认"}
relations:
  references: ["checkpoint-form-mapping"]
  depends_on: ["prd-conflict-analysis"]
  derived_from: ["运营管理平台-PRD.docx"]
  supersedes: ["旧版状态体系-主任务挂起规则"]
  contradicts: []
---
```

Wiki link 不带 `.md` 扩展名，脚本解析时自动匹配 `.pm-wiki/` 下的实际文件。

### 1.2 PM专用5种关系类型

| 类型 | 语义 | 方向 | PM场景举例 |
|------|------|------|----------|
| `references` | 引用/参考 | 单向 | 决策引用了组件映射表 |
| `depends_on` | 依赖/前置 | 单向 | 设计依赖冲突分析的结论 |
| `derived_from` | 推导来源 | 单向 | 综合分析从3份原始PRD推导 |
| `supersedes` | 取代 | 单向 | C12决策取代旧版"主任务挂起"规则 |
| `contradicts` | 矛盾 | 双向 | 决策与首页文档冲突 |

不含 `uses/caused/fixed`（太泛或偏bug-tracking），不含 `applies_to`（YAGNI）。

### 1.3 实体类型

| 类型 | 说明 | 举例 |
|------|------|------|
| `decision` | 产品决策(ADR) | C12-节点挂起主任务不回退 |
| `concept` | 业务概念 | 防呆确认、双录入 |
| `person` | 干系人/团队成员 | 张三(管理员) |
| `project` | 项目标识 | MSP/OMP |
| `document` | 源文档 | 运营管理平台-PRD.docx |
| `component` | UI/表单组件 | 任务拆分、多选下拉框 |

### 1.4 目录新增

```
.pm-wiki/
├── (已有目录不变)
├── _generated/                    ← 自动生成索引，勿手动编辑
│   ├── entities.md                ← pm-wiki-graph.py build 产出
│   └── relations.md               ← pm-wiki-graph.py build 产出
```

`_generated/` 下文件由脚本生成，页面顶部标注 `> [自动生成] 此页面由 pm-wiki-graph.py 产出，勿手动编辑`。

### 1.5 工具脚本：pm-wiki-graph.py

| 命令 | 功能 |
|------|------|
| `build` | 遍历 `.pm-wiki/**/*.md`，解析 frontmatter 的 relations + entities → 写入 `_generated/entities.md` + `_generated/relations.md` |
| `traverse <entity> <relation_type>` | 从指定实体出发，沿指定关系类型走图 → 返回关联页面路径列表 |
| `query <topic>` | 先 qmd 混合检索 → 取top结果 → graph traverse 扩展（沿 depends_on/references/derived_from 走1-2步） → RRF融合返回 |

**降级**：脚本不可用时，Claude直接 Grep 扫描 frontmatter 的 `relations:` 字段，手动构建关联。

### 1.6 检索流程变化

原流程：BM25 + vector → rerank → 返回

新流程：

```
用户提问
  → Stream 1: qmd query (BM25 + vector + rerank) → 命中页面集合 S1
  → Stream 2: pm-wiki-graph.py traverse → 从 S1 出发沿关系扩展 → 命中页面集合 S2
  → RRF融合: score = 1/(k + rank_S1) + 1/(k + rank_S2), k=60
  → 去重排序 → 返回（标注来源：BM25/Vector/Graph）
```

RRF公式写在pm-knowledge.md中，Claude在融合时按公式计算。

---

## 2. 置信度 + Supersession

### 2.1 frontmatter新增字段

```yaml
confidence: 0.8          # 0-1，多源+近期=高，单一+久未验证=低
superseded_by: null      # null=当前有效，有值=已被取代（取代页面路径）
last_confirmed: 2026-05-07  # 最近确认日期
```

### 2.2 置信度计算

| 因素 | 影响 |
|------|------|
| 多源确认（每增加1个独立来源） | +0.2 |
| 单一来源 | 基础 0.4 |
| 30天内确认（last_confirmed ≤ 30天） | +0.2 |
| 90天未确认（last_confirmed > 90天） | -0.2 |
| 有 contradicts 关系 | -0.3 |
| 已被取代（superseded_by 有值） | 置0 |

置信度范围 [0, 1]。检索时 confidence < 0.3 的页面默认不返回。

### 2.3 Supersession流程

1. 新页面写入 → skill检查其 `contradicts` 关系
2. 发现矛盾 → skill提示用户："新页面 [[A]] 与 [[B]] 矛盾，是否确认 [[A]] 取代 [[B]]？"
3. 用户确认 → 自动在旧页面写入 `superseded_by: "A"`，旧页面 confidence 置0
4. 旧页面顶部自动加：`> [已取代] 此页面已被 [[A]] 取代 (2026-05-11)`
5. 旧页面不删除，保留归档
6. 检索时 superseded 页面默认排除，除非用户显式要求历史版本

### 2.4 工具脚本：pm-wiki-lint.py

| 命令 | 功能 |
|------|------|
| `confidence` | 扫描所有页面，按时间衰减重算confidence → 更新frontmatter |
| `supersession` | 检查 `contradicts` 关系对 → 建议supersession标记 |
| `stale` | 列出 `last_confirmed` > 90天的页面 → 标记需重新验证 |
| `orphans` | 列出无 relations 且未被任何页面引用的页面 |
| `broken_refs` | 检查 relations 中的引用路径是否存在对应文件 |

**降级**：脚本不可用时，Claude手动 Grep 扫描 frontmatter 检查上述问题。

---

## 3. 分层记忆 + Crystallization

### 3.1 四层架构

```
.pm-wiki/
├── _working/              ← L0: 工作记忆（当前会话临时草稿）
│   └── session-<date>.md      ← 会话内产生的临时笔记/未定结论
├── (已有目录)             ← L1: 插曲记忆（项目事实、决策、约束）
│   ├── context/
│   ├── requirements/
│   ├── constraints/
│   ├── decisions/
│   ├── synthesis/
│   ├── (competitors/)
│   ├── (users/)
│   ├── (market/)
│   ├── (references/)
├── _semantic/             ← L2: 语义记忆（跨模式提炼的通用知识）
│   ├── patterns.md            ← 从多次项目提炼的通用模式
│   ├── heuristics.md          ← 经验法则
│   ├── anti-patterns.md       ← 反模式（踩坑记录）
│   └ templates.md             ← 可复用模板
├── _procedural/           ← L3: 程序记忆（内化的操作规程）
│   ├── checklists.md          ← 标准检查清单
│   ├── workflows.md           ← 标准工作流
│   └ decision-frameworks.md   ← 决策框架
├── _generated/            ← 自动产出索引（Graph层）
```

### 3.2 升级路径

| 触发条件 | 升级动作 | 谁执行 |
|---------|---------|--------|
| 会话结束 | L0 → L1：提取 `_working/` 中的关键结论，写入正式目录 | pm-wiki-crystallize.py session-end |
| 同类pattern出现≥3次（跨项目） | L1 → L2：crystallize提炼为 `_semantic/` 通用模式 | pm-wiki-crystallize.py distill |
| 模式被多次成功应用 | L2 → L3：固化为 `_procedural/` 检查清单/工作流 | pm-wiki-crystallize.py codify |

### 3.3 `_working/` 生命周期

- 会话开始：创建 `session-YYYY-MM-DD.md`，写入时间戳和任务描述
- 会话进行中：追加临时笔记、未定结论、问题清单
- 会话结束：`pm-wiki-crystallize.py session-end` → 提取关键内容写入L1 → 清理 `_working/`
- 旧session文件保留最近1次，更早的自动清理

### 3.4 工具脚本：pm-wiki-crystallize.py

| 命令 | 功能 |
|------|------|
| `session-end` | 扫描 `_working/session-*.md`，提取结构化结论（决策/约束/发现）→ 写入L1对应目录 → 清理 `_working/` |
| `distill` | 扫描L1中同类页面（如3份decisions），提炼共性模式 → 写入 `_semantic/patterns.md` |
| `codify` | 将 `_semantic/` 中高频模式转化为checklist/workflow → 写入 `_procedural/` |

**distill触发条件**：同一 `tags` 组合下出现≥3个页面时自动建议distill。

**降级**：脚本不可用时，Claude手动读取 `_working/` → 提取关键点 → 写入正式目录。

---

## 4. Event-driven Hooks

不写脚本，定义6个钩子写入pm-knowledge.md。Claude Code在执行PM workflow时自动触发：

| Hook | 触发时机 | 自动动作 | 实现方式 |
|------|---------|---------|---------|
| `on_new_source` | 用户提供新文档 | ingest → extract entities → build graph → check contradictions → suggest supersession | pm-knowledge Ingest流程 |
| `on_session_start` | brainstorming/writing-plans skill启动前 | query项目库 → 注入知识摘要 → 标注缺口 | pm-knowledge → brainstorming衔接（已有） |
| `on_session_end` | 会话结束 | compress session notes → `_working/` → crystallize到L1 | pm-wiki-crystallize.py session-end |
| `on_query` | 知识检索完成后 | 检查答案是否值得回写wiki（新发现→写入L1） | pm-knowledge Query流程 |
| `on_memory_write` | 写入wiki页面时 | 检查contradicts → 建议supersession → 更新confidence | pm-wiki-lint.py supersession |
| `on_schedule` | 定期 | confidence衰减 + stale标记 + distill L1→L2 | Claude Code CronCreate |

`on_schedule` 建议频率：每周一次confidence衰减 + 每月一次distill。

---

## 5. pm-knowledge.md 变化概要

在现有 pm-knowledge.md（~470行）上叠加4个新章节：

| 新章节 | 内容 |
|--------|------|
| **4. Graph层** | Relations语法、关系类型、实体类型、目录结构、graph脚本、RRF融合检索流程 |
| **5. 置信度与Supersession** | confidence字段、计算规则、supersession流程、lint脚本 |
| **6. 分层记忆与Crystallization** | 四层架构、升级路径、_working生命周期、crystallize脚本 |
| **7. Event-driven Hooks** | 6个钩子定义、触发时机、实现方式 |

Query流程（现有Section 2）更新：从"BM25+vector→rerank"改为"BM25+vector→rerank + graph→RRF融合"。

Lint流程（现有Section 3）更新：新增confidence/stale/supersession/orphans/broken_refs检查。

### 包管理

工具脚本位于 `skills/pm-skills/scripts/`：

```
skills/pm-skills/
├── knowledge/
│   └── pm-knowledge.md          ← 新增4个章节
├── scripts/
│   ├── pm-wiki-graph.py         ← Graph层工具
│   ├── pm-wiki-lint.py          ← 置信度+Supersession+健康检查
│   └── pm-wiki-crystallize.py   ← 分层记忆+Crystallization
```

package.json 的 skills 数组不变（脚本不是skill，是工具）。但需要在 pm-knowledge.md 中说明脚本调用方式和降级策略。

---

## 验证清单

- [ ] Relations语法：YAML frontmatter，5种PM专用类型，不带.md扩展名
- [ ] 置信度：0-1浮点数，6因素计算规则，<0.3默认不返回
- [ ] Supersession：contradicts→superseded_by，旧页面保留但不返回
- [ ] 分层记忆：L0→L1→L2→L3，3个升级触发条件
- [ ] Event Hooks：6个触发点，on_schedule用CronCreate
- [ ] 降级策略：每个工具脚本都有"脚本不可用时"的纯Grep/手动方案
- [ ] 向后兼容：现有wiki页面无需修改即可工作（新字段可选，缺省=旧模式）