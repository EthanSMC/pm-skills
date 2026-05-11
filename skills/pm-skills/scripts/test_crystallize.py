"""Tests for pm-wiki-crystallize.py."""
import subprocess
from pathlib import Path


def run_crystallize(args, wiki_dir):
    """Helper to run pm-wiki-crystallize.py."""
    result = subprocess.run(
        ["python", "pm-wiki-crystallize.py", "--wiki", str(wiki_dir)] + args,
        capture_output=True, text=True, cwd=Path(__file__).parent,
    )
    return result


def test_session_end_creates_l1_pages(tmp_wiki):
    """session-end should extract conclusions from _working/ and write to L1."""
    # Create a working session file
    work_dir = tmp_wiki / "_working"
    work_dir.mkdir(exist_ok=True)
    session_file = work_dir / "session-2026-05-11.md"
    session_file.write_text("""---
date: 2026-05-11
task: wiki-retrieval-upgrade
---
# Session Notes

## Decision
- 采用YAML frontmatter存储relations（不放在正文）

## Constraint
- Python脚本必须支持降级模式（脚本不可用时纯Grep）
""", encoding="utf-8")

    result = run_crystallize(["session-end"], tmp_wiki)
    assert result.returncode == 0
    # Check that L1 pages were created
    decisions_dir = tmp_wiki / "decisions"
    constraints_dir = tmp_wiki / "constraints"
    # At least one new file should exist in L1
    l1_files = list(decisions_dir.glob("*.md")) + list(constraints_dir.glob("*.md"))
    assert len(l1_files) >= 2  # 1 decision + 1 constraint extracted


def test_session_end_cleans_working(tmp_wiki):
    """session-end should clean up old _working/ files (keep last 1)."""
    work_dir = tmp_wiki / "_working"
    work_dir.mkdir(exist_ok=True)
    # Create two session files
    (work_dir / "session-2026-05-10.md").write_text("old session", encoding="utf-8")
    (work_dir / "session-2026-05-11.md").write_text("""---
date: 2026-05-11
task: test
---
## Decision
- test decision
""", encoding="utf-8")

    run_crystallize(["session-end"], tmp_wiki)
    # Old session should be cleaned, current one kept
    remaining = list(work_dir.glob("session-*.md"))
    assert len(remaining) <= 1


def test_distill_creates_semantic_pages(tmp_wiki):
    """distill should create _semantic/patterns.md when >=3 pages share same tags."""
    # Add 3 decision pages with identical tags to form a cluster
    decisions_dir = tmp_wiki / "decisions"
    decisions_dir.mkdir(exist_ok=True)
    for i in [2, 3, 4]:
        (decisions_dir / f"decision{i}.md").write_text(f"""---
type: decision
status: confirmed
confidence: 0.7
superseded_by: null
last_confirmed: 2026-05-01
tags: [decision, reconciliation]
entities: []
relations: {{}}
---
# Decision {i}

Decision in the reconciliation pattern.
""", encoding="utf-8")

    result = run_crystallize(["distill"], tmp_wiki)
    assert result.returncode == 0
    semantic_dir = tmp_wiki / "_semantic"
    assert semantic_dir.exists()
    patterns_file = semantic_dir / "patterns.md"
    assert patterns_file.exists()