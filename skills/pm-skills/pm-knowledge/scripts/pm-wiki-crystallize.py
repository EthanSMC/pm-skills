"""PM Wiki Crystallize Tool — session-end, distill, codify.

Usage:
    pm-wiki-crystallize.py --wiki <path> session-end
    pm-wiki-crystallize.py --wiki <path> distill
    pm-wiki-crystallize.py --wiki <path> codify
"""
import argparse
import sys
import re
from pathlib import Path
from datetime import datetime
from collections import defaultdict

try:
    import yaml
except ImportError:
    sys.exit("Error: pyyaml required. Install: pip install pyyaml")


def parse_frontmatter(content):
    """Extract YAML frontmatter from markdown content."""
    if not content.startswith("---"):
        return {}, content
    end = content.find("---", 3)
    if end == -1:
        return {}, content
    try:
        fm = yaml.safe_load(content[3:end].strip()) or {}
    except yaml.YAMLError:
        fm = {}
    body = content[end + 3:]
    return fm, body


def make_frontmatter(fm_dict):
    """Generate YAML frontmatter string."""
    return yaml.dump(fm_dict, default_flow_style=False, allow_unicode=True, sort_keys=False)


def cmd_session_end(wiki_dir):
    """Extract conclusions from _working/ sessions and write to L1 directories."""
    work_dir = wiki_dir / "_working"
    if not work_dir.exists():
        print("No _working/ directory found")
        return

    sessions = sorted(work_dir.glob("session-*.md"))
    if not sessions:
        print("No session files found in _working/")
        return

    extracted = {"decisions": [], "constraints": [], "findings": []}

    # Map singular section names to plural dict keys
    section_to_key = {"Decision": "decisions", "Constraint": "constraints", "Finding": "findings"}

    for session_file in sessions:
        content = session_file.read_text(encoding="utf-8")
        # Extract sections by heading
        for section_type, key in section_to_key.items():
            pattern = rf"## {section_type}\s*\n(.*?)(?=\n## |\Z)"
            matches = re.findall(pattern, content, re.DOTALL)
            for match in matches:
                items = [line.strip().lstrip("- ") for line in match.strip().split("\n") if line.strip().startswith("-")]
                extracted[key].extend(items)

    # Write extracted items to L1
    timestamp = datetime.now().strftime("%Y-%m-%d")

    for category, items in extracted.items():
        if not items:
            continue
        target_dir = wiki_dir / category
        target_dir.mkdir(parents=True, exist_ok=True)
        filename = f"session-{timestamp}-{category}.md"
        fm = {
            "type": category == "decisions" and "decision" or category == "constraints" and "constraint" or "fact",
            "status": "pending-review",
            "confidence": 0.4,
            "superseded_by": None,
            "last_confirmed": timestamp,
            "tags": [category],
            "entities": [],
            "relations": {},
            "source": f"_working/session-{timestamp}.md",
        }
        page_content = f"---\n{make_frontmatter(fm)}---\n# Session {timestamp} — {category.title()}\n\n"
        for item in items:
            page_content += f"- {item}\n"
        (target_dir / filename).write_text(page_content, encoding="utf-8")
        print(f"  Wrote {category}/{filename} ({len(items)} items)")

    # Clean old sessions (keep last 1)
    if len(sessions) > 1:
        for old in sessions[:-1]:
            old.unlink()
            print(f"  Cleaned {old.name}")

    print(f"Session-end complete: {sum(len(v) for v in extracted.values())} items extracted")


