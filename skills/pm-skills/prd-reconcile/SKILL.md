---
name: prd-reconcile
description: "PRD合并与消歧 — 将多份分批构建的PRD/需求文档合并为一份全局PRD。系统化识别跨文档冲突，引导逐一决策，产出无歧义的统一文档。Make sure to use this skill whenever the user has multiple PRD or requirement documents that need merging, mentions cross-document conflicts or inconsistencies, says they need a 'global PRD' or 'unified PRD', or has incrementally-built documents that need reconciliation — even if they just say 'these documents conflict' or 'merge these docs' without explicitly asking for a 'PRD reconcile'."
---

# PRD Reconcile — 多文档合并与消歧

将分批构建的多份PRD/需求文档合并为一份权威的全局PRD。系统化识别冲突、引导逐一决策、确保合并后无歧义。

## 适用场景

- 多份PRD（主文档、页面PRD、模块PRD、字段定义CSV、校验规则Excel等）分批构建，需要合并
- 子文档之间存在矛盾、术语冲突、流程不一致
- 需要产出所有团队可对齐的权威全局PRD

## 前置

- 用户提供所有源文档路径（支持 docx/csv/xlsx/pdf/md）
- 项目知识库 `<project>/.pm-wiki/`（不存在则自动创建）
- 若已有 pm-knowledge skill，可复用其知识库做回源查询

---

## 五阶段流程

### Phase 1: 摄入

逐份读取源文档，提取结构化内容，写入项目知识库。

1. 按格式提取文档内容（docx→python-docx, csv→直接解析, xlsx→openpyxl, pdf→PyPDF2/pdfplumber, md→直接读取）
2. 每份文档按PM维度写入 `.pm-wiki/requirements/` 或 `.pm-wiki/context/`
3. 提取重点：文档标题/版本、章节段落内容、关键术语定义、状态枚举、角色定义、流程步骤、数据字段
4. 记录摄入日志到 `.pm-wiki/log.md`，更新索引 `.pm-wiki/MEMORY.md`

产出：知识库中每份文档的结构化内容，可随时回源。

### Phase 2: 冲突分析

全量交叉比对，识别冲突点并分级编号。

**冲突类型：**
| 类型 | 说明 | 示例 |
|------|------|------|
| 矛盾 | 同一概念不同定义 | 状态枚举不同、角色名称不同 |
| 不一致 | 同一流程步骤/字段不同 | 流程顺序差异、字段列表差异 |
| 术语冲突 | 同一实体不同称呼 | "A岗" vs "预检员" vs "role1" |
| 缺失 | 某文档提到其他未覆盖 | 某字段只在一份文档出现 |
| 隐含歧义 | 看似一致实则不同理解 | "挂起"是否回退主任务状态 |

**分级标准：**
| 级别 | 含义 | 合并影响 |
|------|------|---------|
| P0 | 核心架构冲突 | 不决策就无法合并 |
| P1 | 重要业务逻辑差异 | 影响开发实现 |
| P2 | 术语/命名/展示差异 | 影响沟通但非功能 |
| P3 | 细微差异/风格偏好 | 合并时统一即可 |

**编号规则**：C1, C2, C3... 连续编号。多轮排查时编号续接（第二轮从上一轮最大编号+1开始）。

**排查流程：**
1. 第一轮：逐段落交叉比对所有文档，识别明显矛盾 → 编号分级 → 写入报告
2. 第二轮：回源原始文档逐段落重新提取，检查隐含冲突 → 续接编号
3. 如有需要可继续第三轮，直到用户确认无遗漏

**报告格式** — 写入 `.pm-wiki/synthesis/prd-conflict-analysis.md`：

