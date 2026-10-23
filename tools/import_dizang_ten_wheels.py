#!/usr/bin/env python3
"""Import the ten fascicles of CBETA T0411 from the licensed HTML edition."""

from html.parser import HTMLParser
from pathlib import Path
from urllib.request import Request, urlopen


SOURCE = "https://tripitaka.zensoul.org/T/T0411/{volume}"
OUTPUT = Path(__file__).resolve().parents[1] / "books" / "dizang-ten-wheels"


class SutraHTMLParser(HTMLParser):
    BLOCK_TAGS = {"p", "h2", "h3"}

    def __init__(self):
        super().__init__(convert_charrefs=True)
        self.in_article = False
        self.article_depth = 0
        self.skip_depth = 0
        self.current: list[str] | None = None
        self.current_tag: str | None = None
        self.blocks: list[str] = []

    @staticmethod
    def classes(attrs):
        return set(dict(attrs).get("class", "").split())

    def handle_starttag(self, tag, attrs):
        classes = self.classes(attrs)
        if tag == "article" and "sutra" in classes:
            self.in_article = True
            self.article_depth = 1
            return
        if not self.in_article:
            return
        self.article_depth += 1
        if self.skip_depth:
            self.skip_depth += 1
            return
        if (tag == "sup" and "fn" in classes) or tag in {"rt", "script", "style"}:
            self.skip_depth = 1
            return
        is_verse = tag == "span" and "l" in classes
        if self.current is None and (tag in self.BLOCK_TAGS or is_verse):
            if "docnum" in classes:
                self.skip_depth = 1
                return
            self.current = []
            self.current_tag = tag
        if tag == "br" and self.current is not None:
            self.current.append("\n")
        if tag == "img" and self.current is not None:
            alt = dict(attrs).get("alt")
            if alt:
                self.current.append(alt)

    def handle_endtag(self, tag):
        if not self.in_article:
            return
        if self.skip_depth:
            self.skip_depth -= 1
        elif self.current is not None and tag == self.current_tag:
            text = "".join(self.current).strip()
            if text:
                self.blocks.append(text)
            self.current = None
            self.current_tag = None
        self.article_depth -= 1
        if tag == "article" and self.article_depth == 0:
            self.in_article = False

    def handle_data(self, data):
        if self.in_article and not self.skip_depth and self.current is not None:
            self.current.append(data)


def fetch(volume: int) -> str:
    request = Request(SOURCE.format(volume=volume), headers={"User-Agent": "SutraMem-Library/1.0"})
    with urlopen(request, timeout=30) as response:
        return response.read().decode("utf-8")


def main():
    OUTPUT.mkdir(parents=True, exist_ok=True)
    for volume in range(1, 11):
        parser = SutraHTMLParser()
        parser.feed(fetch(volume))
        if not parser.blocks:
            raise RuntimeError(f"No scripture content found for volume {volume}")
        text = "\n\n".join(parser.blocks).strip() + "\n"
        destination = OUTPUT / f"{volume:03}.txt"
        destination.write_text(text, encoding="utf-8")
        print(f"wrote {destination.relative_to(OUTPUT.parent.parent)} ({len(text)} characters)")


if __name__ == "__main__":
    main()
