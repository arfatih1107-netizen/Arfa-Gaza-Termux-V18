clear
# ==========================================================
# DEVELOPER : Arfa ardiano Al Fatih
# PROJECT   : CH Indonesia Cool Premium v18.9.0
# MASKOT    : Countryhumans Indonesia (Peci & Smirk Style)
# IDENTITY  : ARFA STORE OFFICIAL
# STATUS    : ANTI-DELAY / ACTIVE
# ==========================================================

# 1. SYSTEM ENGINE
USER_ID="ARFA_IND_USER"
DEVICE=$(getprop ro.product.model)
JAM=$(date +"%H:%M:%S")
HARI=$(date +"%A, %d %B %Y")
MEM_FREE=$(free -m | awk '/Mem:/ {print $4"MB"}')

# 2. LOGO ASCII MASKOT COUNTRYHUMANS INDONESIA SAMA SEPERTI FOTO
echo -e "                 \e[1;30m.----------.\e[0m"
echo -e "                 \e[1;30m|   PECI   |\e[0m"
echo -e "                 \e[1;30m'----------'\e[0m"
echo -e "                 \e[1;31m.---''---.\e[0m"
echo -e "                \e[1;31m/   \\    /   \\\e[0m"
echo -e "              \e[1;31m((     \e[1;37mO  O \e[1;31m    ))\e[0m"
echo -e "               \e[1;37m\\    --^--    /\e[0m"
echo -e "              \e[1;37m/ \\   \\___/   / \\\e[0m"
echo -e "             \e[1;31m/   \e[1;37m'---------'   \e[1;31m\\\e[0m"
echo -e "            \e[1;31m/  /|  \e[1;30m[__]\e[1;31m  |\\  \\\e[0m"
echo -e "           \e[1;30m|  | |  \e[1;31mJAKET\e[1;30m | |  |\e[0m"
echo -e "           \e[1;30m|__| |________| |__|\e[0m"
echo -e "         \e[1;31m[ \e[1;37mCH INDONESIA PREMIUM \e[1;31m]\e[0m"

# 3. DASHBOARD CREDIT INFO
echo -e "\e[1;31m┌────────────────────────────────────────────────────────┐\e[0m"
echo -e "\e[1;31m│\e[1;37m [ • ] OPERATOR   : Arfa ardiano Al Fatih           \e[1;31m│\e[0m"
echo -e "\e[1;31m│\e[1;37m [ • ] MASKOT     : CH Indonesia Peci Version       \e[1;31m│\e[0m"
echo -e "\e[1;31m│\e[1;37m [ • ] DEVICE     : $DEVICE / $MEM_FREE            \e[1;31m│\e[0m"
echo -e "\e[1;31m│\e[1;37m [ • ] LOGIN TIME : $JAM | $HARI        \e[1;31m│\e[0m"
echo -e "\e[1;31m└────────────────────────────────────────────────────────┘\e[0m"

# 4. VERIFIKASI SISTEM
echo -ne "\e[1;31mMENYAMBUNGKAN KE INTERFACE [ \e[1;37m"
for i in {1..20}; do echo -ne "■"; sleep 0.01; done
echo -e " \e[1;31m] \e[1;32mSUKSES\e[0m"
echo -e "\e[1;37mAKSES DIIZINKAN : \e[1;32mCH-INDONESIA - $USER_ID\e[0m"
echo -e "\e[1;31m━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━\e[0m"

# 5. BIG BANNER INDONESIA
if command -v figlet &> /dev/null && command -v lolcat &> /dev/null; then
    figlet -f slant "INDONESIA" | lolcat
else
    echo -e "\e[1;31m             [ COUNTRYHUMANS INDONESIA v18.9.0 ]\e[0m"
fi
echo -e "\e[1;31m━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━\e[0m"

# 6. ALIAS PERINTAH
alias cls="clear"
alias menu="echo -e \"\n\e[1;31m  [[ ARFA INDO MENU ]]\n\e[1;37m  [01] Nmap Scan   [02] DDoS Attack   [03] Metasploit\n  [00] Logout\" | lolcat"

# 7. PROMPT TERMINAL
export PS1="\n\e[1;31m┌──[\e[1;37mArfa\e[1;31m@\e[1;37mCH-Indo\e[1;31m]─[\e[1;37mv18.9.0\e[1;31m]\n└──╼ \e[1;31m# \e[0m"
