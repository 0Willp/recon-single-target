# 🎯 Script de Reconhecimento de um único alvo.

![Python](https://img.shields.io/badge/Python-3.8%2B-blue.svg)
![Bash](https://img.shields.io/badge/Shell-Automation-green.svg)
![Status](https://img.shields.io/badge/Status-Active-success.svg)

Um pipeline modular, automatizado e silencioso de enumeração de subdomínios, projetado para extrair o máximo de domínios de um **único alvo**, limpar o ruído e verificar a existência de servidores web ativos.

## 🧠 Metodologia do Fluxo

1. **Enumeração de Subdomínios:** Obtém subdomínios de forma passiva utilizando `subfinder`, `assetfinder`, `findomain` e `amass`.
2. **Alertas em Tempo Real:** Envia uma notificação via Slack/Discord (utilizando o `notify` da ProjectDiscovery) assim que cada ferramenta conclui sua tarefa.
3. **Higienização de Dados:** Consolida todas as saídas, remove duplicatas e filtra falsos positivos para gerar um arquivo `.txt` limpo e organizado.
4. **Web Probing:** Direciona a lista limpa para o `httpx` a fim de verificar portas HTTP/HTTPS ativas.
5. **Limpeza:** Exclui automaticamente arquivos temporários específicos das ferramentas, mantendo seu ambiente de trabalho organizado.


## 📂 Estrutura de Diretórios

Este script pressupõe que você possua uma estrutura profissional de VPS para Bug Bounty. Ele salvará automaticamente a saída em `~/bounty/targets/`:

```bash
~/bounty/
├── targets/         <-- Saída do script
│   └── [example.com/](https://exemplo.com/)
│       ├── 01_all_subs_merged.txt
│       └── 02_alive_httpx.txt
├── tools/           
└── wordlists/
```

## 🛠️ Pré-requisitos

Certifique-se de que as seguintes ferramentas estejam instaladas e disponíveis no `$PATH` do seu sistema:

* [Python 3.x](https://www.python.org/)
* `git` (native on Linux distributions)
* [Subfinder](https://github.com/projectdiscovery/subfinder)
* [Assetfinder](https://github.com/tomnomnom/assetfinder)
* [Findomain](https://github.com/Findomain/Findomain)
* [Amass](https://github.com/owasp-amass/amass)
* [Httpx](https://github.com/projectdiscovery/httpx)
* [Notify](https://github.com/projectdiscovery/notify) 

## 🚀 Usage
Execute o script passando o argumento -d, o domínio a ser enumerado:
```bash
python3 recon_single.py -d hackerone.com
```

## 🐼 Mentalidade
"Ferramentas não encontram bugs; pesquisadores, sim. As ferramentas apenas tornam o palheiro menor."

## ⚖️ Aviso Legal
Este projeto destina-se exclusivamente a fins educacionais e de pesquisa ética em segurança. O autor não se responsabiliza por qualquer uso indevido das ferramentas instaladas por este script. Realize testes apenas em sistemas dentro do escopo autorizado.

Desenvolvido por 0WILLP 
🐼 | Escrevendo código e encontrando bugs.


