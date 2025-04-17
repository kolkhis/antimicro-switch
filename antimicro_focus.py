from pywinauto.application import Application
from pynput import keyboard
import sys

exe_path = r'C:\Program Files\AntiMicro\antimicro.exe'
app = Application(backend='uia')

print('Connecting to antimicro...')
app.connect(path=exe_path)
main_window = app.window(title='antimicro')

print(f"Connection successful: {main_window.exists()}")
if not main_window.exists():
    print(f"Connection was not successful. Terminating script...")
    sys.exit()

def find_combo():
    if main_window.exists():
        main_window.set_focus()
    else:
        print('Antimicro was either closed or restarted. Terminating script...')
        sys.exit()

def for_canonical(f):
    return lambda k: f(l.canonical(k))

am_hotkey = keyboard.HotKey(keyboard.HotKey.parse('<shift>+='), find_combo)
with keyboard.Listener(
        on_press=for_canonical(am_hotkey.press),
        on_release=for_canonical(am_hotkey.release)) as l:
    l.join()

# with keyboard.GlobalHotKeys({ '<shift>+=': find_combo, '<ctrl>+<shift>+c': sys.exit, }) as l:
#     l.join()

