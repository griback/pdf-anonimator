# Publicação no GitHub

## Estado

- Repositório Git local inicializado em `main`; primeiro commit preserva o fonte v3 recebido.
- Destino confirmado pelo titular: `https://github.com/griback/pdf-anonimator.git`, remoto `origin`.
- O usuário confirmou autoria e autorização para publicação pública. Licença livre adotada: **AGPL-3.0-only**; texto integral em `LICENSE`, autoria em `NOTICE`.
- Não houve envio de código, criação de repositório público ou publicação de release.
- GitHub CLI (`gh`) não foi encontrado neste ambiente durante a preparação inicial.
- A integração GitHub foi instalada, mas suas ferramentas de repositório ainda não estão disponíveis nesta conversa. A nova consulta via Git não encontrou autenticação local; a consulta pública retornou HTTP 404 (repositório inexistente ou privado).
- Login oficial do Git Credential Manager iniciado; envio depende de o titular concluir a autorização em `https://github.com/login/device`. Não registrar códigos temporários, senhas ou tokens no projeto ou no chat.

## Antes da primeira publicação

1. Autoria, destino público e licença já definidos. Preservar `LICENSE`, `NOTICE` e `THIRD_PARTY_NOTICES.md`.
2. Conectar a conta GitHub no Codex, ou autenticar uma ferramenta GitHub local. Não colar tokens em chats ou arquivos.
3. Revisar arquivos e histórico a publicar; não enviar PDFs, relatórios ou arquivos de `dist/`.
4. Com autenticação disponível, verificar se `griback/pdf-anonimator` existe. Se não existir, criá-lo público e vazio, sem inicializar README/licença pelo GitHub. O remoto local usa a URL abaixo:

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

Os workflows só poderão ser verificados no GitHub após o primeiro envio. Não há assinatura digital do executável configurada.
