import re
import sqlite3
from pathlib import Path


def sanitize_filename(name: str) -> str:
    cleaned = re.sub(r'[<>:"/\\|?*]+', "_", name).strip()
    return cleaned or "unknown_source"


def main() -> None:
    db_path = Path("data/knowledge.db")
    out_dir = Path("knowledge_sources")
    out_dir.mkdir(parents=True, exist_ok=True)

    conn = sqlite3.connect(db_path)
    conn.row_factory = sqlite3.Row
    rows = conn.execute(
        """
        SELECT source, title, content
        FROM wiki_articles
        WHERE source LIKE 'upload:%'
        ORDER BY source, id
        """
    ).fetchall()
    conn.close()

    grouped: dict[str, list[sqlite3.Row]] = {}
    for row in rows:
        source = (row["source"] or "").replace("upload:", "", 1)
        grouped.setdefault(source, []).append(row)

    for source_name, items in grouped.items():
        file_name = sanitize_filename(source_name) + ".md"
        target = out_dir / file_name
        lines = [f"# Source: {source_name}", ""]
        for idx, item in enumerate(items, start=1):
            lines.append(f"## Knowledge Point {idx}: {item['title']}")
            lines.append("")
            lines.append((item["content"] or "").strip())
            lines.append("")
        target.write_text("\n".join(lines), encoding="utf-8")

    print(f"exported_sources={len(grouped)}")


if __name__ == "__main__":
    main()
