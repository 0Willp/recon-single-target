# 🎯 Recon Single Target Pipeline

![Python](https://img.shields.io/badge/Python-3.8%2B-blue.svg)
![Bash](https://img.shields.io/badge/Shell-Automation-green.svg)
![Status](https://img.shields.io/badge/Status-Active-success.svg)

A modular, automated, and silent subdomain enumeration pipeline designed to extract the maximum amount of domains for a **single target**, clean the noise, and probe for alive web servers.

## 🧠 Flow Methodology

1. **Subdomain Enumeration:** Fetches subdomains passively using `subfinder`, `assetfinder`, `findomain`, and `amass`.
2. **Real-Time Alerts:** Sends a Slack/Discord notification (via ProjectDiscovery's `notify`) as soon as each tool finishes its job.
3. **Data Sanitization:** Merges all outputs, removes duplicates, and filters out false positives to create a pristine `.txt` file.
4. **Web Probing:** Pipes the clean list into `httpx` to verify active HTTP/HTTPS ports.
5. **Clean up:** Automatically deletes tool-specific temporary files, leaving your workspace organized.


## 📂 Directory Structure

This script assumes you have a professional Bug Bounty VPS structure. It will automatically save the output to `~/bounty/targets/`:

```text
~/bounty/
├── targets/         <-- Script output goes here
│   └── [example.com/](https://example.com/)
│       ├── 01_all_subs_merged.txt
│       └── 02_alive_httpx.txt
├── tools/           
└── wordlists/
```

## 🛠️ Prerequisites

Ensure the following tools are installed and available in your system's `$PATH`:

* [Subfinder](https://github.com/projectdiscovery/subfinder)
* [Assetfinder](https://github.com/tomnomnom/assetfinder)
* [Findomain](https://github.com/Findomain/Findomain)
* [Amass](https://github.com/owasp-amass/amass)
* [Httpx](https://github.com/projectdiscovery/httpx)
* [Notify](https://github.com/projectdiscovery/notify) 

## 🚀 Usage
Execute the script passing the argument -d, the domain to be enumerated:
```text
python3 recon_single.py -d hackerone.com
```


## ⚖️ Legal Disclaimer
This project is for educational and ethical security research purposes only. The author is not responsible for any misuse of the tools installed by this script. Only target systems within authorized scope.

Developed by 0WILLP 🐼 | Lifting code & Finding bugs


