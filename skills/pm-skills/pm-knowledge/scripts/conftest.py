"""Shared test fixtures for pm-wiki scripts."""
import pytest
import os
from pathlib import Path


SAMPLE_PAGES = {
    "decisions/conflict-resolutions.md": """---
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
  supersedes: ["旧版状态体系"]
  contradicts: []
---
# PRD 冲突决策记录

C12: 节点挂起，主任务不回退状态。
""",
    "requirements/checkpoint-form-mapping.md": """---
type: analysis
status: pending-review
confidence: 0.4
superseded_by: null
last_confirmed: 2026-04-20
tags: [mapping, form-component, checkpoint-type]
entities:
  - {type: component, name: "任务拆分"}
  - {type: component, name: "多选下拉框"}
relations:
  references: []
  depends_on: ["conflict-resolutions"]
  derived_from: ["KYC校验规则.xlsx"]
  supersedes: []
  contradicts: []
---
# 检查点类型 → 动态表单组件映射表

Type1→Type5 mapping details.
""",
    "synthesis/prd-conflict-analysis.md": """---
type: analysis
status: pending-review
confidence: 0.6
superseded_by: null
last_confirmed: 2026-04-10
tags: [conflict, prd, reconciliation]
entities:
  - {type: document, name: "运营管理平台-PRD.docx"}
relations:
  references: ["conflict-resolutions"]
  depends_on: []
  derived_from: ["运营管理平台-PRD.docx"]
  supersedes: []
  contradicts: []
---
# PRD 文档冲突分析报告

25 conflicts identified across 5 documents.
""",
    "context/product-overview.md": """---
type: fact
status: confirmed
confidence: 0.9
superseded_by: null
last_confirmed: 2026-05-01
tags: [prd, overview, architecture]
entities:
  - {type: project, name: "MSP"}
  - {type: concept, name: "主任务"}
relations:
  references: ["conflict-resolutions"]
  depends_on: []
  derived_from: []
  supersedes: []
  contradicts: []
---
# MSP 运营管理平台 — 产品全景

Core architecture: 主任务 → 版本化分拆 → 执行节点 → 检查点.
""",
    "decisions/旧版状态体系.md": """---
type: decision
status: confirmed
confidence: 0.0
superseded_by: "conflict-resolutions"
last_confirmed: 2026-03-01
tags: [decision, status, deprecated]
entities:
  - {type: concept, name: "主任务挂起"}
relations:
  references: []
  depends_on: []
  derived_from: []
  supersedes: []
  contradicts: ["conflict-resolutions"]
---
> [已取代] 此页面已被 [[conflict-resolutions]] 取代 (2026-05-07)

# 旧版状态体系

主任务有suspended状态（已被C12决策取代）。
""",
}


@pytest.fixture
def tmp_wiki(tmp_path):
    """Create a mock .pm-wiki/ directory with sample pages."""
    wiki_dir = tmp_path / ".pm-wiki"
    for rel_path, content in SAMPLE_PAGES.items():
        page_path = wiki_dir / rel_path
        page_path.parent.mkdir(parents=True, exist_ok=True)
        page_path.write_text(content, encoding="utf-8")
    # Create _generated dir (empty initially)
    (wiki_dir / "_generated").mkdir()
    return wiki_dir