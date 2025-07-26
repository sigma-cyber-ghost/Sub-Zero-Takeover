#!/usr/bin/env python3
import asyncio, aiohttp, json, os, sys, time, argparse
from urllib.parse import urlparse
from rich.console import Console
from rich.progress import Progress, SpinnerColumn, TextColumn, TimeElapsedColumn

console = Console()
subdomains, takeovers = set(), set()
BANNER = r"""
⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⡿⠋⠁⠀⠀⠈⠉⠙⠻⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿
⣿⣿⣿⣿⣿⣿⣿⣿⣿⡟⠀⠀⠀⠀⠀⠀⠀⠀⠀⠈⠻⣿⣿⣿⣿⣿⣿⣿⣿⣿
⣿⣿⣿⣿⣿⣿⣿⣿⡟⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠈⢻⣿⣿⣿⣿⣿⣿⣿
⣿⣿⣿⣿⣿⣿⣿⡟⠀⠀⠀⠀⠀⢀⣠⣤⣤⣤⣤⣄⠀⠀⠀⠹⣿⣿⣿⣿⣿⣿
⣿⣿⣿⣿⣿⣿⣿⠁⠀⠀⠀⠀⠾⣿⣿⣿⣿⠿⠛⠉⠀⠀⠀⠀⠘⣿⣿⣿⣿⣿
⣿⣿⣿⣿⣿⣿⡏⠀⠀⠀⣤⣶⣤⣉⣿⣿⡯⣀⣴⣿⡗⠀⠀⠀⠀⣿⣿⣿⣿⣿
⣿⣿⣿⣿⣿⣿⡇⠀⠀⠀⡈⠀⠀⠉⣿⣿⣶⡉⠀⠀⣀⡀⠀⠀⠀⢻⣿⣿⣿⣿
⣿⣿⣿⣿⣿⣿⡇⠀⠀⠸⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⠇⠀⠀⠀⢸⣿⣿⣿⣿
⣿⣿⣿⣿⣿⣿⣿⠀⠀⠀⠉⢉⣽⣿⠿⣿⡿⢻⣯⡍⢁⠄⠀⠀⠀⣸⣿⣿⣿⣿
⣿⣿⣿⣿⣿⣿⣿⡄⠀⠀⠐⡀⢉⠉⠀⠠⠀⢉⣉⠀⡜⠀⠀⠀⠀⣿⣿⣿⣿⣿
⣿⣿⣿⣿⣿⣿⠿⠁⠀⠀⠀⠘⣤⣭⣟⠛⠛⣉⣁⡜⠀⠀⠀⠀⠀⠛⠿⣿⣿⣿
⡿⠟⠛⠉⠉⠀⠀⠀⠀⠀⠀⠀⠈⢻⣿⡀⠀⣿⠏⠀⠀⠀⠀⠀⠀⠀⠀⠀⠈⠉
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠉⠁⠀⠁⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
"""

SOCIALS = {
    "Twitter": "https://twitter.com/safderkhan0800_",
    "Instagram": "https://www.instagram.com/safderkhan0800_/",
    "YouTube": "https://www.youtube.com/@sigma_ghost_hacking",
    "Telegram": "https://t.me/Sigma_Cyber_Ghost"
}

def print_banner():
    console.print(BANNER.strip(), style="bold red")
    console.print("[bold white]SHADOWDNS WARP MODE[/bold white]")
    console.print("[cyan]Ultra Fast Passive Subdomain Takeover Scanner[/cyan]")
    for name, url in SOCIALS.items():
        console.print(f"[blue]{name}[/blue]: {url}")

def extract_host(src):
    return urlparse(src if "://" in src else f"http://{src}").hostname

async def resolve_subdomain(session, fqdn, timeout):
    try:
        async with session.get(f"https://{fqdn}", timeout=timeout, allow_redirects=True) as r:
            text = await r.text()
            if any(x in text.lower() for x in ['no such app', 'heroku', 'not found', 'github']):
                takeovers.add(fqdn)
            subdomains.add(fqdn)
    except:
        pass

async def scan(domain, wordlist, threads, timeout):
    conn = aiohttp.TCPConnector(limit_per_host=threads, limit=threads*2)
    async with aiohttp.ClientSession(connector=conn) as session:
        with open(wordlist, 'r', errors='ignore') as f:
            lines = [line.strip() for line in f if line.strip()]
        with Progress(
            SpinnerColumn(), TextColumn("[progress.description]{task.description}"),
            TimeElapsedColumn(), transient=False
        ) as progress:
            task = progress.add_task(f"Scanning {len(lines)} subdomains on {domain}", total=len(lines))
            semaphore = asyncio.Semaphore(threads)
            async def bounded_resolve(sub):
                fqdn = f"{sub}.{domain}"
                async with semaphore:
                    await resolve_subdomain(session, fqdn, timeout)
                progress.advance(task)
            await asyncio.gather(*[bounded_resolve(sub) for sub in lines])

def save(domain):
    with open("shadowdns_results.json", "w") as f:
        json.dump({
            "target": domain,
            "subdomains": sorted(subdomains),
            "takeovers": sorted(takeovers)
        }, f, indent=2)
    console.print("\n[green]✔ Results saved to shadowdns_results.json[/green]")

async def run(domain, wordlist, threads, timeout):
    print_banner()
    console.print(f"\n[bold green]Target:[/] {domain}")
    start = time.time()
    await scan(domain, wordlist, threads, timeout)
    save(domain)
    total = time.time() - start
    console.print(f"\n⏱️ Completed in {int(total // 60)}m {int(total % 60)}s")

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("target", help="Target domain or URL")
    parser.add_argument("wordlist", help="Subdomain wordlist path")
    parser.add_argument("--threads", type=int, default=500, help="Concurrent threads (default: 500)")
    parser.add_argument("--timeout", type=int, default=2, help="Timeout per request in seconds (default: 2)")
    args = parser.parse_args()

    domain = extract_host(args.target)
    try:
        asyncio.run(run(domain, args.wordlist, args.threads, args.timeout))
    except KeyboardInterrupt:
        console.print("[red]✖ Interrupted by user[/red]")
        sys.exit(0)
