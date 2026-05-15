"""PM Wiki Lint Tool — confidence scoring, supersession, stale detection, orphans.

Usage:
    pm-wiki-lint.py --wiki <path> confidence
    pm-wiki-lint.py --wiki <path> supersession
    pm-wiki-lint.py --wiki <path> stale
    pm-wiki-lint.py --wiki <path> orphans
    pm-wiki-lint.py --wiki <path> broken_refs
"""
import argparse
import sys
from pathlib import Path
from datetime import datetime, date

try:
    import yaml
except ImportError:
    sys.exit("Error: pyyaml required. Install: pip install pyyaml")

RELATION_TYPES = ["references", "depends_on", "derived_from", "supersedes", "contradicts"]


def parse_frontmatter(content):
    """Extract YAML frontmatter from markdown content."""
    if not content.startswith("---"):
        return {}
    end = content.find("---", 3)
    if end == -1:
        return {}
    try:
        return yaml.safe_load(content[3:end].strip()) or {}
    except yaml.YAMLError:
        return {}


def write_frontmatter(content, fm):
    """Replace YAML frontmatter in markdown content with updated fm."""
    if not content.startswith("---"):
        return content
    end = content.find("---", 3)
    if end == -1:
        return content
    body = content[end + 3:]
    new_fm = yaml.dump(fm, default_flow_style=False, allow_unicode=True, sort_keys=False)
    return f"---\n{new_fm}---{body}"


def scan_pages(wiki_dir):
    """Walk wiki_dir, parse frontmatter from all .md files."""
    pages = {}
    for md_file in wiki_dir.rglob("*.md"):
        rel = md_file.relative_to(wiki_dir)
        if str(rel).startswith("_generated") or str(rel).startswith("_working"):
            continue
        content = md_file.read_text(encoding="utf-8")
        fm = parse_frontmatter(content)
        page_name = str(rel.with_suffix("").as_posix())
        pages[page_name] = {"fm": fm, "path": md_file, "content": content}
    return pages


def calculate_confidence(fm, page_name, pages):
    """Calculate confidence score based on spec rules."""
    base = 0.4  # single source

    # Multi-source: count derived_from + references
    relations = fm.get("relations", {})
    sources = len(relations.get("derived_from", [])) + len(relations.get("references", []))
    if sources > 1:
        base += 0.2 * (sources - 1)

    # Recent confirmation
    last_confirmed = fm.get("last_confirmed", "")
    if last_confirmed:
        try:
            lc_date = date.fromisoformat(str(last_confirmed))
            days_since = (date.today() - lc_date).days
            if days_since <= 30:
                base += 0.2
            elif days_since > 90:
                base -= 0.2
        except ValueError:
            pass

    # Contradictions
    contradicts = relations.get("contradicts", [])
    if contradicts:
        base -= 0.3

    # Superseded
    if fm.get("superseded_by"):
        base = 0.0

    return max(0.0, min(1.0, base))


def cmd_confidence(wiki_dir):
    """Recalculate and update confidence scores for all pages."""
    pages = scan_pages(wiki_dir)
    updated = 0
    for page_name, data in pages.items():
        fm = data["fm"]
        new_conf = calculate_confidence(fm, page_name, pages)
        old_conf = fm.get("confidence", None)
        if old_conf != new_conf:
            fm["confidence"] = round(new_conf, 2)
            new_content = write_frontmatter(data["content"], fm)
            data["path"].write_text(new_content, encoding="utf-8")
            updated += 1
            print(f"  {page_name}: {old_conf} → {new_conf}")
    print(f"Updated {updated} confidence scores")


def cmd_supersession(wiki_dir):
    """Check contradicts pairs and suggest supersession."""
    pages = scan_pages(wiki_dir)
    pairs = []
    for page_name, data in pages.items():
        fm = data["fm"]
        contradicts = fm.get("relations", {}).get("contradicts", [])
        for target in contradicts:
            # Resolve target to page name
            resolved = target
            for name in pages:
                if Path(name).stem == target or Path(name).name == target or name == target:
                    resolved = name
                    break
            target_fm = pages.get(resolved, {}).get("fm", {})
            if not target_fm.get("superseded_by"):
                pairs.append((page_name, resolved))
    if pairs:
        print("Contradicts pairs needing supersession review:")
        for src, tgt in pairs:
            print(f"  {src} contradicts {tgt}")
    else:
        print("No contradicts pairs found")


