"""Tests for pm-wiki-graph.py."""
import subprocess
import json
from pathlib import Path


def run_graph(args, wiki_dir):
    """Helper to run pm-wiki-graph.py with args."""
    result = subprocess.run(
        ["python", "pm-wiki-graph.py", "--wiki", str(wiki_dir)] + args,
        capture_output=True, text=True, cwd=Path(__file__).parent,
    )
    return result


def test_build_creates_generated_files(tmp_wiki):
    """build command should create _generated/entities.md and _generated/relations.md."""
    result = run_graph(["build"], tmp_wiki)
    assert result.returncode == 0
    entities_path = tmp_wiki / "_generated" / "entities.md"
    relations_path = tmp_wiki / "_generated" / "relations.md"
    assert entities_path.exists()
    assert relations_path.exists()


def test_build_entities_content(tmp_wiki):
    """entities.md should list all extracted entities."""
    run_graph(["build"], tmp_wiki)
    content = (tmp_wiki / "_generated" / "entities.md").read_text(encoding="utf-8")
    assert "C12-节点挂起主任务不回退" in content
    assert "防呆确认" in content
    assert "任务拆分" in content
    assert "MSP" in content


def test_build_relations_content(tmp_wiki):
    """relations.md should list all typed relations."""
    run_graph(["build"], tmp_wiki)
    content = (tmp_wiki / "_generated" / "relations.md").read_text(encoding="utf-8")
    assert "decisions/conflict-resolutions → references → requirements/checkpoint-form-mapping" in content
    assert "decisions/conflict-resolutions → depends_on → synthesis/prd-conflict-analysis" in content
    assert "decisions/conflict-resolutions → supersedes → decisions/旧版状态体系" in content


def test_build_auto_generated_header(tmp_wiki):
    """Generated files should have auto-generated header."""
    run_graph(["build"], tmp_wiki)
    content = (tmp_wiki / "_generated" / "entities.md").read_text(encoding="utf-8")
    assert "[自动生成]" in content