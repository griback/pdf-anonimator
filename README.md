# Anonimizador Local de PDF

Aplicativo desktop para remover texto e áreas visuais de PDFs com processamento local. Interface em **Português** e **English**, selecionável no topo da janela. Não envia documentos à internet.

## Uso

1. Abra o executável Windows em `dist/`, ou execute `python anonimizador_pdf.py` com as dependências instaladas.
2. Selecione o PDF; informe termos (um por linha) e/ou ative CPF, e-mail e telefone.
3. Analise o documento e revise todas as páginas. Arraste sobre áreas que também devam ser removidas.
4. Gere um **novo** PDF e faça revisão visual do resultado; a verificação automática examina a camada textual.

A detecção de CPF e telefone segue formatos brasileiros mesmo na interface em inglês. Não há OCR: páginas escaneadas exigem marcação visual. Não há garantia de anonimização completa de todo conteúdo de um PDF, como anexos ou estruturas especiais.

O relatório `*_relatorio.json` contém termos pesquisados e caminhos dos arquivos: trate-o como informação sensível e não o publique junto do PDF.

## Desenvolvimento no Windows

Python 3.14 é a versão usada na validação local e na configuração do GitHub Actions.

```powershell
py -3.14 -m venv .venv
.\.venv\Scripts\python.exe -m pip install -r requirements.txt
.\.venv\Scripts\python.exe anonimizador_pdf.py
.\.venv\Scripts\python.exe -m unittest discover -s tests -v
```

`instalar.bat` prepara o ambiente local. Para gerar o executável, use `build_exe.bat`: instala as dependências de compilação, executa os testes e interrompe em caso de erro. Alternativamente, instale `requirements-build.txt` e execute `python build.py`.

Saída atual: `dist/AnonimizadorPDF_v3.1.0.exe` e arquivo `.exe.sha256`. O executável `AnonimizadorPDF_v3.exe` é o legado preservado. O arquivo `AnonimizadorPDF_v3.spec` é referência da compilação antiga; o processo atual usa `build.py`.

## Manutenção e colaboração

Use o Codex aberto nesta pasta para solicitar correções e versões. As instruções permanentes estão em `AGENTS.md`; o histórico de mudanças, em `CHANGELOG.md`. Para cada alteração: descrever o objetivo, revisar o código, executar testes e registrar um commit. Prefira uma branch por melhoria e pull request para revisão.

Veja [CONTRIBUTING.md](CONTRIBUTING.md) e [PUBLICACAO.md](PUBLICACAO.md). `dist/`, PDFs, relatórios e ambientes locais ficam fora do Git. Executáveis devem ser distribuídos em Releases com a versão exata do fonte e o checksum.

**Licença do projeto pendente de definição pelo titular.** O PyMuPDF declara licença AGPL ou comercial; consulte [a documentação da dependência](https://pymupdf.readthedocs.io/en/latest/about.html). Este repositório ainda não está publicado e não tem licença de código aberto concedida.

## English

Local desktop PDF redaction tool with a Portuguese/English interface. Select a PDF, enter terms or enable Brazilian CPF/email/phone detection, review every page, mark additional areas and save to a new PDF. No OCR is included; scanned documents require visual redaction. Always review the resulting PDF visually. Reports include sensitive search terms and paths.

Use Python 3.14, install `requirements.txt`, then run `python anonimizador_pdf.py`. Run tests with `python -m unittest discover -s tests -v`. Build on Windows using `requirements-build.txt` and `python build.py`. The project license and initial public repository are pending owner confirmation.
