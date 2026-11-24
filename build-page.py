"""Rebuild the single-file page from the readable scene, preserving its host bridge."""
from html import escape, unescape
from pathlib import Path
import re

assets = Path(__file__).resolve().parent / "assets"
page = assets / "public-source.html"
scene = (assets / "embedded-scene.html").read_text()
source = page.read_text()
pattern = r'(data-srcdoc=")(.*?)(")'
assert len(re.findall(pattern, source, flags=re.S)) == 1
source = re.sub(pattern, lambda m: m[1] + escape(scene, quote=True) + m[3], source, flags=re.S)
page.write_text(source)
assert unescape(re.search(pattern, source, flags=re.S)[2]) == scene
print(f"Built {page} ({page.stat().st_size:,} bytes); embedded scene matches exactly.")
