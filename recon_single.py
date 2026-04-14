#!/usr/bin/env python3
import os
import subprocess
import argparse
import time
from pathlib import Path

# ── ANSI Colors ───────────────────────────────────────────────────────────────
G, C, Y, R, B, RST = "\033[32m", "\033[36m", "\033[33m", "\033[31m", "\033[34m", "\033[0m"

def print_step(msg):  print(f"\n{C}[*]{RST} {msg}")
def print_ok(msg):    print(f"    {G}[+]{RST} {msg}")
def print_warn(msg):  print(f"    {Y}[!]{RST} {msg}")

def run_command(cmd: str) -> bool:
    result = subprocess.run(cmd, shell=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    return result.returncode == 0


def count_lines(filepath: Path) -> int:
    if not filepath.exists():
        return 0
    with open(filepath, 'r', errors='ignore') as f:
        return sum(1 for _ in f)


def send_notification(msg: str):
    subprocess.run(f'echo "{msg}" | notify -silent', shell=True)


def main():
    parser = argparse.ArgumentParser(description="Single Target Recon")
    parser.add_argument("-d", "--domain", required=True, help="Target domain (e.g., testphp.vulnweb.com)")
    args = parser.parse_args()
    domain = args.domain

    start_time = time.time()

    base_dir = Path(os.path.expanduser("~/bounty/targets")) / domain
    base_dir.mkdir(parents=True, exist_ok=True)

    print(f"\n{G}[+]{RST} Starting enumeration for: {domain}")
    print(f"{G}[+]{RST} Output directory: {base_dir}")

    subfinder_out = base_dir / "temp_subfinder.txt"
    assetfinder_out = base_dir / "temp_assetfinder.txt"
    findomain_out = base_dir / "temp_findomain.txt"
    amass_out = base_dir / "temp_amass.txt"

    final_merged = base_dir / "01_all_subs_merged.txt"
    final_httpx = base_dir / "02_alive_httpx.txt"

    stats = {}

    # Subfinder
    print_step("Running Subfinder...")
    run_command(f"subfinder -d {domain} -silent -o {subfinder_out}")
    stats['subfinder'] = count_lines(subfinder_out)
    send_notification(f"🎯 Subfinder finished in {domain}. Found: {stats['subfinder']} subdomains.")
    print_ok(f"Subfinder: {stats['subfinder']} found.")

    # Assetfinder
    print_step("Running Assetfinder...")
    run_command(f"assetfinder -subs-only {domain} > {assetfinder_out}")
    stats['assetfinder'] = count_lines(assetfinder_out)
    send_notification(f"🎯 Assetfinder finished in {domain}. Found: {stats['assetfinder']} subdomains.")
    print_ok(f"Assetfinder: {stats['assetfinder']} found.")

    # Findomain
    print_step("Running Findomain...")
    run_command(f"findomain -t {domain} -q -u {findomain_out}")
    stats['findomain'] = count_lines(findomain_out)
    send_notification(f"🎯 Findomain finished in {domain}. Found: {stats['findomain']} subdomains.")
    print_ok(f"Findomain: {stats['findomain']} found.")

    # Amass (Passive)
    print_step("Running Amass (Passive)... this may take a few minutes..")
    run_command(f"amass enum -passive -d {domain} -o {amass_out}")
    stats['amass'] = count_lines(amass_out)
    send_notification(f"🎯 Amass finished in {domain}. Found: {stats['amass']} subdomains.")
    print_ok(f"Amass: {stats['amass']} found.")

    # Cleaning & Deduplication
    print_step("Merging results and removing duplicates.")
    all_subs = set()
    for temp_file in [subfinder_out, assetfinder_out, findomain_out, amass_out]:
        if temp_file.exists():
            with open(temp_file, 'r', errors='ignore') as f:
                for line in f:
                    sub = line.strip().lower()
                    if sub.endswith(domain):
                        all_subs.add(sub)

    # Saving clean file
    with open(final_merged, 'w') as f:
        for sub in sorted(all_subs):
            f.write(sub + '\n')

    stats['merged'] = len(all_subs)
    print_ok(f"Total number of unique subdomains: {stats['merged']}")
    send_notification(f"🧹Blending in {domain} completed. Total number of unique subdomains: {stats['merged']}.")

    # Httpx
    print_step("Validating active subdomains with Httpx...")
    if stats['merged'] > 0:
        run_command(f"cat {final_merged} | httpx -silent -o {final_httpx}")
        stats['alive'] = count_lines(final_httpx)
    else:
        stats['alive'] = 0

    print_ok(f"Subdomains assets (HTTP/HTTPS): {stats['alive']}")

    end_time = time.time()
    elapsed_seconds = int(end_time - start_time)
    minutes, seconds = divmod(elapsed_seconds, 60)
    hours, minutes = divmod(minutes, 60)
    time_str = f"{hours}h {minutes}m {seconds}s" if hours > 0 else f"{minutes}m {seconds}s"
    send_notification(
        f"🚀 Recon completed in {domain}!\nAlive (httpx): {stats['alive']}/{stats['merged']}\n⏱️ Total time: {time_str}")

    # Clean up
    print_step("Clearing temporary files.")
    for temp_file in [subfinder_out, assetfinder_out, findomain_out, amass_out]:
        if temp_file.exists():
            temp_file.unlink()
    print_ok("Temporary files removed. Keeping only the clean RAW file and the live HTTPX.")

    # Resume
    print(f"\n{G}{'─' * 46}{RST}")
    print(f"{G}  Summary of the Enumeration › {domain}{RST}")
    print(f"{G}{'─' * 46}{RST}")
    print(f"  Subfinder:    {stats['subfinder']}")
    print(f"  Assetfinder:  {stats['assetfinder']}")
    print(f"  Findomain:    {stats['findomain']}")
    print(f"  Amass:        {stats['amass']}")
    print(f"{Y}{'─' * 46}{RST}")
    print(f"  Total Unique: {C}{stats['merged']}{RST}")
    print(f"  Total Assets: {G}{stats['alive']}{RST} (httpx)")
    print(f"  Total Time:   {B}{time_str}{RST} ⏱️")
    print(f"{G}{'─' * 46}{RST}\n")


if __name__ == "__main__":
    main()