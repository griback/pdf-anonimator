# Publicação no GitHub

## Estado

- Repositório Git local inicializado em `main`; primeiro commit preserva o fonte v3 recebido.
- Sem remoto GitHub configurado. Conta, nome do repositório e licença aguardam confirmação.
- Não houve envio de código, criação de repositório público ou publicação de release.
- GitHub CLI (`gh`) não foi encontrado neste ambiente durante a preparação inicial.

## Antes da primeira publicação

1. Confirmar autoria/permissão para publicar e escolher uma licença considerando a licença AGPL/comercial do PyMuPDF. Adicionar o texto completo em `LICENSE` e atualizar README/CONTRIBUTING.
2. Informar a conta/organização e nome desejado. Autenticar no GitHub pelo navegador ou CLI; não colar tokens em chats ou arquivos.
3. Revisar arquivos e histórico a publicar; não enviar PDFs, relatórios ou arquivos de `dist/`.
4. Criar o repositório público vazio no GitHub e configurar o remoto com sua URL real:

```powershell
git remote add origin https://github.com/CONTA/REPOSITORIO.git
git push -u origin main
```

Os nomes acima são exemplos; substituí-los pelos dados confirmados. Se o repositório já existir, inspecionar seu conteúdo antes de integrar.

## Próximas versões

1. Trabalhar em uma branch, revisar mudanças e executar testes.
2. Atualizar `version.py` e `CHANGELOG.md`. Fazer revisão visual em português e inglês, incluindo PDFs escaneados.
3. Executar `build_exe.bat`; verificar o EXE em uma máquina Windows sem Python quando possível.
4. Integrar a mudança em `main`. Quando solicitada a publicação, criar tag `vX.Y.Z` correspondente a `version.py`.
5. Rodar o workflow **Windows executable** manualmente no GitHub, selecionando a tag. Ele valida, compila e guarda EXE/checksum como artefatos, sem publicar automaticamente.
6. Criar uma GitHub Release da mesma tag e anexar EXE e SHA-256. GitHub também oferece o código-fonte da tag. Incluir licença e avisos exigidos pelas dependências na distribuição conforme a licença escolhida.

Os workflows só poderão ser verificados no GitHub após o primeiro envio. Não há assinatura digital do executável configurada.
