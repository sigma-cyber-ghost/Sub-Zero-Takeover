# ❄️ Sub-Zero-Takeover

## 🕸️ Black Hat Hacker Edition – Subdomain Takeover Scanner

A high-speed, async-powered subdomain takeover scanner for red/black teamers, bug bounty hunters, and cyber spectres.

> Fast as shadow. Silent as DNS. Fatal as takeover.

---

## ⚙️ Features

- 🔍 Scans thousands of subdomains in minutes (e.g., 100K+ under 15 min)
- ⚡ Fully asynchronous using `aiohttp`
- 💥 Detects vulnerable subdomains (Heroku, GitHub, Netlify, etc.)
- 🧪 Verifies using real HTTP responses, not just DNS
- 🔧 Customizable thread count and timeout
- 📊 Live progress animation using Rich
- 📁 Outputs clean, structured JSON results
- 🧱 CLI-friendly and scriptable

---

## 🧠 How It Works

1. Accepts a domain and a subdomain wordlist  
2. Constructs all possible subdomain combinations (e.g., `admin.example.com`)  
3. Sends asynchronous HTTP(S) requests to each target  
4. Detects takeover signatures in the HTML response  
5. Saves results in `shadowdns_results.json`

---

## 📦 Installation

```bash
git clone https://github.com/sigma-cyber-ghost/Sub-Zero-Takeover.git
cd Sub-Zero-Takeover
pip3 install aiohttp rich dnspython selenium  
```
## ⚡ Performance Tips

--threads	More concurrency (500–1000 is fast)
--timeout	Lower = faster, but risk timeout
Use fast DNS	Speeds up resolving dramatically
VPS / VPS SSD	More stable under high thread count

## 🔥 Example Wordlists
Try these for better results:
```bash
/usr/share/seclists/Discovery/DNS/subdomains-top1million-110000.txt
Custom org-specific recon wordlists
```

##🚀 Usage

## 🔎 Basic Scan
```bash
python3 shadowdns.py example.com /usr/share/seclists/Discovery/DNS/subdomains-top1million-110000.txt
```
## ⚡ With More Threads
```bash
python3 shadowdns.py example.com /usr/share/seclists/Discovery/DNS/subdomains-top1million-110000.txt --threads 500
```
## ⏱ Custom Timeout (default: 2s)
```bash
python3 shadowdns.py example.com /usr/share/seclists/Discovery/DNS/subdomains-top1million-110000.txt --timeout 1
```

## 🌐 Connect With Us

[![Telegram](https://img.shields.io/badge/Telegram-Sigma_Ghost-blue?logo=telegram)](https://t.me/Sigma_Cyber_Ghost)  [![YouTube](https://img.shields.io/badge/YouTube-Sigma_Ghost-red?logo=youtube)](https://www.youtube.com/@sigma_ghost_hacking)  [![Instagram](https://img.shields.io/badge/Instagram-Safder_Khan-purple?logo=instagram)](https://www.instagram.com/safderkhan0800_/)  [![Twitter](https://img.shields.io/badge/Twitter-@safderkhan0800_-1DA1F2?logo=twitter)](https://twitter.com/safderkhan0800_)
