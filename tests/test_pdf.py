import hashlib
import json
from pathlib import Path
import tempfile
import unittest

import pymupdf as fitz
from anonimizador_pdf import inspect_pdf, redact, variants
from i18n import EN, set_language, tr
from string import Formatter


class PDFTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name)
        self.src = self.root / 'input.pdf'
        self.dst = self.root / 'output.pdf'
        with fitz.open() as doc:
            page = doc.new_page()
            page.insert_text((72, 72), 'Example Person')
            page.insert_text((72, 110), '123.456.789-00')
            page.insert_text((72, 150), 'example@example.org')
            page.insert_text((72, 190), '(11) 91234-5678')
            page.insert_text((72, 230), 'Keep this public text')
            doc.set_metadata({'author': 'Example Person'})
            doc.save(self.src)
        set_language('pt_BR')
        self.addCleanup(set_language, 'pt_BR')

    def test_inspection(self):
        pages, terms, patterns, _ = inspect_pdf(str(self.src), ['Example Person'], {'CPF': True, 'E-mail': True})
        self.assertEqual(len(pages), 1)
        self.assertEqual(terms['Example Person'], 1)
        self.assertEqual(patterns, {'CPF': 1, 'E-mail': 1})

    def test_redaction_preserves_source_removes_text_and_metadata(self):
        before = hashlib.sha256(self.src.read_bytes()).digest()
        report, path = redact(str(self.src), str(self.dst), ['Example Person'], {'CPF': True, 'E-mail': True, 'Telefone': True}, {})
        with fitz.open(self.dst) as doc:
            text = doc[0].get_text()
            for secret in ['Example Person', '123.456.789-00', 'example@example.org', '91234-5678']:
                self.assertNotIn(secret, text)
            self.assertIn('Keep this public text', text)
            self.assertFalse(doc.metadata.get('author'))
        self.assertEqual(before, hashlib.sha256(self.src.read_bytes()).digest())
        self.assertEqual(report['verification']['status'], 'OK')
        self.assertEqual(json.loads(Path(path).read_text(encoding='utf-8')), report)

    def test_manual_area(self):
        report, _ = redact(str(self.src), str(self.dst), [], {}, {0: [(65, 55, 200, 80)]})
        self.assertEqual(report['manual_redactions'], 1)
        with fitz.open(self.dst) as doc:
            self.assertNotIn('Example Person', doc[0].get_text())
            self.assertIn('Keep this public text', doc[0].get_text())

    def test_original_cannot_be_output(self):
        before = self.src.read_bytes()
        with self.assertRaises(ValueError):
            redact(str(self.src), str(self.src), [], {}, {})
        self.assertEqual(before, self.src.read_bytes())

    def test_blank_page_warns_in_english(self):
        with fitz.open() as doc:
            doc.new_page()
            doc.save(self.root / 'blank.pdf')
        set_language('en')
        report, _ = redact(str(self.root / 'blank.pdf'), str(self.dst), [], {}, {})
        self.assertIn('review visually', report['warnings'][0])

    def test_cpf_variants(self):
        self.assertEqual(set(variants('12345678900')), {'12345678900', '123.456.789-00'})


class TranslationTests(unittest.TestCase):
    def tearDown(self):
        set_language('pt_BR')

    def test_translation_and_formatting(self):
        set_language('en')
        self.assertEqual(tr('Página {v0} / {v1}', v0=2, v1=5), 'Page 2 / 5')
        set_language('pt_BR')
        self.assertEqual(tr('Página {v0} / {v1}', v0=2, v1=5), 'Página 2 / 5')

    def test_placeholders_match_for_all_translations(self):
        for source, target in EN.items():
            fields = lambda text: {key for _, key, _, _ in Formatter().parse(text) if key is not None}
            self.assertEqual(fields(source), fields(target), source)


if __name__ == '__main__':
    unittest.main()
