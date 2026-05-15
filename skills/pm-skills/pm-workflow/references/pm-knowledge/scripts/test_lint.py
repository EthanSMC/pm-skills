"""Tests for pm-wiki-lint.py."""
import subprocess
from pathlib import Path
from datetime import datetime, timedelta


def run_lint(args, wiki_dir):
    """Helper to run pm-wiki-lint.py."""
    result = subprocess.run(
        ["python", "pm-wiki-lint.py", "--wiki", str(wiki_dir)] + args,
        capture_output=True, text=True, cwd=Path(__file__).parent,
    )
    return result


def test_confidence_recalculates_scores(tmp_wiki):
    """confidence command should update confidence scores based on time decay."""
    result = run_lint(["confidence"], tmp_wiki)
    assert result.returncode == 0
    # Read conflict-resolutions page — should have updated confidence
    content = (tmp_wiki / "decisions" / "conflict-resolutions.md").read_text(encoding="utf-8")
    assert "confidence:" in content


def test_stale_lists_old_pages(tmp_wiki):
    """stale command should list pages with last_confirmed > 90 days."""
    # Create a stale page
    stale_dir = tmp_wiki / "context"
    stale_dir.mkdir(exist_ok=True)
    stale_date = (datetime.now() - timedelta(days=120)).strftime("%Y-%m-%d")
    stale_page = stale_dir / "old-info.md"
    stale_page.write_text(f"""---
type: fact
status: confirmed
confidence: 0.5
superseded_by: null
last_confirmed: {stale_date}
tags: [old]
entities: []
relations: {{}}
---
# Old Info

Stale content.
""", encoding="utf-8")

    result = run_lint(["stale"], tmp_wiki)
    assert result.returncode == 0
    assert "old-info" in result.stdout


def test_supersession_detects_contradictions(tmp_wiki):
    """supersession command should list contradicts pairs for supersession review."""
    result = run_lint(["supersession"], tmp_wiki)
    assert result.returncode == 0
    # conflict-resolutions and 旧版状态体系 have contradicts relation
    assert "conflict-resolutions" in result.stdout or "旧版状态体系" in result.stdout


def test_orphans_detects_unreferenced_pages(tmp_wiki):
    """orphans command should list pages with no relations and no inbound references."""
    # Create an orphan page
    orphan_dir = tmp_wiki / "context"
    orphan_page = orphan_dir / "orphan.md"
    orphan_page.write_text("""---
type: fact
status: confirmed
confidence: 0.5
superseded_by: null
last_confirmed: 2026-05-01
tags: [orphan]
entities: []
relations: {}
---
# Orphan

No one references this.
""", encoding="utf-8")

    result = run_lint(["orphans"], tmp_wiki)
    assert result.returncode == 0
    assert "orphan" in result.stdout