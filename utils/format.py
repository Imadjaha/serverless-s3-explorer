import re
import mimetypes
from dash import html


def icon(path: str) -> str:
    if path.endswith("/"):
        return "bi bi-folder-fill text-primary"
    mt = mimetypes.guess_type(path)[0] or ""
    return (
        "bi bi-file-earmark-image" if mt.startswith("image/") else "bi bi-file-earmark"
    )


def human_bytes(b: int) -> str:
    for u in ["B", "KiB", "MiB", "GiB", "TiB"]:
        if b < 1024 or u == "TiB":
            return f"{b:.1f} {u}" if u != "B" else f"{b} B"
        b /= 1024


def highlight(text: str, needle: str):
    if not needle:
        return [text]
    segs, last = [], 0
    for m in re.finditer(re.escape(needle), text, re.I):
        if m.start() > last:
            segs.append(text[last : m.start()])
        segs.append(html.Mark(text[m.start() : m.end()]))
        last = m.end()
    segs.append(text[last:])
    return segs
