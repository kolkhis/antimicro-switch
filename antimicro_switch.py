from pywinauto.keyboard import send_keys
from pywinauto.application import Application
from pynput import keyboard
import sys

antimicro_path = r'C:\Program Files\AntiMicro\antimicro.exe'
stepmania_path = r"C:\Program Files\7-Zip\7zFM.exe"
am_app = Application(backend='uia')

print('Connecting to antimicro...')
am_app.connect(path=antimicro_path)
antimicro_window = am_app.window(title='antimicro')

print(f"Connection successful: {antimicro_window.exists()}")
if not antimicro_window.exists():
    print(f"Connection was not successful. Terminating script...")
    sys.exit()

# Stepmania
sm_app = Application(backend='uia')
sm_app.connect(path=stepmania_path)
print('Connecting to 7z...')
stepmania_window = sm_app.window(title='7-Zip')
print(f"Connection successful: {stepmania_window.exists()}")
if not stepmania_window.exists():
    print('Could not connect to 7z. Terminating script...')
    sys.exit()

# Game/Emulator
game_fp = input('Enter the game filepath: ')
if game_fp != '':
    window_name = input('Enter the game\'s window name: ')
    emu_app = Application(backend='uia')
    print(f'Connecting to {window_name}...')
    emu_app.connect(path=game_fp)
    game_window = emu_app.window()
    print(f"Connection successful: {game_window.exists()}")
    if not game_window.exists():
        print('Coult not connect. Terminating script...')
        sys.exit()


switch = { 0: '{UP}',
           1: '{DOWN}' }

key = switch[0]
def find_combo():
    global key
    if antimicro_window.exists() and stepmania_window.exists():
        antimicro_window.set_focus()
        antimicro_window.wait(wait_for='visible')
        send_keys(key)
        # window_switch_fns = {switch[0]: stepmania_window.set_focus,
        #                      switch[1]: game_window.set_focus }  # This will be game window
        # window_switch_fns[key]()
        stepmania_window.set_focus()
        key = switch[0] if key == '{DOWN}' else switch[1]
    else:
        print('Antimicro was either closed or restarted. Terminating script...')
        sys.exit()

def for_canonical(f):
    return lambda k: f(l.canonical(k))

# am_hotkey = keyboard.HotKey(keyboard.HotKey.parse('<shift>+='), find_combo)
# with keyboard.Listener(
#         on_press=for_canonical(am_hotkey.press),
#         on_release=for_canonical(am_hotkey.release)) as l:
#     l.join()

with keyboard.GlobalHotKeys({ '<shift>+=': find_combo, '<ctrl>+<shift>+c': sys.exit, }) as l:
    l.join()

