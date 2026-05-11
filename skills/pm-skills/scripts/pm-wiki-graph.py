"""PM Wiki Graph Tool — build, traverse, and query the knowledge graph.

Usage:
    pm-wiki-graph.py --wiki <path> build
    pm-wiki-graph.py --wiki <path> traverse <entity> [--relation <type>]
    pm-wiki-graph.py --wiki <path> query <topic>
"""
import argparse
import sys
import os
from pathlib import Path
from datetime import datetime

try:
    import yaml
except ImportError:
    sys.exit("Error: pyyaml required. Install: pip install pyyaml")

RELATION_TYPES = ["references", "depends_on", "derived_from", "supersedes", "contradicts"]
ENTITY_TYPES = ["decision", "concept", "person", "project", "document", "component"]
AUTO_GEN_HEADER = "> [自动生成] 此页面由 pm-wiki-graph.py 产出，勿手动编辑\n\n"


def parse_frontmatter(content):
    """Extract YAML frontmatter from markdown content."""
    if not content.startswith("---"):
        return {}
    end = content.find("---", 3)
    if end == -1:
        return {}
    fm_text = content[3:end].strip()
    try:
        return yaml.safe_load(fm_text) or {}
    except yaml.YAMLError:
        return {}


def scan_pages(wiki_dir):
    """Walk wiki_dir, parse frontmatter from all .md files (excluding _generated/ and _working/)."""
    pages = {}
    for md_file in wiki_dir.rglob("*.md"):
        rel = md_file.relative_to(wiki_dir)
        # Skip generated and working dirs
        if str(rel).startswith("_generated") or str(rel).startswith("_working"):
            continue
        content = md_file.read_text(encoding="utf-8")
        fm = parse_frontmatter(content)
        # Page name = relative path without .md extension, always use / separator
        page_name = str(rel.with_suffix("").as_posix())
        fm["_path"] = str(md_file)
        fm["_rel_path"] = page_name
        pages[page_name] = fm
    return pages


def resolve_page_name(ref, pages):
    """Resolve a wiki link (without .md) to an actual page name.

    Tries exact match first, then searches for partial matches.
    """
    if ref in pages:
        return ref
    # Fallback: search by stem
    for name in pages:
        if Path(name).stem == ref or Path(name).name == ref:
            return name
    return None


def build_graph(wiki_dir):
    """Build _generated/entities.md and _generated/relations.md."""
    pages = scan_pages(wiki_dir)
    gen_dir = wiki_dir / "_generated"
    gen_dir.mkdir(exist_ok=True)

    # Collect entities
    entity_lines = []
    for page_name, fm in sorted(pages.items()):
        entities = fm.get("entities", [])
        for ent in entities:
            etype = ent.get("type", "unknown")
            ename = ent.get("name", "")
            entity_lines.append(f"- [{etype}] {ename} ← {page_name}")

    entities_content = AUTO_GEN_HEADER + "# Entities Index\n\n"
    entities_content += f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M')}\n\n"
    entities_content += "\n".join(entity_lines)

    (gen_dir / "entities.md").write_text(entities_content, encoding="utf-8")

    # Collect relations
    relation_lines = []
    for page_name, fm in sorted(pages.items()):
        relations = fm.get("relations", {})
        for rtype in RELATION_TYPES:
            refs = relations.get(rtype, [])
            for ref in refs:
                resolved = resolve_page_name(ref, pages)
                target = resolved or ref
                relation_lines.append(f"- {page_name} → {rtype} → {target}")

    relations_content = AUTO_GEN_HEADER + "# Relations Index\n\n"
    relations_content += f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M')}\n\n"
    relations_content += "\n".join(relation_lines)

    (gen_dir / "relations.md").write_text(relations_content, encoding="utf-8")

    print(f"Built graph: {len(entity_lines)} entities, {len(relation_lines)} relations")


def traverse_graph(wiki_dir, entity_name, relation_type=None):
    """Traverse graph from a starting point, optionally filtered by relation type."""
    pages = scan_pages(wiki_dir)

    # Find pages mentioning the entity
    start_pages = []
    for page_name, fm in pages.items():
        entities = fm.get("entities", [])
        for ent in entities:
            if ent.get("name", "") == entity_name:
                start_pages.append(page_name)

    if not start_pages:
        # Also try matching page name
        resolved = resolve_page_name(entity_name, pages)
        if resolved:
            start_pages = [resolved]

    if not start_pages:
        print(f"Entity '{entity_name}' not found")
        return

    # Walk relations from start pages
    visited = set()
    results = []
    for start in start_pages:
        fm = pages.get(start, {})
        relations = fm.get("relations", {})
        for rtype in RELATION_TYPES:
            if relation_type and rtype != relation_type:
                continue
            refs = relations.get(rtype, [])
            for ref in refs:
                resolved = resolve_page_name(ref, pages)
                if resolved and resolved not in visited:
                    visited.add(resolved)
                    results.append(f"{start} → {rtype} → {resolved}")

    # Also find pages that reference start_pages (reverse traversal)
    for page_name, fm in pages.items():
        if page_name in visited or page_name in start_pages:
            continue
        relations = fm.get("relations", {})
        for rtype in RELATION_TYPES:
            if relation_type and rtype != relation_type:
                continue
            refs = relations.get(rtype, [])
            for ref in refs:
                if ref in start_pages:
                    if page_name not in visited:
                        visited.add(page_name)
                        results.append(f"{page_name} → {rtype} → {ref} (reverse)")

    for line in results:
        print(line)


def main():
    parser = argparse.ArgumentParser(description="PM Wiki Graph Tool")
    parser.add_argument("--wiki", required=True, help="Path to .pm-wiki directory")
    subparsers = parser.add_subparsers(dest="command")

    subparsers.add_parser("build", help="Build _generated/ indexes")
    traverse_parser = subparsers.add_parser("traverse", help="Traverse from entity")
    traverse_parser.add_argument("entity", help="Starting entity name")
    traverse_parser.add_argument("--relation", choices=RELATION_TYPES, help="Filter by relation type")

    query_parser = subparsers.add_parser("query", help="Graph-enhanced query")
    query_parser.add_argument("topic", help="Topic to search")

    args = parser.parse_args()
    wiki_dir = Path(args.wiki)

    if not wiki_dir.exists():
        sys.exit(f"Wiki directory not found: {wiki_dir}")

    if args.command == "build":
        build_graph(wiki_dir)
    elif args.command == "traverse":
        traverse_graph(wiki_dir, args.entity, args.relation)
    elif args.command == "query":
        # query = build + traverse + RRF (future: integrate with qmd)
        build_graph(wiki_dir)
        traverse_graph(wiki_dir, args.topic)
    else:
        parser.print_help()


if __name__ == "__main__":
    main()