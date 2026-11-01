"""Portuguese source messages and English translations; no network access."""
_language = "pt_BR"

def set_language(language):
    global _language
    if language not in ("pt_BR", "en"):
        raise ValueError("Unsupported language: " + language)
    _language = language

def get_language():
    return _language

def tr(message, **values):
    template = EN.get(message, message) if _language == "en" else message
    return template.format(**values) if values else template

EN = {'Anonimizador Local de PDF': 'Local PDF Redactor',
 'PyMuPDF não está instalado.': 'PyMuPDF is not installed.',
 'Redação permanente de texto e áreas visuais — processamento local.': 'Permanent text and image '
                                                                       'redaction — local '
                                                                       'processing.',
 '1. Selecionar PDF': '1. Select PDF',
 '2. Analisar PDF': '2. Analyze PDF',
 'Termos específicos (um por linha)': 'Specific terms (one per line)',
 'Detecção automática': 'Automatic detection',
 'Status / análise': 'Status / analysis',
 '4. GERAR PDF ANONIMIZADO': '4. GENERATE REDACTED PDF',
 '5. Verificar último resultado': '5. Verify last output',
 'Página - / -': 'Page - / -',
 'Desfazer área': 'Undo area',
 'Limpar página': 'Clear page',
 '3. Revisão visual: arraste o mouse sobre qualquer área que também deva ser eliminada.': '3. '
                                                                                          'Visual '
                                                                                          'review: '
                                                                                          'drag '
                                                                                          'over '
                                                                                          'any '
                                                                                          'additional '
                                                                                          'area to '
                                                                                          'remove.',
 'PDF carregado. Clique em “2. Analisar PDF”.': 'PDF loaded. Click “2. Analyze PDF”.',
 'Primeiro selecione um PDF válido.': 'Select a valid PDF first.',
 'Analisando PDF...': 'Analyzing PDF...',
 'Nenhum termo específico informado.': 'No specific terms entered.',
 'Análise concluída. Revise visualmente e use “4. GERAR PDF ANONIMIZADO”.': 'Analysis complete. '
                                                                            'Review visually and '
                                                                            'use “4. GENERATE '
                                                                            'REDACTED PDF”.',
 'Não há nada selecionado para anonimizar.': 'Nothing selected for redaction.',
 'Não sobrescreva o PDF original.': 'Do not overwrite the original PDF.',
 'Processando redações...': 'Applying redactions...',
 '=== PDF GERADO ===': '=== PDF GENERATED ===',
 'AVISO: ': 'WARNING: ',
 'Saída: ': 'Output: ',
 'Relatório: ': 'Report: ',
 'PDF anonimizado criado.\n\nFaça também uma revisão visual final.': 'Redacted PDF created.\n'
                                                                     '\n'
                                                                     'Perform a final visual '
                                                                     'review as well.',
 '=== NOVA VERIFICAÇÃO ===': '=== NEW VERIFICATION ===',
 'Resultado: ': 'Result: ',
 'ATENÇÃO — ainda há conteúdo pesquisável correspondente.': 'WARNING — matching searchable content '
                                                            'remains.',
 'OK — nenhum termo/padrão selecionado foi localizado na camada textual.': 'OK — no selected '
                                                                           'terms/patterns found '
                                                                           'in the text layer.',
 'ERRO: ': 'ERROR: ',
 'PyMuPDF não encontrado. Execute instalar.bat ou instale requirements.txt.': 'PyMuPDF not found. '
                                                                              'Run instalar.bat or '
                                                                              'install '
                                                                              'requirements.txt.',
 'nenhuma': 'none',
 'sim': 'yes',
 'não/aparentemente vazios': 'no/apparently empty',
 'Página {v0}: pouco/nenhum texto pesquisável; revise visualmente.': 'Page {v0}: little/no '
                                                                     'searchable text; review '
                                                                     'visually.',
 'Termo ainda extraível: {v0}': 'Term still extractable: {v0}',
 'Padrão {v0} ainda possui ocorrência extraível.': 'Pattern {v0} still has an extractable match.',
 'Páginas: {v0}': 'Pages: {v0}',
 'Páginas com pouco/nenhum texto: {v0}': 'Pages with little/no text: {v0}',
 'Metadados presentes: {v0}': 'Metadata present: {v0}',
 'Página {v0} / {v1}': 'Page {v0} / {v1}',
 'Área manual adicionada na página {v0}.': 'Manual area added on page {v0}.',
 'Áreas manuais: {v0}': 'Manual areas: {v0}',
 'Verificação textual automática: {v0}': 'Automatic text verification: {v0}',
 '{v0}: {v1} possível(is) ocorrência(s)': '{v0}: {v1} possible match(es)',
 'Termo “{v0}”: {v1} removida(s)': 'Term “{v0}”: {v1} removed',
 '{v0}: {v1} removida(s)': '{v0}: {v1} removed',
 'Termo “{v0}”: {v1} restante(s)': 'Term “{v0}”: {v1} remaining',
 '{v0}: {v1} restante(s)': '{v0}: {v1} remaining',
 'Termo “{v0}”: {v1} ocorrência(s) encontrada(s)': 'Term “{v0}”: {v1} match(es) found',
 'Telefone': 'Phone (Brazil)',
 'ATENÇÃO': 'WARNING'}
