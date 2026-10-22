#!/usr/bin/env python3
"""Import the 32-section Kumārajīva Diamond Sutra from Wikisource."""

from __future__ import annotations

import hashlib
import json
import re
import urllib.parse
import urllib.request
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
BOOK_DIR = ROOT / "books" / "diamond-sutra"
REVISION = 2621253

TITLES = [
    "法會因由分第一", "善現啟請分第二", "大乘正宗分第三", "妙行無住分第四",
    "如理實見分第五", "正信希有分第六", "無得無說分第七", "依法出生分第八",
    "一相無相分第九", "莊嚴淨土分第十", "無為福勝分第十一", "尊重正教分第十二",
    "如法受持分第十三", "離相寂滅分第十四", "持經功德分第十五", "能淨業障分第十六",
    "究竟無我分第十七", "一體同觀分第十八", "法界通化分第十九", "離色離相分第二十",
    "非說所說分第二十一", "無法可得分第二十二", "淨心行善分第二十三", "福智無比分第二十四",
    "化無所化分第二十五", "法身非相分第二十六", "無斷無滅分第二十七", "不受不貪分第二十八",
    "威儀寂靜分第二十九", "一合理相分第三十", "知見不生分第三十一", "應化非真分第三十二",
]


def fetch_wikitext() -> str:
    query = urllib.parse.urlencode({
        "action": "parse",
        "oldid": REVISION,
        "prop": "wikitext",
        "format": "json",
        "formatversion": 2,
    })
    request = urllib.request.Request(
        f"https://zh.wikisource.org/w/api.php?{query}",
        headers={"User-Agent": "SutraMemLibrary/1.0 (content import)"},
    )
    with urllib.request.urlopen(request, timeout=30) as response:
        return json.load(response)["parse"]["wikitext"]


def clean_section(source: str) -> str:
    source = re.sub(r"<!--.*?-->", "", source, flags=re.S)
    source = re.sub(r"\[\[(?:[^\]|]+\|)?([^\]]+)\]\]", r"\1", source)
    source = re.sub(r"<br\s*/?>", "\n", source, flags=re.I)
    source = re.sub(r"''+", "", source)
    paragraphs = []
    for paragraph in re.split(r"\n\s*\n", source.strip()):
        text = "".join(line.strip() for line in paragraph.splitlines() if line.strip())
        if not text:
            continue
        sentences = [part for part in re.split(r"(?<=[。！？；])(?=[「『“]?[^」』”])", text) if part]
        paragraphs.append("\n".join(sentences))
    return "\n\n".join(paragraphs).strip() + "\n"


def main() -> None:
    wikitext = fetch_wikitext()
    pattern = re.compile(r"^====\s*([^『\n]+?)(?:『.*?』)?\s*====\s*$", re.M)
    matches = list(pattern.finditer(wikitext))
    if len(matches) != 32:
        raise RuntimeError(f"Expected 32 sections, found {len(matches)}")

    BOOK_DIR.mkdir(parents=True, exist_ok=True)
    chapters = []
    for offset, (expected_title, match) in enumerate(zip(TITLES, matches), start=1):
        next_start = matches[offset].start() if offset < len(matches) else wikitext.find("\n==外部链接==", match.end())
        if next_start < 0:
            next_start = len(wikitext)
        text = clean_section(wikitext[match.end():next_start])
        file_name = f"{offset:03d}.txt"
        (BOOK_DIR / file_name).write_text(text, encoding="utf-8")
        chapters.append({
            "id": f"chapter-{offset:02d}",
            "title": expected_title,
            "file": file_name,
            "sha256": hashlib.sha256(text.encode("utf-8")).hexdigest(),
        })

    catalog_path = ROOT / "catalog.json"
    catalog = json.loads(catalog_path.read_text(encoding="utf-8"))
    catalog["books"] = [{
        "id": "sutra.diamond.zh-hant",
        "title": "金剛般若波羅蜜經",
        "shortTitle": "金剛經",
        "kind": "sutra",
        "version": 1,
        "status": "available",
        "summary": "姚秦鳩摩羅什譯，依三十二分整理，支持閱讀、背誦與念誦。",
        "source": "維基文庫，修訂 2621253，CC BY-SA 4.0",
        "contentBaseURL": "https://raw.githubusercontent.com/pzdn2009/sutramem-library/main/books/diamond-sutra/",
        "supportsReading": True,
        "supportsMemorization": True,
        "supportsRecitation": True,
        "chapters": chapters,
    }]
    catalog_path.write_text(json.dumps(catalog, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(f"Imported {len(chapters)} chapters into {BOOK_DIR}")


if __name__ == "__main__":
    main()
