
import ctypes
import time

SendInput = ctypes.windll.user32.SendInput

space_pressed=0x39
r_pressed = 0x13
t_pressed = 0x14
a_pressed = 0x1E
d_pressed = 0x20
w_pressed = 0x11

# C struct redefinitions 
PUL = ctypes.POINTER(ctypes.c_ulong)
class KeyBdInput(ctypes.Structure):
    _fields_ = [("wVk", ctypes.c_ushort),
                ("wScan", ctypes.c_ushort),
                ("dwFlags", ctypes.c_ulong),
                ("time", ctypes.c_ulong),
                ("dwExtraInfo", PUL)]

class HardwareInput(ctypes.Structure):
    _fields_ = [("uMsg", ctypes.c_ulong),
                ("wParamL", ctypes.c_short),
                ("wParamH", ctypes.c_ushort)]

class MouseInput(ctypes.Structure):
    _fields_ = [("dx", ctypes.c_long),
                ("dy", ctypes.c_long),
                ("mouseData", ctypes.c_ulong),
                ("dwFlags", ctypes.c_ulong),
                ("time",ctypes.c_ulong),
                ("dwExtraInfo", PUL)]

class Input_I(ctypes.Union):
    _fields_ = [("ki", KeyBdInput),
                 ("mi", MouseInput),
                 ("hi", HardwareInput)]

class Input(ctypes.Structure):
    _fields_ = [("type", ctypes.c_ulong),
                ("ii", Input_I)]

# Actuals Functions

def PressKey(hexKeyCode):
    extra = ctypes.c_ulong(0)
    ii_ = Input_I()
    ii_.ki = KeyBdInput( 0, hexKeyCode, 0x0008, 0, ctypes.pointer(extra) )
    x = Input( ctypes.c_ulong(1), ii_ )
    ctypes.windll.user32.SendInput(1, ctypes.pointer(x), ctypes.sizeof(x))

def ReleaseKey(hexKeyCode):
    extra = ctypes.c_ulong(0)
    ii_ = Input_I()
    ii_.ki = KeyBdInput( 0, hexKeyCode, 0x0008 | 0x0002, 0, ctypes.pointer(extra) )
    x = Input( ctypes.c_ulong(1), ii_ )
    ctypes.windll.user32.SendInput(1, ctypes.pointer(x), ctypes.sizeof(x))

if __name__ == '__main__':
    PressKey(0x39)
    time.sleep(1)
    ReleaseKey(0x39)
    time.sleep(1)
    
    # R Button
    PressKey(0x13)
    time.sleep(1)
    ReleaseKey(0x13)
    time.sleep(1)
    
    # T Button
    time.sleep(1)
    PressKey(0x14)
    time.sleep(1)
    ReleaseKey(0x14)
    time.sleep(1)
    
    # A Button
    time.sleep(1)
    PressKey(0x1E)
    time.sleep(1)
    ReleaseKey(0x1E)
    time.sleep(1)
    
    # D Button
    time.sleep(1)
    PressKey(0x20)
    time.sleep(1)
    ReleaseKey(0x20)
    time.sleep(1)
    
    time.sleep(1)
    PressKey(0x11)
    time.sleep(1)
    ReleaseKey(0x11)
    time.sleep(1)
    
    