# -*- coding: utf-8 -*-
# Anime Hacker Bot v6.0 - Cybersecurity Learning Edition
# Developer: Arfa Ardiano Al-Fatih

import logging
import random
import json
import os
import sys
import time
import datetime
import traceback
import hashlib
import base64
import binascii
import socket
import ipaddress
import requests
import qrcode
import urllib.parse
import secrets
import string
from io import BytesIO
from telegram import Update
from telegram.ext import (
    Application, CommandHandler, MessageHandler,
    filters, ContextTypes
)

# ================== CONFIG ==================
BOT_VERSION = "6.0"
BOT_TOKEN = "8821339236:AAGLE7LiXiH_LiqYf9qqf_0o9pdyNkPkdYA"
ADMIN_ID = 8782970948
DATA_FILE = "users.json"
VIDEO_URL = "https://raw.githubusercontent.com/arfatih1107-netizen/Arfa-Gaza-Termux-V18/main/v1443ag5000cdaj751nog65m28cbuoh0.mp4"

DEVELOPER = "Arfa Ardiano Al-Fatih"
DEVELOPER_USERNAME = "@arfatih1107"
GITHUB_REPO = "https://github.com/arfatih1107-netizen/Arfa-Gaza-Termux-V18"

logging.basicConfig(
    format='%(asctime)s - %(levelname)s - %(message)s',
    level=logging.INFO
)

# ================== AUTO RESTART ==================
def restart_bot():
    print("\n[!] Bot crash! Restart dalam 5 detik...")
    time.sleep(5)
    os.execv(sys.executable, [sys.executable] + sys.argv)

def safe_reply(func):
    async def wrapper(update, ctx):
        try:
            await func(update, ctx)
        except Exception as e:
            logging.error(f"[{func.__name__}] {e}")
            try:
                await update.message.reply_text(f"Error: {str(e)[:150]}")
            except Exception:
                pass
    return wrapper

# ================== ANIME HACKER DATA ==================
HACKER_QUOTES = [
    "Hacking is not a crime, it's a skill. Yang jahat itu niatnya.",
    "The quieter you become, the more you are able to hear. - Kali Linux",
    "Security is not a product, but a process. - Bruce Schneier",
    "In cybersecurity, there are two types: those who have been hacked, and those who will be.",
    "Baka! Firewall itu bukan tembok, tapi filter!",
    "Ganbatte, white hat! Dunia butuh hacker baik!",
    "The best defense is a good offense. - Sun Tzu (modified)",
    "Keamanan bukan tujuan akhir, tapi perjalanan panjang."
]

CYBER_TIPS = [
    "Gunakan password minimal 12 karakter, kombinasi huruf, angka, simbol.",
    "Aktifkan 2FA (Two-Factor Authentication) di semua akun penting.",
    "Jangan klik link dari sumber tidak dikenal - itu phising!",
    "Update software rutin - banyak bug keamanan yang sudah di-patch.",
    "Gunakan password manager seperti Bitwarden atau KeePass.",
    "Backup data penting secara berkala (3-2-1 rule).",
    "Gunakan HTTPS - cek gembok di address bar browser.",
    "Jangan pakai WiFi publik tanpa VPN untuk data sensitif.",
    "Waspada social engineering - hacker sering pakai manipulasi.",
    "Encrypt data sensitif dengan VeraCrypt atau GPG."
]

CYBER_FACTS = [
    "Hacker pertama kali muncul tahun 1960-an di MIT.",
    "Term 'hacker' awalnya berarti programmer yang sangat mahir.",
    "Kali Linux punya lebih dari 600 tool hacking.",
    "Bug bounty terbesar pernah mencapai $2 juta (Google).",
    "Stuxnet adalah malware paling kompleks yang pernah dibuat.",
    "Zero-day adalah celah yang belum diketahui pembuat software.",
    "95% kebocoran data disebabkan human error.",
    "WannaCry menginfeksi 200.000+ komputer dalam sehari.",
    "Firewall pertama dikembangkan tahun 1980-an.",
    "HTTPS ditemukan tahun 1994 oleh Netscape."
]

ANIME_HACKER_JOKES = [
    "Kenapa hacker suka anime? Karena plot twist-nya unpredictable!",
    "Hacker: 'I'm in.' Anime protagonist: 'Sugoi!'",
    "Apa bedanya hacker dan ninja? Ninja pakai shuriken, hacker pakai terminal!",
    "Kenapa L dari Death Note bisa lacak Kira? Karena dia hacker level dewa!",
    "Hacker botak seperti Saitama? Ya, dia one-punch firewall!"
]

