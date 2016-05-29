from unicurses import *
import time

def kbhit():
    ch  = getch()
    if (ch != ERR):
        ungetch(ch)
        return 1
    else:
        return 0

stdscr = initscr()
cbreak()
noecho()
nodelay(stdscr, True)
scrollok(stdscr, True)
while (1):
    if kbhit():
        mvaddstr(0,0, str.format("Key pressed! It was: {0}\n", getch()))
        refresh()
        time.sleep(1)
    else:
        mvaddstr(0,0, "No key pressed yet...\n")
        refresh()

