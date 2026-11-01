# Manutenção do Anonimizador PDF

- Comunique-se em português, a menos que o usuário solicite outro idioma.
- Aplicativo desktop local em Python/Tkinter, com PyMuPDF; não enviar PDFs ou termos a serviços externos.
- Fonte principal: `anonimizador_pdf.py`. Traduções: `i18n.py`. Versão: `version.py`.
- Preserve a seleção Português/English; novos textos devem passar por `tr`. Identificadores de padrões e chaves do relatório JSON são estáveis e não devem ser traduzidos.
- Não sobrescreva PDFs originais. A verificação automática cobre somente texto; mantenha a orientação de revisão visual.
- O relatório JSON contém termos e caminhos potencialmente sensíveis. Não incluir PDFs, relatórios, segredos ou dados reais nos commits/testes.
- Use dados sintéticos nos testes: `python -m unittest discover -s tests -v`.
- Para executável Windows: `python -m pip install -r requirements-build.txt`, depois `python build.py` (ou `build_exe.bat`).
- Versões novas: atualizar `version.py` e `CHANGELOG.md`; gerar EXE e SHA-256 em `dist/`. Preserve o EXE v3 original. Não versionar `dist/` ou `build/`.
- Antes de entregar: rodar testes, verificar mudanças com Git e informar o que foi validado e o que ainda depende de revisão manual.
- Publicações: entregar executável e fonte correspondente juntos em GitHub Releases; somente criar tag/release quando solicitado.
- Titular e conta GitHub: `griback`. Nome confirmado: `pdf-anonimator`. O usuário confirmou autoria, autorização de publicação pública e pediu licença livre; adotada AGPL-3.0-only. Preserve `LICENSE`, `NOTICE` e os avisos de terceiros.
- A publicação pública está autorizada neste destino; a autenticação GitHub ainda precisa estar disponível. Consulte `PUBLICACAO.md` para o estado atual. Não solicitar novamente informações já confirmadas.