# ================== DATABASE ==================
def load_data():
    try:
        if os.path.exists(DATA_FILE):
            with open(DATA_FILE, 'r') as f:
                return json.load(f)
        return {}
    except Exception:
        return {}

def save_data(data):
    try:
        with open(DATA_FILE, 'w') as f:
            json.dump(data, f, indent=2)
    except Exception:
        pass

def get_user(uid):
    data = load_data()
    uid = str(uid)
    if uid not in data:
        data[uid] = {"coins": 0, "afk": None, "notes": {}, "joined": str(datetime.datetime.now())}
        save_data(data)
    return data[uid]

def update_user(uid, key, value):
    data = load_data()
    uid = str(uid)
    if uid not in data:
        data[uid] = {"coins": 0, "afk": None, "notes": {}, "joined": str(datetime.datetime.now())}
    data[uid][key] = value
    save_data(data)

# ================== VIDEO ==================
async def kirim_video(chat_id, ctx):
    try:
        r = requests.get(VIDEO_URL, timeout=90, stream=True)
        if r.status_code != 200:
            await ctx.bot.send_message(chat_id=chat_id, text="Video gagal dimuat.")
            return
        with open("temp_video.mp4", "wb") as f:
            for chunk in r.iter_content(chunk_size=8192):
                if chunk:
                    f.write(chunk)
        with open("temp_video.mp4", "rb") as f:
            await ctx.bot.send_video(
                chat_id=chat_id,
                video=f,
                caption=f"Anime Hacker Video\nDev: {DEVELOPER}",
                supports_streaming=True
            )
        if os.path.exists("temp_video.mp4"):
            os.remove("temp_video.mp4")
    except Exception as e:
        try:
            await ctx.bot.send_message(chat_id=chat_id, text=f"Error video: {str(e)[:100]}")
        except Exception:
            pass

# ================== FITUR UTAMA ==================

