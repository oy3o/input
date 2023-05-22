# Input Event

Support input and key detection, Cases or input characters can be subscribed to through events, the following types are supported.

- ASCII Input Event
- UTF-8 Input Event
- Mouse Click Event
- Mouse Move Event
- CTRL+Alpha Event

## listen key or mouse press
combine `input.CTRL` + Upper Alpha can be access. ASCII char such as `input.A` is ASCII of `A`.
```py
import oy3opy.input as input

input.onkey(input.CTRL + input.A, lambda _:print('CTRL + A'))

input.onkey(input.DOWN, lambda _:print('ARROW DOWN'))
input.onkey(input.UP, lambda _:print('ARROW UP'))
input.onkey(input.LEFT, lambda _:print('ARROW LEFT'))
input.onkey(input.RIGHT, lambda _:print('ARROW RIGHT'))

input.onkey(input.ENTER, lambda _:print('ENTER'))
input.onkey(input.BACKSPACE, lambda _:print('BACKSPACE'))

input.onmouse(input.SCROLL_DOWN, lambda *_:print('SCROLL DOWN'))
input.onmouse(input.SCROLL_UP, lambda *_:print('SCROLL UP'))

for wc in input.listen(move=0):
    if wc == 'q':
        input.stop()
    print(wc)
```

## listen mouse move
`input.ALT` is mouse only, because `ALT + Key` always is system shortcut.
```py
import oy3opy.input as input
import curses

screen = curses.initscr() 
screen.keypad(True) 
curses.noecho()
curses.cbreak()
curses.raw()

def pos(y,x,type):
    screen.addstr(0, 0, f'({y},{x})')
    screen.clrtoeol()
    screen.refresh()

input.onmouse(input.MOVE, pos)
input.onmouse(input.CTRL + input.ALT + input.MOVE, pos)

for wc in input.listen(screen):
    if wc == 'q':
        input.stop()
```