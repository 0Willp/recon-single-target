# 🎯 Recon Single Target — enumeração de subdomínios de um alvo

![Python](https://img.shields.io/badge/Python-3.8%2B-blue.svg)
![Bash](https://img.shields.io/badge/Shell-Automation-green.svg)
![Status](https://img.shields.io/badge/Status-Active-success.svg)

Pipeline automatizado e silencioso de enumeração de subdomínios, projetado para extrair o máximo de subdomínios de um **único domínio raiz**, validar o escopo, remover ruído e verificar quais hosts têm servidor web ativo.

> Para processar uma lista de domínios de uma vez, use o projeto irmão [recon-multiple-targets](https://github.com/0Willp/recon-multiple-targets).

## 🧠 Metodologia do Fluxo

1. **Enumeração passiva:** coleta subdomínios com `subfinder`, `assetfinder`, `findomain` e `amass enum -passive`.
2. **Alertas em tempo real:** dispara uma notificação (via `notify` da ProjectDiscovery, ex.: Telegram/Slack/Discord) ao término de cada ferramenta.
3. **Higienização + validação de escopo:** consolida todas as saídas, normaliza, remove duplicatas e mantém **apenas** o próprio domínio ou subdomínios reais dele (`sub == domínio` ou `sub` termina em `.domínio`) — descartando falsos positivos como `fakeexample.com` para o alvo `example.com`.
4. **Web probing:** envia a lista limpa para o `httpx`, identificando hosts com HTTP/HTTPS ativos.
5. **Limpeza:** remove os arquivos temporários de cada ferramenta, mantendo só os resultados finais.

## 📂 Estrutura de diretórios

O script pressupõe uma estrutura de VPS para Bug Bounty e salva a saída em `~/bounty/targets/<domínio>/`:

```text
~/bounty/
├── targets/                     <-- saída do script
│   └── example.com/
│       ├── 01_all_subs_merged.txt   (subdomínios únicos, já validados por escopo)
│       └── 02_alive_httpx.txt       (hosts com web ativo)
├── tools/
└── wordlists/
```

Os arquivos temporários (`temp_subfinder.txt`, `temp_assetfinder.txt`, `temp_findomain.txt`, `temp_amass.txt`) são criados durante a execução e removidos ao final.

## 🛠️ Pré-requisitos

Tenha as seguintes ferramentas instaladas e no `$PATH`:

* [Python 3.8+](https://www.python.org/)
* [subfinder](https://github.com/projectdiscovery/subfinder)
* [assetfinder](https://github.com/tomnomnom/assetfinder)
* [findomain](https://github.com/Findomain/Findomain)
* [amass](https://github.com/owasp-amass/amass)
* [httpx](https://github.com/projectdiscovery/httpx)
* [notify](https://github.com/projectdiscovery/notify) — opcional, apenas para os alertas. Requer o `provider-config.yaml` configurado (Telegram/Slack/Discord).

> ⚠️ As saídas de tela são silenciosas (`stdout`/`stderr` descartados). Se uma ferramenta não estiver instalada, o passo correspondente simplesmente reportará `0` — confira o `$PATH` antes de concluir que o alvo está "limpo".

## 🚀 Uso

Passe `-d` com o domínio a ser enumerado:

```bash
python3 recon_single.py -d hackerone.com
```

## 🐼 Mentalidade
"Ferramentas não encontram bugs; pesquisadores, sim. As ferramentas apenas tornam o palheiro menor."

## ⚖️ Aviso Legal
Este projeto destina-se exclusivamente a fins educacionais e de pesquisa ética em segurança. O autor não se responsabiliza por qualquer uso indevido. Realize testes apenas em sistemas dentro do escopo autorizado.

Desenvolvido por 0WILLP
🐼 | Escrevendo código e encontrando bugs.
