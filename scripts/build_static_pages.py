"""Publish only the rebuilt standalone page and its software license."""
from html import unescape
from html.parser import HTMLParser
from pathlib import Path
import re
import shutil
import subprocess
import sys
from urllib.parse import urlsplit

ROOT = Path(__file__).resolve().parents[1]


def validate_page(page, scene):
    matches = re.findall(r'data-srcdoc="(.*?)"', page, flags=re.S)
    if len(matches) != 1 or unescape(matches[0]) != scene:
        raise ValueError('The standalone page must embed the exact current scene')
    class References(HTMLParser):
        def handle_starttag(self, tag, attrs):
            for key, url in attrs:
                if key not in {'href', 'src', 'poster', 'xlink:href'} or not url:
                    continue
                parsed = urlsplit(url)
                if parsed.path and not parsed.scheme and not parsed.netloc:
                    raise ValueError(f'The standalone page references an unpublished local file: {url}')
    for html in [page, scene]:
        References(convert_charrefs=True).feed(html)


def build_site(output=None, root=ROOT):
    subprocess.run([sys.executable, str(root / 'build-page.py')], check=True)
    page = (root / 'assets/public-source.html').read_text()
    scene = (root / 'assets/embedded-scene.html').read_text()
    validate_page(page, scene)
    output = Path(output) if output is not None else root / 'dist'
    if output.is_symlink():
        raise ValueError('Output directory must not be a symlink')
    if output.exists():
        shutil.rmtree(output)
    output.mkdir(parents=True)
    shutil.copyfile(root / 'assets/public-source.html', output / 'index.html')
    shutil.copyfile(root / 'LICENSE', output / 'LICENSE.txt')
    print(f'Built standalone site and license: {output}')
    return output


if __name__ == '__main__':
    build_site()
