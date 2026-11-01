# Publicação no GitHub

## Estado

- Repositório Git local inicializado em `main`; primeiro commit preserva o fonte v3 recebido.
- Destino confirmado pelo titular: `https://github.com/griback/pdf-anonimator.git`, remoto `origin`.
- O usuário confirmou autoria e autorização para publicação pública. Licença livre adotada: **AGPL-3.0-only**; texto integral em `LICENSE`, autoria em `NOTICE`.
- Repositório público criado e código enviado: https://github.com/griback/pdf-anonimator.
- Branch `main` local acompanha `origin/main`. Sem PDFs, relatórios pessoais ou executáveis no histórico.
- A versão 3.1.0 foi compilada e validada localmente; pacote e código-fonte estão em `dist/`. Ainda não há GitHub Release publicada.
- GitHub CLI (`gh`) não foi encontrado neste ambiente durante a preparação inicial.
- A integração GitHub está instalada. A autenticação local foi concluída pelo login oficial do Git Credential Manager no navegador; o envio foi confirmado pelo GitHub. Não registrar senhas ou tokens no projeto ou no chat.

## Integração configurada

1. Autoria, destino público e licença já definidos. Preservar `LICENSE`, `NOTICE` e `THIRD_PARTY_NOTICES.md`.
2. Autenticação local configurada pelo Git Credential Manager. Se o GitHub solicitar renovação, usar o login oficial no navegador. Não colar tokens em chats ou arquivos.
3. Revisar arquivos e histórico a publicar; não enviar PDFs, relatórios ou arquivos de `dist/`.
4. O repositório já foi criado e recebeu o histórico local. Para futuros envios após revisão, o remoto usa a URL abaixo:

```powershell
git remote -v
# origin: https://github.com/griback/pdf-anonimator.git
git push -u origin main
```

Se o repositório já existir, inspecionar seu conteúdo antes de integrar. Não sobrescrever histórico remoto ou usar envio forçado.

## Próximas versões

1. Trabalhar em uma branch, revisar mudanças e executar testes.
2. Atualizar `version.py` e `CHANGELOG.md`. Fazer revisão visual em português e inglês, incluindo PDFs escaneados.
3. Executar `build_exe.bat`; verificar o EXE em uma máquina Windows sem Python quando possível.
4. Integrar a mudança em `main`. Quando solicitada a publicação, criar tag `vX.Y.Z` correspondente a `version.py`.
5. Rodar o workflow **Windows executable** manualmente no GitHub, selecionando a tag. Ele valida, compila e guarda EXE/checksum como artefatos, sem publicar automaticamente.
6. Criar uma GitHub Release da mesma tag e anexar EXE e SHA-256. GitHub também oferece o código-fonte da tag. Incluir licença e avisos exigidos pelas dependências na distribuição conforme a licença escolhida.

Os workflows estão configurados no repositório; verificar seus resultados na aba Actions após cada envio. Não há assinatura digital do executável configurada.
