import asyncio
import aiohttp
import json
import os
import sys
import time
import random
from collections import Counter


RED = "\033[1;31m"
WHITE = "\033[1;37m"
CYAN = "\033[1;36m"
GREEN = "\033[1;32m"
BOLD = "\033[1m"
RESET = "\033[0m"
GREY = "\033[90m"

USER_AGENTS = [
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Safari/537.36",
    "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36"
]

class GhostOverlord:
    def __init__(self):
        self.db_path = "data.json" 
        self.found_details = []

    def banner(self):
        os.system('cls' if os.name == 'nt' else 'clear')
        print(f"""{RED}
  ██████╗ ██╗  ██╗ ██████╗ ███████╗████████╗     ██████╗ ███████╗██╗███╗   ██╗████████╗
 ██╔════╝ ██║  ██║██╔═══██╗██╔════╝╚══██╔══╝    ██╔═══██╗██╔════╝██║████╗  ██║╚══██╔══╝
 ██║  ███╗███████║██║   ██║███████╗   ██║       ██║   ██║███████╗██║██╔██╗ ██║   ██║   
 ██║   ██║██╔══██║██║   ██║╚════██║   ██║       ██║   ██║╚════██║██║██║╚██╗██║   ██║   
 ╚██████╔╝██║  ██║╚██████╔╝███████║   ██║       ╚██████╔╝███████║██║██║ ╚████║   ██║   
  ╚═════╝ ╚═╝  ╚═╝ ╚═════╝ ╚══════╝   ╚═╝        ╚═════╝ ╚══════╝╚═╝╚═╝  ╚═══╝   ╚═╝

{WHITE}        ---------------------- MULTI-TOOLS TRACKING & MONITORING --------------------
{GREY}            Tools By Ghost{RESET}
""")
        print(f"{RED}[ STATUS ]{RESET} {WHITE}Active DB: {CYAN}{self.db_path}{RESET}")
        print(f"{RED}[01]{RESET} {WHITE}Deep Scan  (Dengan Variasi/Mutasi Nama){RESET}")
        print(f"{RED}[02]{RESET} {WHITE}Quick Scan (Hanya Nama Inti / Tanpa Variasi){RESET}")
        print(f"{RED}[03]{RESET} {WHITE}Ganti Database JSON{RESET}")
        print(f"{RED}[04]{RESET} {WHITE}Keluar (Exit Sesi Overlord){RESET}")
        print(f"{RED}{'='*85}{RESET}")

    def generate_aggressive_mutations(self, username):
        base = username.lower().replace(" ", "")
        mutations = [
            base, 
            f"{base}_official", f"{base}.official", f"{base}official",
            f"{base}_offi", f"{base}5151", f"{base}_real", f"iam{base}", f"{base}_"
        ]
        return list(set(mutations))

    async def check_target(self, session, site_name, url_template, username):
        target_url = url_template.format(username)
        headers = {
            "User-Agent": random.choice(USER_AGENTS),
            "Referer": "https://www.google.com/"
        }
        
        try:
            async with session.get(target_url, headers=headers, timeout=12, ssl=False, allow_redirects=False) as response:
                if response.status == 200:
                    content = await response.text()
                    # Validasi konten nyata agar tidak false positive
                    if len(content) > 750: 
                        print(f"{RED}[DETEKSI]{RESET} {WHITE}{site_name:<15}{RESET} : {CYAN}{target_url}{RESET}")
                        self.found_details.append({"site": site_name, "user": username, "url": target_url})
                        return True
        except:
            pass
        return False

    async def run_scan(self, target, use_mutations=True):
        self.found_details = []
        if not os.path.exists(self.db_path):
            print(f"\n{RED}[!] ERROR: Database '{self.db_path}' tidak ditemukan!{RESET}")
            input("\nTekan Enter..."); return

        with open(self.db_path, "r", encoding="utf-8") as f:
            raw_data = json.load(f)
            db = {k: v["url"] for k, v in raw_data.items() if isinstance(v, dict) and "url" in v}

        # Seleksi Mode
        if use_mutations:
            targets = self.generate_aggressive_mutations(target)
            mode_text = "MODE DEEP SCAN (AGRESIF)"
        else:
            targets = [target]
            mode_text = "MODE QUICK SCAN (INTI)"
        
        print(f"\n{RED}[*]{RESET} Mengunci Target : {WHITE}{target}{RESET}")
        print(f"{RED}[*]{RESET} Mode           : {CYAN}{mode_text}{RESET}")
        print(f"{RED}[*]{RESET} Total Jalur    : {len(targets) * len(db)} Requests{RESET}\n")
        print(f"{RED}{'='*95}{RESET}")
        
        async with aiohttp.ClientSession() as session:
            tasks = [self.check_target(session, s, u, t) for t in targets for s, u in db.items()]
            await asyncio.gather(*tasks)

        # --- FINAL REPORT ---
        print(f"\n{RED}{'='*95}{RESET}")
        print(f"{WHITE}{BOLD}ANALISIS JEJAK DIGITAL BERHASIL DIKUNCI (ACTIVE LINKS):{RESET}")
        if self.found_details:
            sites_found = sorted(list(set(item['site'] for item in self.found_details)))
            for site in sites_found:
                site_results = [i for i in self.found_details if i['site'] == site]
                print(f"{GREEN}✔{RESET} {WHITE}{site:<15}: {RED}{len(site_results)} Identitas Valid{RESET}")
                for res in site_results:
                    print(f"   {GREY}└─> ID: {res['user']:<20} {CYAN}Link: {res['url']}{RESET}")
            
            print(f"\n{GREEN}[+]{RESET} {WHITE}Total: {len(self.found_details)} jejak digital berhasil dikunci.{RESET}")
        else:
            print(f"{RED}[!] Tidak ada jejak valid yang ditemukan dalam database ini.{RESET}")
        
        print(f"{RED}{'='*95}{RESET}")
        input(f"\n{RED}>>{RESET} Tekan Enter untuk kembali...")

    def switch_db(self):
        files = [f for f in os.listdir('.') if f.endswith('.json')]
        if not files:
            print(f"\n{RED}[!] Tidak ada database JSON di folder ini.{RESET}")
            time.sleep(2); return

        print(f"\n{RED}[+]{RESET} {WHITE}Pilih Database Baru:{RESET}")
        for i, f in enumerate(files, 1):
            print(f"   {RED}[{i}]{RESET} {WHITE}{f}{RESET}")
        
        try:
            choice = int(input(f"\n{RED}GHOST-EYE >> Pilih Nomor: {RESET}"))
            self.db_path = files[choice-1]
            print(f"{GREEN}[OK] Database dialihkan ke: {self.db_path}{RESET}")
        except:
            print(f"{RED}[!] Input tidak valid.{RESET}")
        time.sleep(1.5)

    def main_loop(self):
        while True:
            self.banner()
            cmd = input(f"{RED}GHOST-EYE@OVERLORD:~# {RESET}").strip()
            
            if cmd in ["1", "01"]:
                target = input(f"{WHITE}Masukkan Nama Dasar (Deep Scan) >> {RESET}").strip()
                if target: asyncio.run(self.run_scan(target, use_mutations=True))
            elif cmd in ["2", "02"]:
                target = input(f"{WHITE}Masukkan Nama Inti (Quick Scan) >> {RESET}").strip()
                if target: asyncio.run(self.run_scan(target, use_mutations=False))
            elif cmd in ["3", "03"]:
                self.switch_db()
            elif cmd in ["4", "04"]:
                print(f"{RED}[!] Mengakhiri Sesi Overlord...{RESET}")
                time.sleep(1)
                sys.exit()

if __name__ == "__main__":
    try:
        GhostOverlord().main_loop()
    except KeyboardInterrupt:
        sys.exit()
