from pywinauto import ElementNotFoundError, WindowNotFoundError
from pywinauto.keyboard import send_keys
from pywinauto.application import Application
from pynput import keyboard
import sys

description = """
            This is an automation script for a streamer friend, iFlipsy. 
            He plays games with a DDR pad and uses AntiMicro to map his controls.
            His channel point redemptions include DDR song redemptions, which require him to change his controller mapping.
            The script will bind a single hotkey for him to tab over to AntiMicro,
            change his controller mapping, and tab to the right game.
            """

def get_antimicro_window():
    """Connect to antimicro window, and return it."""
    print('Connecting to antimicro...')
    am_app.connect(path=antimicro_path)
    antimicro_window = am_app.window(title_re='[.]*?antimicro[.]*?')
    print(f"Connection successful: {antimicro_window.exists()}")
    if not antimicro_window.exists():
        print(f"Connection was not successful. Terminating script...")
        sys.exit()
    return antimicro_window


def get_stepmania_window():
    """Connect to stepmania window, and return it."""
    print('Connecting to StepMania...')
    sm_app.connect(path=stepmania_path)
    stepmania_window = sm_app.window(title_re=r'[.]*?StepMania[.]*?')
    print(f"Connection successful: {stepmania_window.exists()}")
    if not stepmania_window.exists():
        print('Could not connect to StepMania. Terminating script...')
        sys.exit()
    return stepmania_window


def get_game_window():
    """Connect to Game/Emulator window, and return it."""
    global game_path
    print(f'Connecting to game...')
    game_app.connect(path=game_path)
    game_window = game_app.window()
    print(f"Connection to game successful: {game_window.exists()}")
    if not game_window.exists():
        print('Could not connect. Terminating script...')
        sys.exit()
    return game_window


def reconnect_all_windows():
    """Attempt to reconnect to all windows, save them in their respective variables in the global namespace"""
    global antimicro_window
    global stepmania_window
    global game_window
    print('A window was either closed or restarted. Attempting to reconnect...')
    antimicro_window = get_antimicro_window()
    stepmania_window = get_stepmania_window()
    stepmania_window = get_stepmania_window()
    all_windows_exist = stepmania_window.exists() and antimicro_window.exists() and game_window.exists()
    if not all_windows_exist:
        print('One or more windows could not be re-connected to. Terminating script...')
        sys.exit()


def find_combo():
    """On Detect hotkey: <shift>+=, swap to AM and switch profiles, swap to corresponding game."""
    global key
    global antimicro_window
    global stepmania_window
    global game_window
    try:
        if stepmania_window.is_active():  # 7z rn
            key = switch[1]  # Down to stepmania layout
        elif game_window.is_active():
            key = switch[0]  # Up to game layout
        if antimicro_window.exists():
            antimicro_window.set_focus()
            antimicro_window.wait(wait_for='visible active ready')
            send_keys(key)
            focus_fns[key]()
            key = switch[0] if key == '{DOWN}' else switch[1]
    except ElementNotFoundError:
        reconnect_all_windows()
    except WindowNotFoundError:
        reconnect_all_windows()


def for_canonical(f):
    """Wrapper function for detecting defined hotkey (<Shift>+=)."""
    return lambda k: f(l.canonical(k))


emu_list = [r"C:\Program Files (x86)\Project64 3.0\Project64.exe",
            r"C:\Users\Flipsy\Documents\Various Games\Systems\NES\Mesen.0.9.9\Mesen.exe",
            r"C:\Program Files (x86)\PCSX2\pcsx2.exe", 
            r"C:\Users\Flipsy\Documents\Various Games\Systems\SNES\zsnesw151\zsnesw.exe",
            r"C:\Users\Flipsy\Documents\Various Games\Systems\duckstation-windows-x64-release\duckstation-qt-x64-ReleaseLTCG.exe"]

emu_nu = input('Which emulator are you using?\n' \
               '1. Project64\n' \
               '2. Mesen\n' \
               '3. PCSX2\n' \
               '4. ZSNES\n' \
               '5. DuckStation\n> ')

while emu_nu not in ['1', '2', '3', '4', '5', 'q']:
    print('Invalid input. Select 1-5.')
    emu_nu = input('Which emulator are you using?\n' \
                   '1. Project64\n' \
                   '2. Mesen\n' \
                   '3. PCSX2\n' \
                   '4. ZSNES\n' \
                   '5. DuckStation\n> ')

if emu_nu == 'q':
    print('Quitting application...')
    sys.exit()

game_path = emu_list[int(emu_nu) - 1]
antimicro_path = r'C:\Program Files\AntiMicro\antimicro.exe'
stepmania_path = r"C:\Games\StepMania\Program\StepMania.exe"

am_app = Application(backend='uia')
game_app = Application(backend='uia')
sm_app = Application(backend='uia')

antimicro_window = get_antimicro_window()
stepmania_window = get_stepmania_window()
game_window = get_game_window()

key: str
switch = { 0: '{UP}',
           1: '{DOWN}' }
focus_fns = {'{UP}': game_window.set_focus,
             '{DOWN}': stepmania_window.set_focus }

am_hotkey = keyboard.HotKey(keyboard.HotKey.parse('<shift>+='), find_combo)
with keyboard.Listener(
        on_press=for_canonical(am_hotkey.press),
        on_release=for_canonical(am_hotkey.release)) as l:
    l.join()

