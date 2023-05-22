import curses

CTRL = 1 << 25
ALT  = 1 << 27
MOVE = 1 << 28

LEFT_UP             = 1<<0
LEFT_DOWN           = 1<<1
LEFT_CLICK          = 1<<2
LEFT_DOUBLE         = 1<<3
LEFT_THREE          = 1<<4
MIDDLE_UP           = 1<<5
MIDDLE_DOWN         = 1<<6
MIDDLE_CLICK        = 1<<7
MIDDLE_DOUBLE       = 1<<8
MIDDLE_THREE        = 1<<9
RIGHT_UP            = 1<<10
RIGHT_DOWN          = 1<<11
RIGHT_CLICK         = 1<<12
RIGHT_DOUBLE        = 1<<13
RIGHT_THREE         = 1<<14
SCROLL_UP           = 1<<16
SCROLL_DOWN         = 1<<21

ESC = 27
ENTER = 10
BACKSPACE = 127
DOWN = 258
UP = 259
LEFT = 260
RIGHT = 261

PLUS = 42
ADD = 43
MINUS = 45
DIV = 47

A = 65
B = 66
C = 67
D = 68
E = 69
F = 70
G = 71
H = 72
I = 73
J = 74
K = 75
L = 76
M = 77
N = 78
O = 79
P = 80
Q = 81
R = 82
S = 83
T = 84
U = 85
V = 86
W = 87
X = 88
Y = 89
Z = 90

a = 97
b = 98
c = 99
d = 100
e = 101
f = 102
g = 103
h = 104
i = 105
j = 106
k = 107
l = 108
m = 109
n = 110
o = 111
p = 112
q = 113
r = 114
s = 115
t = 116
u = 117
v = 118
w = 119
x = 120
y = 121
z = 122

mouse_listeners = {}
key_listeners = {}
char_listeners = {}

def onchar(event, listener):
    if event not in char_listeners:
        char_listeners[event] = []
    char_listeners[event].append(listener)

def offchar(event, listener):
    char_listeners[event].remove(listener)

def onkey(event, listener):
    if CTRL|event:
        event = event&127 - 64
    if event not in key_listeners:
        key_listeners[event] = []
    key_listeners[event].append(listener)

def offkey(event, listener):
    key_listeners[event].remove(listener)

def onmouse(event, listener):
    if event not in mouse_listeners:
        mouse_listeners[event] = []
    mouse_listeners[event].append(listener)

def offmouse(event, listener):
    mouse_listeners[event].remove(listener)


screen = None
_listen = False
def _init():
    global screen
    screen = curses.initscr() 
    screen.keypad(True) 
    curses.noecho()
    curses.cbreak()
    curses.raw()
    return screen

def listen(screen=screen,button=curses.ALL_MOUSE_EVENTS,move=curses.REPORT_MOUSE_POSITION):
    if not screen:
        screen = _init()
    global _listen
    _listen = True
    curses.mousemask(button | move)
    if move:
        print('\033[?1003h')
    while _listen:
        wc = screen.get_wch()
        if wc == curses.KEY_MOUSE:
            _,y,x,_,key = curses.getmouse()
            if key in mouse_listeners:
                for listener in mouse_listeners[key]:
                    listener(y, x, key)
        else:
            key = ord(wc) if type(wc) == str else wc
            if key in key_listeners:
                for listener in key_listeners[key]:
                    listener(key)
        if (type(wc) == str) and (32 <= ord(wc)):
            if wc in char_listeners:
                for listener in char_listeners[wc]:
                    listener(wc)
            yield wc
    curses.mousemask(0)
    if move:
        print('\033[?1003l')

def stop():
    global _listen
    _listen = False