```markdown
---
type: analysis
status: pending-review
source: 全量文档交叉比对
ingested: YYYY-MM-DD
project: <项目名>
tags: [conflict, prd, reconciliation]
---
# PRD 冲突分析报告

## P0 级冲突（必须决策）
| 编号 | 冲突描述 | 涉及文档 | 建议方向 |
|------|---------|---------|---------|

## P1 级冲突（重要差异）
| 编号 | 冲突描述 | 涉及文档 | 建议方向 |
|------|---------|---------|---------|

## P2-P3 级冲突（合并时统一）
| 编号 | 冲突描述 | 涉及文档 | 处理方式 |
|------|---------|---------|---------|
```

产出：冲突分析报告，编号+分级+涉及文档+建议方向。

### Phase 3: 逐一决策

与用户逐一讨论每个冲突，记录决策和理由。

**呈现格式** — 每个冲突向用户展示：
- 编号和描述
- 涉及文档的原文对比（不是摘要，是原文引用）
- ≥2个决策选项 + 利弊分析
- 推荐方向（如有）+推荐理由

**讨论顺序**：P0 → P1 → P2-P3。P0决策完成后检查是否影响其他冲突的建议方向。

**多轮衔接**：Phase 2和Phase 3交替——发现冲突→编号→讨论→决策→再排查→新冲突→继续，直到用户确认"没有更多冲突了"。

**复杂系统建模**：如果冲突涉及状态转换、权限矩阵等系统性问题，单独产出完整矩阵写入决策记录。

**决策记录格式** — 写入 `.pm-wiki/decisions/conflict-resolutions.md`：

```markdown
---
type: fact
status: confirmed
source: 逐一讨论决策
ingested: YYYY-MM-DD
project: <项目名>
tags: [decision, prd, reconciliation]
---
# PRD 冲突决策记录

## P0 级决策（已确认）
| 编号 | 冲突 | 决策 |
|------|------|------|

## P1 级决策（已确认）
| 编号 | 冲突 | 决策 |
|------|------|------|

（每个决策附 **Why:** 理由 和 **How to apply:** 适用场景）
```

产出：决策记录，全部confirmed。

### Phase 4: 合并编写

基于所有源文档和决策记录编写全局PRD。

1. **设计章节结构**：根据源文档覆盖范围和决策结果，设计合并后的大纲。不要照搬任何单份文档的结构，而是基于所有文档的综合覆盖面重新设计
2. **逐章编写**：
   - 冲突内容取决策结果，不取任何单文档的说法
   - 标注决策编号引用方便回溯
   - 统一术语（按术语决策统一用词）
   - 状态枚举、字段命名统一
3. **系统性内容完整性**：确保状态转换矩阵、角色权限、数据模型等系统性内容完整呈现，不留半成品
4. **写入** `<项目名> - 全局PRD.md` 到项目根目录

产出：全局PRD文档。

### Phase 5: 验证

对照决策记录逐条验证全局PRD。

**验证清单：**
1. 决策覆盖 — 逐C编号检查是否体现
2. 术语一致性 — 搜索废弃旧术语应全部替换
3. 系统性内容完整性 — 状态矩阵/权限矩阵/数据模型无遗漏
4. 冲突残留 — 全文自查无未解决矛盾
5. 源文档覆盖 — 每份源文档核心内容都有对应章节

遗漏→回Phase 4补充→重新验证。全部通过→最终版确认。

---

## 与 pm-knowledge 的衔接

产出写入共享知识库：
- 冲突分析 → `.pm-wiki/synthesis/`
- 决策记录 → `.pm-wiki/decisions/`
- 映射表 → `.pm-wiki/requirements/`
- 产品概览 → `.pm-wiki/context/`
- 操作日志 → `.pm-wiki/log.md`
- 索引 → `.pm-wiki/MEMORY.md`

pm-knowledge 的 query 可在 Phase 2-3 回源查询。

---

## 关键原则

- **不遗漏**：全量逐段落交叉比对，不接受"差不多"判断
- **不猜测**：每个冲突必须与用户讨论确认，不自作主张
- **不遗忘**：决策编号+理由+PRD引用，全程可回溯
- **不歧义**：合并后术语统一、枚举统一、流程唯一
- **多轮迭代**：冲突排查不是一次性的——分析→决策→再排查，直到用户确认无遗漏