@safe_reply
async def start(update: Update, ctx: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user
    get_user(user.id)
    teks = (
        f"Halo {user.first_name}!\n\n"
        f"Anime Hacker Bot v{BOT_VERSION}\n"
        f"===================================\n"
        f"Cybersecurity Learning Edition\n"
        f"===================================\n"
        f"Belajar security, networking, & CTF\n"
        f"Ketik /help untuk daftar perintah\n"
        f"===================================\n"
        f"Dev: {DEVELOPER}\n"
        f"{DEVELOPER_USERNAME}\n"
        f"===================================\n"
        f"Ganbatte, white hat!"
    )
    await update.message.reply_text(teks)
    await kirim_video(update.effective_chat.id, ctx)

@safe_reply
async def help_cmd(update: Update, ctx: ContextTypes.DEFAULT_TYPE):
    text = (
        f"Anime Hacker Bot v{BOT_VERSION}\n"
        "===================================\n"
        "EDUKASI:\n"
        "1. /start - Mulai\n"
        "2. /help - Bantuan\n"
        "3. /cybertips - Tips keamanan\n"
        "4. /cyberfacts - Fakta hacker\n"
        "5. /hackerquote - Quote hacker\n"
        "6. /hackerjoke - Joke hacker\n"
        "\nTOOLS HASHING:\n"
        "7. /md5 [teks]\n"
        "8. /sha1 [teks]\n"
        "9. /sha256 [teks]\n"
        "10. /sha512 [teks]\n"
        "\nTOOLS ENCODING:\n"
        "11. /b64enc [teks] - Base64 encode\n"
        "12. /b64dec [teks] - Base64 decode\n"
        "13. /hexenc [teks] - Hex encode\n"
        "14. /hexdec [teks] - Hex decode\n"
        "15. /urlenc [teks] - URL encode\n"
        "16. /urldec [teks] - URL decode\n"
        "17. /binenc [teks] - Binary encode\n"
        "\nNETWORKING:\n"
        "18. /ipinfo [ip] - Info IP\n"
        "19. /myip - IP publik kamu\n"
        "20. /dns [domain] - DNS lookup\n"
        "21. /whois [domain] - Info domain\n"
        "22. /port [ip] [port] - Cek port\n"
        "23. /ping [host] - Ping host\n"
        "\nSECURITY TOOLS:\n"
        "24. /passcheck [password] - Cek kekuatan\n"
        "25. /passgen [panjang] - Generate password\n"
        "26. /uuid - Generate UUID\n"
        "27. /randomhex [panjang] - Random hex\n"
        "\nLIFE UTILITIES:\n"
        "28. /time - Waktu\n"
        "29. /date - Tanggal\n"
        "30. /id - ID Telegram\n"
        "31. /coin - Koin\n"
        "32. /daily - Klaim harian\n"
        "33. /slot - Slot\n"
        "34. /dadu - Dadu\n"
        "35. /random - Random\n"
        "36. /cuaca [kota]\n"
        "37. /qr [teks]\n"
        "38. /wiki [topik]\n"
        "39. /hitung [expr]\n"
        "40. /note\n"
        "41. /sticker\n"
        "42. /afk\n"
        "43. /poll\n"
        "44. /video - Kirim video\n"
        "45. /uptime - Uptime bot\n"
        "===================================\n"
        "Bonus: /dev, /github, /version\n"
        "Dev: " + DEVELOPER
    )
    await update.message.reply_text(text)

# ============ EDUKASI ============
@safe_reply
async def cybertips(update: Update, ctx: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(f"Cyber Tip:\n\n{random.choice(CYBER_TIPS)}")

@safe_reply
async def cyberfacts(update: Update, ctx: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(f"Cyber Fact:\n\n{random.choice(CYBER_FACTS)}")

@safe_reply
async def hackerquote(update: Update, ctx: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(f"\"{random.choice(HACKER_QUOTES)}\"")

@safe_reply
async def hackerjoke(update: Update, ctx: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(random.choice(ANIME_HACKER_JOKES))

# ============ HASHING ============
@safe_reply
async def md5_cmd(update: Update, ctx: ContextTypes.DEFAULT_TYPE):
    if not ctx.args:
        await update.message.reply_text("Usage: /md5 [teks]")
        return
    teks = " ".join(ctx.args)
    hasil = hashlib.md5(teks.encode()).hexdigest()
    await update.message.reply_text(f"MD5:\n{hasil}\n\nInput: {teks}")

@safe_reply
async def sha1_cmd(update: Update, ctx: ContextTypes.DEFAULT_TYPE):
    if not ctx.args:
        await update.message.reply_text("Usage: /sha1 [teks]")
        return
    teks = " ".join(ctx.args)
    hasil = hashlib.sha1(teks.encode()).hexdigest()
    await update.message.reply_text(f"SHA1:\n{hasil}\n\nInput: {teks}")

@safe_reply
async def sha256_cmd(update: Update, ctx: ContextTypes.DEFAULT_TYPE):
    if not ctx.args:
        await update.message.reply_text("Usage: /sha256 [teks]")
        return
    teks = " ".join(ctx.args)
    hasil = hashlib.sha256(teks.encode()).hexdigest()
    await update.message.reply_text(f"SHA256:\n{hasil}\n\nInput: {teks}")

@safe_reply
async def sha512_cmd(update: Update, ctx: ContextTypes.DEFAULT_TYPE):
    if not ctx.args:
        await update.message.reply_text("Usage: /sha512 [teks]")
        return
    teks = " ".join(ctx.args)
    hasil = hashlib.sha512(teks.encode()).hexdigest()
    await update.message.reply_text(f"SHA512:\n{hasil}\n\nInput: {teks}")

# ============ ENCODING ============
@safe_reply
async def b64enc(update: Update, ctx: ContextTypes.DEFAULT_TYPE):
    if not ctx.args:
        await update.message.reply_text("Usage: /b64enc [teks]")
        return
    teks = " ".join(ctx.args)
    hasil = base64.b64encode(teks.encode()).decode()
    await update.message.reply_text(f"Base64 Encode:\n{hasil}")

@safe_reply
async def b64dec(update: Update, ctx: ContextTypes.DEFAULT_TYPE):
    if not ctx.args:
        await update.message.reply_text("Usage: /b64dec [teks]")
        return
    teks = " ".join(ctx.args)
    hasil = base64.b64decode(teks.encode()).decode()
    await update.message.reply_text(f"Base64 Decode:\n{hasil}")

@safe_reply
async def hexenc(update: Update, ctx: ContextTypes.DEFAULT_TYPE):
    if not ctx.args:
        await update.message.reply_text("Usage: /hexenc [teks]")
        return
    teks = " ".join(ctx.args)
    hasil = binascii.hexlify(teks.encode()).decode()
    await update.message.reply_text(f"Hex Encode:\n{hasil}")

@safe_reply
async def hexdec(update: Update, ctx: ContextTypes.DEFAULT_TYPE):
    if not ctx.args:
        await update.message.reply_text("Usage: /hexdec [hex]")
        return
    teks = " ".join(ctx.args)
    hasil = binascii.unhexlify(teks.encode()).decode()
    await update.message.reply_text(f"Hex Decode:\n{hasil}")

@safe_reply
async def urlenc(update: Update, ctx: ContextTypes.DEFAULT_TYPE):
    if not ctx.args:
        await update.message.reply_text("Usage: /urlenc [teks]")
        return
    teks = " ".join(ctx.args)
    hasil = urllib.parse.quote(teks)
    await update.message.reply_text(f"URL Encode:\n{hasil}")

@safe_reply
async def urldec(update: Update, ctx: ContextTypes.DEFAULT_TYPE):
    if not ctx.args:
        await update.message.reply_text("Usage: /urldec [teks]")
        return
    teks = " ".join(ctx.args)
    hasil = urllib.parse.unquote(teks)
    await update.message.reply_text(f"URL Decode:\n{hasil}")

@safe_reply
async def binenc(update: Update, ctx: ContextTypes.DEFAULT_TYPE):
    if not ctx.args:
        await update.message.reply_text("Usage: /binenc [teks]")
        return
    teks = " ".join(ctx.args)
    hasil = " ".join(format(ord(c), '08b') for c in teks)
    await update.message.reply_text(f"Binary:\n{hasil}")

# ============ NETWORKING ============
@safe_reply
async def ipinfo(update: Update, ctx: ContextTypes.DEFAULT_TYPE):
    if not ctx.args:
        await update.message.reply_text("Usage: /ipinfo [ip]")
        return
    ip = ctx.args[0]
    r = requests.get(f"http://ip-api.com/json/{ip}", timeout=15).json()
    if r.get('status') == 'success':
        await update.message.reply_text(
            f"IP Info\n"
            f"IP: {r['query']}\n"
            f"Negara: {r['country']}\n"
            f"Kota: {r['city']}\n"
            f"ISP: {r['isp']}\n"
            f"Zona: {r['timezone']}\n"
            f"Lat/Lon: {r['lat']}, {r['lon']}"
        )
    else:
        await update.message.reply_text("IP tidak valid.")

@safe_reply
async def myip(update: Update, ctx: ContextTypes.DEFAULT_TYPE):
    r = requests.get("https://api.ipify.org?format=json", timeout=15).json()
    await update.message.reply_text(f"IP Publik kamu:\n{r['ip']}")

@safe_reply
async def dns_cmd(update: Update, ctx: ContextTypes.DEFAULT_TYPE):
    if not ctx.args:
        await update.message.reply_text("Usage: /dns [domain]")
        return
    domain = ctx.args[0]
    ip = socket.gethostbyname(domain)
    await update.message.reply_text(f"DNS Lookup\nDomain: {domain}\nIP: {ip}")

@safe_reply
async def whois_cmd(update: Update, ctx: ContextTypes.DEFAULT_TYPE):
    if not ctx.args:
        await update.message.reply_text("Usage: /whois [domain]")
        return
    domain = ctx.args[0]
    try:
        r = requests.get(f"https://api.hackertarget.com/whois/?q={domain}", timeout=15)
        hasil = r.text[:1500]
        await update.message.reply_text(f"WHOIS {domain}:\n\n{hasil}")
    except Exception:
        await update.message.reply_text("Gagal mengambil WHOIS.")

@safe_reply
async def port_cmd(update: Update, ctx: ContextTypes.DEFAULT_TYPE):
    if len(ctx.args) < 2:
        await update.message.reply_text("Usage: /port [ip] [port]\nContoh: /port 1.1.1.1 80")
        return
    try:
        ip = ctx.args[0]
        port = int(ctx.args[1])
    except Exception:
        await update.message.reply_text("IP/port tidak valid.")
        return
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.settimeout(3)
    result = s.connect_ex((ip, port))
    s.close()
    if result == 0:
        await update.message.reply_text(f"Port {port} di {ip}: TERBUKA")
    else:
        await update.message.reply_text(f"Port {port} di {ip}: TERTUTUP/FILTERED")

@safe_reply
async def ping_host(update: Update, ctx: ContextTypes.DEFAULT_TYPE):
    if not ctx.args:
        await update.message.reply_text("Usage: /ping [host]")
        return
    host = ctx.args[0]
    try:
        start = time.time()
        ip = socket.gethostbyname(host)
        elapsed = round((time.time() - start) * 1000, 2)
        await update.message.reply_text(f"Ping {host}\nIP: {ip}\nRespon: {elapsed}ms (DNS only)")
    except Exception:
        await update.message.reply_text(f"Host {host} tidak ditemukan.")

# ============ SECURITY TOOLS ============
@safe_reply
async def passcheck(update: Update, ctx: ContextTypes.DEFAULT_TYPE):
    if not ctx.args:
        await update.message.reply_text("Usage: /passcheck [password]")
        return
    pwd = " ".join(ctx.args)
    score = 0
    feedback = []
    if len(pwd) >= 8: score += 20
    if len(pwd) >= 12: score += 20
    if len(pwd) >= 16: score += 10
    if any(c.islower() for c in pwd): score += 10
    if any(c.isupper() for c in pwd): score += 10
    if any(c.isdigit() for c in pwd): score += 10
    if any(c in "!@#$%^&*()_+-=[]{}|;:,.<>?" for c in pwd): score += 20
    
    if score >= 80:
        level = "SANGAT KUAT"
    elif score >= 60:
        level = "KUAT"
    elif score >= 40:
        level = "SEDANG"
    elif score >= 20:
        level = "LEMAH"
    else:
        level = "SANGAT LEMAH"
    
    if len(pwd) < 12: feedback.append("- Perpanjang minimal 12 karakter")
    if not any(c.isupper() for c in pwd): feedback.append("- Tambah huruf besar")
    if not any(c.isdigit() for c in pwd): feedback.append("- Tambah angka")
    if not any(c in "!@#$%^&*()_+-=[]{}|;:,.<>?" for c in pwd): feedback.append("- Tambah simbol")
    
    saran = "\n".join(feedback) if feedback else "- Password sudah bagus!"
    
    await update.message.reply_text(
        f"Password Strength\n"
        f"===================================\n"
        f"Skor: {score}/100\n"
        f"Level: {level}\n"
        f"Panjang: {len(pwd)} karakter\n"
        f"===================================\n"
        f"Saran:\n{saran}"
    )

@safe_reply
async def passgen(update: Update, ctx: ContextTypes.DEFAULT_TYPE):
    length = 16
    if ctx.args:
        try:
            length = int(ctx.args[0])
        except Exception:
            pass
    length = min(max(length, 4), 128)
    chars = string.ascii_letters + string.digits + "!@#$%^&*()_+-="
    pwd = ''.join(secrets.choice(chars) for _ in range(length))
    await update.message.reply_text(
        f"Password Generated\n"
        f"Panjang: {length}\n"
        f"===================================\n"
        f"{pwd}\n"
        f"===================================\n"
        f"Simpan di tempat aman!"
    )

@safe_reply
async def uuid_cmd(update: Update, ctx: ContextTypes.DEFAULT_TYPE):
    import uuid
    await update.message.reply_text(f"UUID:\n{uuid.uuid4()}")

@safe_reply
async def randomhex(update: Update, ctx: ContextTypes.DEFAULT_TYPE):
    length = 16
    if ctx.args:
        try:
            length = int(ctx.args[0])
        except Exception:
            pass
    length = min(max(length, 1), 256)
    hexs = ''.join(secrets.choice("0123456789abcdef") for _ in range(length))
    await update.message.reply_text(f"Random Hex ({length}):\n{hexs}")

# ============ LIFE UTILITIES ============
@safe_reply
async def ping(update: Update, ctx: ContextTypes.DEFAULT_TYPE):
    start_t = time.time()
    msg = await update.message.reply_text("Pinging...")
    end_t = time.time()
    await msg.edit_text(f"Pong! {round((end_t-start_t)*1000)}ms")

@safe_reply
async def info(update: Update, ctx: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user
    u = get_user(user.id)
    await update.message.reply_text(
        f"Profile\nNama: {user.first_name}\nUsername: @{user.username or '-'}\nID: {user.id}\nKoin: {u['coins']}"
    )

@safe_reply
async def time_cmd(update: Update, ctx: ContextTypes.DEFAULT_TYPE):
    now = datetime.datetime.now()
    await update.message.reply_text(f"Jikan: {now.strftime('%H:%M:%S')}")

@safe_reply
async def date_cmd(update: Update, ctx: ContextTypes.DEFAULT_TYPE):
    now = datetime.datetime.now()
    hari = ['Senin','Selasa','Rabu','Kamis','Jumat','Sabtu','Minggu']
    await update.message.reply_text(f"{hari[now.weekday()]}, {now.strftime('%d %B %Y')}")

@safe_reply
async def id_cmd(update: Update, ctx: ContextTypes.DEFAULT_TYPE):
    await update.message.re
