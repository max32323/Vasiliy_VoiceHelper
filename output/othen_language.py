import win32api
import win32gui
import ctypes

import voice


# #Переключение раскладки клавиатуры
# #---------------------------------------------------------



def setCyrillicLayout():
    window_handle = win32gui.GetForegroundWindow()
    result = win32api.SendMessage(window_handle, 0x0050, 0, 0x04190419)

def setEngLayout():
    window_handle = win32gui.GetForegroundWindow()
    result = win32api.SendMessage(window_handle, 0x0050, 0, 0x04090409)

def get_layout():
    u = ctypes.windll.LoadLibrary("user32.dll")
    pf = getattr(u, "GetKeyboardLayout")
    if hex(pf(0)) == '0x4190419':
        return 'ru'
    if hex(pf(0)) == '0x4090409':
        return 'en'


l = get_layout()
if l == 'en':
    setCyrillicLayout()
elif l == 'ru':
    setEngLayout()
voice.speaker('Изык был изменён')