ANONIMIZADOR LOCAL DE PDF v3

Fluxo:
1. Execute anonimizador_pdf.py (ou compile o EXE com build_exe.bat).
2. Clique em "1. Selecionar PDF".
3. Informe termos e/ou marque CPF, E-mail e Telefone.
4. Clique em "2. Analisar PDF". O painel Status mostra ocorrencias e paginas sem texto.
5. Revise visualmente. Arraste o mouse sobre areas que devam ser removidas.
6. Clique em "4. GERAR PDF ANONIMIZADO" e escolha um NOVO arquivo.
7. Opcional: clique em "5. Verificar ultimo resultado".

IMPORTANTE:
- O original nunca deve ser sobrescrito.
- Tarjas sao aplicadas como redactions do PDF, inclusive sobre pixels de imagens.
- Paginas escaneadas sem camada textual exigem revisao/marcacao visual.
- A verificacao automatica cobre a camada textual; sempre faca revisao visual final.
- O processamento e local. O programa nao envia o PDF para a internet.

CRIAR EXE:
- Instale Python 3 para Windows, se necessario.
- Execute build_exe.bat.
- O executavel sera criado em dist\AnonimizadorPDF_v3.exe.