def cmd_distill(wiki_dir):
    """Scan L1 pages, find tag clusters >=3, extract common patterns to _semantic/."""
    semantic_dir = wiki_dir / "_semantic"
    semantic_dir.mkdir(exist_ok=True)

    # Collect all L1 pages by tag combination
    pages = {}
    tag_groups = defaultdict(list)
    for md_file in wiki_dir.rglob("*.md"):
        rel = md_file.relative_to(wiki_dir)
        if str(rel).startswith("_") or str(rel).startswith("raw"):
            continue
        content = md_file.read_text(encoding="utf-8")
        fm, _ = parse_frontmatter(content)
        page_name = str(rel.with_suffix("").as_posix())
        pages[page_name] = fm
        tags = fm.get("tags", [])
        if tags:
            tag_key = ",".join(sorted(tags))
            tag_groups[tag_key].append(page_name)

    # Find clusters >= 3
    distilled = 0
    for tag_key, page_names in tag_groups.items():
        if len(page_names) < 3:
            continue
        # Create a patterns page for this tag cluster
        timestamp = datetime.now().strftime("%Y-%m-%d")
        tag_list = tag_key.split(",")
        filename = f"patterns-{tag_list[0]}-{timestamp}.md"

        fm = {
            "type": "analysis",
            "status": "pending-review",
            "confidence": 0.5,
            "superseded_by": None,
            "last_confirmed": timestamp,
            "tags": tag_list + ["pattern", "distilled"],
            "entities": [],
            "relations": {"derived_from": page_names},
        }

        # Summarize pattern: list common themes
        summary_lines = []
        for name in page_names:
            page_fm = pages.get(name, {})
            title = page_fm.get("type", "") + ": " + name
            summary_lines.append(f"- **{name}** ({page_fm.get('status', '?')})")

        pattern_content = f"---\n{make_frontmatter(fm)}---\n"
        pattern_content += f"> [待审] 蒸馏产出，需审核确认\n\n"
        pattern_content += f"# Pattern: {tag_list[0]} ({len(page_names)} pages)\n\n"
        pattern_content += f"## Common Pages\n"
        pattern_content += "\n".join(summary_lines) + "\n"
        pattern_content += f"\n## Auto-distilled {timestamp} from {len(page_names)} source pages.\n"

        # Check if patterns.md already exists — append section
        patterns_file = semantic_dir / "patterns.md"
        if patterns_file.exists():
            existing = patterns_file.read_text(encoding="utf-8")
            # Append new section
            patterns_file.write_text(existing + "\n\n" + pattern_content, encoding="utf-8")
        else:
            patterns_file.write_text(pattern_content, encoding="utf-8")

        distilled += 1
        print(f"  Distilled '{tag_key}' → _semantic/patterns.md ({len(page_names)} pages)")

    # Ensure other semantic pages exist (even if empty templates)
    for template in ["heuristics.md", "anti-patterns.md", "templates.md"]:
        tpl_file = semantic_dir / template
        if not tpl_file.exists():
            tpl_file.write_text(f"# {template.replace('.md', '').title()}\n\n(Auto-created template — fill in as patterns emerge)\n", encoding="utf-8")

    print(f"Distill complete: {distilled} patterns distilled")


def cmd_codify(wiki_dir):
    """Convert semantic patterns to procedural checklists/workflows."""
    procedural_dir = wiki_dir / "_procedural"
    procedural_dir.mkdir(exist_ok=True)

    # Read patterns and create checklist stubs
    semantic_dir = wiki_dir / "_semantic"
    if not semantic_dir.exists():
        print("No _semantic/ directory found — run distill first")
        return

    patterns_file = semantic_dir / "patterns.md"
    if not patterns_file.exists():
        print("No patterns.md found — run distill first")
        return

    # Create procedural templates
    timestamp = datetime.now().strftime("%Y-%m-%d")
    for template in ["checklists.md", "workflows.md", "decision-frameworks.md"]:
        tpl_file = procedural_dir / template
        if not tpl_file.exists():
            tpl_file.write_text(f"# {template.replace('.md', '').title()}\n\n(Auto-created {timestamp} — codify from semantic patterns)\n", encoding="utf-8")

    print(f"Codify: procedural templates created in _procedural/")


def main():
    parser = argparse.ArgumentParser(description="PM Wiki Crystallize Tool")
    parser.add_argument("--wiki", required=True, help="Path to .pm-wiki directory")
    subparsers = parser.add_subparsers(dest="command")

    subparsers.add_parser("session-end", help="Extract from _working/ → L1")
    subparsers.add_parser("distill", help="Distill L1 → _semantic/")
    subparsers.add_parser("codify", help="Codify _semantic/ → _procedural/")

    args = parser.parse_args()
    wiki_dir = Path(args.wiki)

    if not wiki_dir.exists():
        sys.exit(f"Wiki directory not found: {wiki_dir}")

    cmds = {
        "session-end": cmd_session_end,
        "distill": cmd_distill,
        "codify": cmd_codify,
    }
    if args.command in cmds:
        cmds[args.command](wiki_dir)
    else:
        parser.print_help()


if __name__ == "__main__":
    main()