def cmd_stale(wiki_dir):
    """List pages with last_confirmed > 90 days."""
    pages = scan_pages(wiki_dir)
    stale = []
    for page_name, data in pages.items():
        fm = data["fm"]
        lc = fm.get("last_confirmed", "")
        if not lc:
            continue
        try:
            lc_date = date.fromisoformat(str(lc))
            days = (date.today() - lc_date).days
            if days > 90 and not fm.get("superseded_by"):
                stale.append((page_name, days))
        except ValueError:
            pass
    if stale:
        print(f"Stale pages ({len(stale)}):")
        for name, days in sorted(stale, key=lambda x: -x[1]):
            print(f"  {name} — {days} days since confirmation")
    else:
        print("No stale pages found")


def cmd_orphans(wiki_dir):
    """List pages with no relations and no inbound references."""
    pages = scan_pages(wiki_dir)
    # Build inbound reference map
    inbound = set()
    for page_name, data in pages.items():
        relations = data["fm"].get("relations", {})
        for rtype in RELATION_TYPES:
            for ref in relations.get(rtype, []):
                inbound.add(ref)

    orphans = []
    for page_name, data in pages.items():
        relations = data["fm"].get("relations", {})
        has_outbound = any(relations.get(rtype, []) for rtype in RELATION_TYPES)
        # Check inbound by both full path and short name
        has_inbound = page_name in inbound or Path(page_name).stem in inbound
        if not has_outbound and not has_inbound and not data["fm"].get("superseded_by"):
            orphans.append(page_name)
    if orphans:
        print(f"Orphan pages ({len(orphans)}):")
        for name in sorted(orphans):
            print(f"  {name}")
    else:
        print("No orphan pages found")


def cmd_broken_refs(wiki_dir):
    """Check if relations reference pages that don't exist."""
    pages = scan_pages(wiki_dir)
    existing_names = set(pages.keys())
    # Also add short names (without directory prefix) for matching
    short_names = {Path(n).stem for n in existing_names}
    broken = []
    for page_name, data in pages.items():
        relations = data["fm"].get("relations", {})
        for rtype in RELATION_TYPES:
            for ref in relations.get(rtype, []):
                found = ref in existing_names or ref in short_names
                if not found:
                    broken.append((page_name, rtype, ref))
    if broken:
        print(f"Broken references ({len(broken)}):")
        for src, rtype, ref in broken:
            print(f"  {src} → {rtype} → {ref} (not found)")
    else:
        print("No broken references found")


def main():
    parser = argparse.ArgumentParser(description="PM Wiki Lint Tool")
    parser.add_argument("--wiki", required=True, help="Path to .pm-wiki directory")
    subparsers = parser.add_subparsers(dest="command")

    subparsers.add_parser("confidence", help="Recalculate confidence scores")
    subparsers.add_parser("supersession", help="Check contradicts pairs")
    subparsers.add_parser("stale", help="List stale pages (>90 days)")
    subparsers.add_parser("orphans", help="List orphan pages")
    subparsers.add_parser("broken_refs", help="Check broken references")

    args = parser.parse_args()
    wiki_dir = Path(args.wiki)

    if not wiki_dir.exists():
        sys.exit(f"Wiki directory not found: {wiki_dir}")

    cmds = {
        "confidence": cmd_confidence,
        "supersession": cmd_supersession,
        "stale": cmd_stale,
        "orphans": cmd_orphans,
        "broken_refs": cmd_broken_refs,
    }
    if args.command in cmds:
        cmds[args.command](wiki_dir)
    else:
        parser.print_help()


if __name__ == "__main__":
    main()