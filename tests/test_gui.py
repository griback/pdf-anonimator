"""Exercise the actual Tk widgets and document state during language changes."""
import unittest

import pymupdf

from anonimizador_pdf import App
from i18n import set_language


class LanguageSwitchTests(unittest.TestCase):
    def test_language_switch_keeps_document_and_result(self):
        set_language('pt_BR')
        self.addCleanup(set_language, 'pt_BR')
        app = App()
        app.withdraw()
        self.addCleanup(app.destroy)
        app.doc = pymupdf.open()
        self.addCleanup(app.doc.close)
        app.doc.new_page().insert_text((72, 72), 'Example Person')
        app.terms.insert('1.0', 'Example Person')
        app.manual = {0: [(10, 20, 30, 40)]}
        app.cpf.set(True)
        app.last = ('output.pdf', ['Example Person'], {'CPF': True})
        result = app.last
        app.gen.configure(state='normal')
        app.ver.configure(state='normal')
        for language, button in [('English', '2. Analyze PDF'), ('Português', '2. Analisar PDF')]:
            app.language.set(language)
            app.switch_language()
            self.assertEqual(app.an_btn['text'], button)
            self.assertEqual(app.terms.get('1.0', 'end-1c'), 'Example Person')
            self.assertEqual(app.manual, {0: [(10, 20, 30, 40)]})
            self.assertEqual(app.last, result)
            self.assertTrue(app.cpf.get())
            self.assertEqual(str(app.ver['state']), 'normal')
            self.assertEqual(str(app.gen['state']), 'normal')
            self.assertIsNotNone(app.img)
