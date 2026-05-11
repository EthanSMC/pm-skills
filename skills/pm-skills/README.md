# PM Skills Plugin

产品经理工作流 Skills Plugin — 从知识摄入到需求分析到 PRD，可选原型验证。

适用于 Claude Code / Claude Agent SDK。

## 包含的 Skills

| Skill | 说明 | 触发时机 |
|-------|------|---------|
| `pm-workflow` | 主编排 skill，串联所有阶段 | `/pm-workflow [任务描述]` |
| `pm-knowledge` | 知识引擎（摄入、检索、组织） | 知识摄入/查询时自动调用 |
| `pm-personalize` | 从项目库提炼通用知识到个人库 | 手动调用或 ingest 后自动建议 |
| `prd-reconcile` | 多文档合并与消歧 | 多份PRD/需求文档需合并时 |
| `brainstorming` | 需求探索与设计 | 创建新功能/组件前 |
| `write-prd` | PRD 撰写（增量，不重复 spec） | 设计文档通过后 |
| `prototyping` | 原型验证（技术规格+实施计划+骨架代码） | PRD 通过后用户选择进入 |

## 工作流

```
阶段0: pm-knowledge    知识准备（检索已有知识）
阶段0a: prd-reconcile  多文档合并与消歧（按需）
阶段1: brainstorming   需求探索（基于知识基础）
阶段2: write-prd       PRD 撰写（增量补充 spec） ← 默认终点
阶段3: prototyping     原型验证（可选，用户选择后进入）
  子阶段: 技术规格 → 实施计划 → 骨架构建 → 审查 → 验证 → 分支管理
```

知识在整个流程中由各阶段各自负责回写：

```
文档/URL/文件 → pm-knowledge.ingest → wiki
                                            ↓
用户提问 → pm-knowledge.query → 知识摘要 → brainstorming → 设计决策 → decisions/
                                                          ↓
                                                    write-prd → PRD → requirements/
                                                          ↓
                                                [用户选择: 是否原型验证?]
                                                 ↓ (是)                ↓ (否)
                                         prototyping → 原型产出       工作流结束

多份PRD → prd-reconcile → 冲突分析 → 决策 → 全局PRD → requirements/
```

## 知识库架构

### 双库分离

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

### 审核分流

| 内容类型 | 处理方式 |
|---------|---------|
| 事实性（数据、功能列表、用户原话） | 自动写入 |
| 结构性（索引、链接、日志） | 自动写入 |
| 分析性（对比结论、痛点归纳） | 草稿待审 |
| 推荐性（优先级、风险评估） | 草稿待审 |

## 前置依赖

### MinerU Document Explorer (qmd)

文档解析和检索引擎。安装：

```bash
npm install mineru-document-explorer
# 安装后全局可用 qmd 命令
# 也可单独全局安装：
npm install -g mineru-document-explorer
pip install pymupdf python-docx python-pptx
```

## 安装

### 方式一：本地引用（开发用）

在项目的 `.claude/settings.json` 中：

```json
{
  "skills": {
    "sources": [
      { "type": "local", "path": "./skills/pm-skills" }
    ]
  }
}
```

### 方式二：NPM 安装

```bash
npm install pm-skills
# mineru-document-explorer 会自动作为依赖安装，提供 qmd 命令
```

```json
{
  "skills": {
    "sources": [
      { "type": "npm", "package": "pm-skills" }
    ]
  }
}
```

## 项目结构

```
skills/pm-skills/
├── package.json
├── README.md
├── workflow/
│   └── pm-workflow.md           # 主编排
├── knowledge/
│   ├── pm-knowledge.md          # 知识引擎
│   ├── pm-personalize.md        # 个人知识提炼
│   └── prd-reconcile.md         # 多文档合并与消歧
├── design/
│   ├── brainstorming.md         # 需求探索
│   ├── visual-companion.md      # 可视化伴侣
│   └── scripts/
│       ├── server.cjs
│       ├── helper.js
│       ├── frame-template.html
│       ├── start-server.sh
│       └── stop-server.sh
├── product/
│   └── write-prd.md             # PRD 撰写（增量）
└── implementation/
    ├── prototyping.md                # 原型验证（合并5个实施阶段）
    └── spec-document-reviewer-prompt.md
```

## 使用

```
/pm-workflow [任务描述]
```

或单独调用任意 skill：

```
/brainstorming [需求描述]
/pm-knowledge ingest [文档路径]
/pm-knowledge query [查询内容]
```

## License

MIT
