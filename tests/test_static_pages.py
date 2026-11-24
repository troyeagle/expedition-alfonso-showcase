import importlib.util
from pathlib import Path
import tempfile
import unittest

ROOT = Path(__file__).resolve().parents[1]
spec = importlib.util.spec_from_file_location('static_pages', ROOT / 'scripts/build_static_pages.py')
builder = importlib.util.module_from_spec(spec)
spec.loader.exec_module(builder)


class StaticPagesTests(unittest.TestCase):
    def test_release_preserves_scene_and_license_without_local_evidence(self):
        with tempfile.TemporaryDirectory() as temp:
            output = builder.build_site(Path(temp) / 'dist')
            self.assertEqual({p.name for p in output.iterdir()}, {'index.html', 'LICENSE.txt'})
            self.assertEqual((output / 'index.html').read_bytes(), (ROOT / 'assets/public-source.html').read_bytes())
            self.assertEqual((output / 'LICENSE.txt').read_bytes(), (ROOT / 'LICENSE').read_bytes())
            builder.validate_page((output / 'index.html').read_text(), (ROOT / 'assets/embedded-scene.html').read_text())

    def test_stale_or_multiple_embedded_scenes_are_rejected(self):
        for page in ['<iframe data-srcdoc="old"></iframe>', '<iframe data-srcdoc="scene"></iframe><iframe data-srcdoc="scene"></iframe>']:
            with self.subTest(page=page), self.assertRaises(ValueError):
                builder.validate_page(page, 'scene')

    def test_standalone_page_cannot_depend_on_unpublished_files(self):
        with self.assertRaises(ValueError):
            builder.validate_page('<iframe data-srcdoc="scene"></iframe><script src="private.js"></script>', 'scene')

    def test_inline_svg_data_and_fragment_references_remain_supported(self):
        scene='<svg><use href="#icon"/></svg><img src="data:image/png;base64,eA==">'
        from html import escape
        builder.validate_page('<iframe data-srcdoc="'+escape(scene,quote=True)+'"></iframe>', scene)


if __name__ == '__main__':
    unittest.main()
