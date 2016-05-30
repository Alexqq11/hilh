from unicurses import *
import copy
#stdscr = initscr()

class MainMenu:
    def __init__(self, width, height):
        self.enabled = True
        self.y = 20 #((getmaxyx(stdscr)[0] + 1) // 2) + height
        self.x = 20 #((getmaxyx(stdscr)[1] + 1)// 2) + width
        self.width = width
        self.height = height
        self.menu_window = newwin(height, width, self.y, self.x)
        self.topics = ["NEW GAME","RESUME GAME","LOAD GAME","SAVE GAME","SETTINGS","EXIT"]
        self.topics_pointer = 0
        self.locked_topics = [3]
        self.to_stay_lock = []
        self.panel = new_panel(self.menu_window)
        update_panels()
        doupdate()

    def _scroll(self,key):
        if key == ord('w') or key == KEY_UP:
            self.topics_pointer -= 1
            while(self.topics_pointer  in self.locked_topics):
                self.topics_pointer -= 1
        elif key == ord('s') or key == KEY_DOWN:
            self.topics_pointer += 1
            while(self.topics_pointer  in self.locked_topics):
                self.topics_pointer += 1
        self.topics_pointer %= len(self.topics)

    def _selected(self):
        if key == 10:
            if self.topics_pointer == 5:
                exit()

    def key_event(self, key):
        if self.enabled:
            if key == ord('w') or key == ord('s') or key == KEY_UP or key == KEY_DOWN:
                self._scroll(key)
            elif key == 10:
                self._selected()

    def disable(self):
        if self.enabled:
            self.to_stay_lock  = copy.copy(self.locked_topics)
            self.locked_topics = list(range(0, len(self.topics)))
            self.enabled = False
            hide_panel(self.panel)

    def enable(self):
        if not self.enabled:
            self.locked_topics = copy.copy(self.to_stay_lock)
            self.to_stay_lock = []
            show_panel(self.panel)
            self.enabled = True



    def refresh(self):
        if self.enabled:
            self._refresh()
    def _refresh(self):

        x = 2
        y = 2
        box(self.menu_window, 0, 0)
        for i in range(0, len(self.topics)):
            if (self.topics_pointer == i):
                wattron(self.menu_window, A_REVERSE)
                mvwaddstr(self.menu_window, y, x, self.topics[i])
                wattroff(self.menu_window, A_REVERSE)
            elif i in self.locked_topics:
                wattron(self.menu_window, A_UNDERLINE)
                mvwaddstr(self.menu_window, y, x, self.topics[i])
                wattroff(self.menu_window, A_UNDERLINE)
            else:
                mvwaddstr(self.menu_window, y, x, self.topics[i])
            y += 1
        wrefresh(self.menu_window)
        update_panels()
        doupdate()

class GameStat:
    def __init__(self):
        self.enabled = True
        self.x = 0
        self.y = 0
        self.width = 130
        self.height = 5
        self.data_pull = "MONEY: {0}        CITIZENS: {1}      LEVEL: {2}          TIME: {3}      TOWERS: {4}           WAWES: {5}     WAVE LIVES: {6}"
        self.game_stat_window = newwin(self.height, self.width, self.y, self.x)
        self.game_stat_panel = new_panel(self.game_stat_window)
        update_panels()
        doupdate()
    def disable(self):
        if self.enabled:
            self.enabled = False
            hide_panel(self.game_stat_panel)
    def enable(self):
        if not self.enabled:
            self.enabled = True
            show_panel(self.game_stat_panel)

    def refresh(self):
        if self.enabled:
            x = 2
            y = 2
            box(self.game_stat_window, 0, 0)
            wattron(self.game_stat_window, A_REVERSE)
            mvwaddstr(self.game_stat_window, y, x, self.data_pull)
            wattroff(self.game_stat_window, A_REVERSE)
            wrefresh(self.game_stat_window)
            update_panels()
            doupdate()

class GameField:
    def __init__(self):
        self.enabled = True
        self.x = 0
        self.y = 5
        self.width = 130 ## game world.size + 2  (game world size 128)
        self.height = 45 ## game world.size  + 2 (game world size 43)
        self.field_data_pull = [[' ' for x in range(self.width - 2)] for y in range(self.height - 2)]
        self.game_field_window = newwin(self.height, self.width, self.y, self.x)
        self.game_field_panel = new_panel(self.game_field_window)
        update_panels()
        doupdate()

    def disable(self):
        if self.enabled:
            self.enabled = False
            hide_panel(self.game_field_panel)

    def enable(self):
        if not self.enabled:
            self.enabled = True
            show_panel(self.game_field_panel)

    def refresh(self):
        if self.enabled:
            x = 1
            y = 1
            box(self.game_field_window)
            for line in self.field_data_pull:
                for cell in line:
                    mvwaddstr(self.game_field_window, y, x, cell)
                    x += 1
                x = 1
                y += 1
            wrefresh(self.game_field_window)
            update_panels()
            doupdate()


class Button:
    def __init__(self, menu, name, x, y, width, height, button_id):
        self.menu = menu
        self.Parent_menu_window = menu.game_menu_interface_window
        self.name = name
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.button_id = button_id
        self.active = True
        self.button_window = derwin(self.Parent_menu_window, self.height, self.width, self.y, self.x)
        self._activate()

    def _activate(self):
        box(self.button_window)
        mvwaddstr(self.button_window, ((self.height + 1) // 2) - 1, (self.width - len(self.name)) // 2 + 1, self.name)
        wbkgd(self.button_window, BLUE_WHITE) ##### caution
        wrefresh(self.button_window)
        update_panels()
        doupdate()

    def background_change(self):
        if self.under_choice():
            wbkgd(self.button_window, WHITE_BLACK)
            wrefresh(self.button_window)
        elif self.locked():
            wbkgd(self.button_window, CYAN_WHITE)
            wrefresh(self.button_window)
        else:
            wbkgd(self.button_window, BLUE_WHITE)
            wrefresh(self.button_window)

    def under_choice(self):
        return self.menu.topics_pointer == self.button_id

    def locked(self):
        return self.button_id in self.menu.locked_buttons

    def refresh(self):
        self.background_change()
        box(self.button_window)
        wrefresh(self.button_window)


class GameMenuInterface: # make buttons
    def __init__(self):
        self.x = 130
        self.y = 0
        self.width = 20
        self.height = 50
        self.game_menu_interface_window = newwin(self.height, self.width, self.y, self.x)
        self.game_menu_interface_panel = new_panel(self.game_menu_interface_window)
        self.buttons = []
        self._init_buttons()
        self.topics_pointer = 0
        self.locked_buttons = [1, 3]
        self.to_stay_lock = []
        self.last_point = -1
        self.enabled = True
        self.blocked = False
        wbkgd(self.game_menu_interface_window, CYAN_WHITE)
        update_panels()
        doupdate()

    def block(self):
        if not self.blocked:
            self.to_stay_lock = copy.copy(self.locked_buttons)
            self.locked_buttons = list(range(0,len(self.buttons)))
            self.blocked = True
            self.last_point = self.topics_pointer
            self.topics_pointer = -1
            self.refresh()

    def unblock(self):
        if self.blocked:
            self.locked_buttons = copy.copy(self.to_stay_lock)
            self.topics_pointer = self.last_point
            self.to_stay_lock = []
            self.blocked = False

    def disable(self):
        if self.enabled:
            self.to_stay_lock  = copy.copy(self.locked_buttons)
            self.locked_buttons = list(range(0,len(self.buttons)))
            self.enabled = False
            hide_panel(self.game_menu_interface_panel)

    def enable(self):
        if not self.enabled:
            self.locked_buttons = copy.copy(self.to_stay_lock)
            self.to_stay_lock = []
            show_panel(self.game_menu_interface_panel)
            self.enabled = True

    def _init_buttons(self):
        buttons_list = ["MAIN MENU", "TASKS", "FASTER", "SLOWER", "BUILD TOWER", "READY", "PAUSE"]
        x = 1
        y = 1
        buttons_interval = 1
        button_width = 18
        button_height = 4
        for e in range(0, len(buttons_list)):
            self.buttons.append(Button(self, buttons_list[e], x, y, button_width, button_height, e))
            y += button_height + buttons_interval

    def key_event(self,key):
        if self.enabled and not self.blocked:
            if key in [ord('w'), ord('W'), ord('S'), ord('s')]:  # == ord('w') or key == ord('s') oor key == KEY_UP or key == KEY_DOWN:
                self._scroll(key)
            # may be it need to refresh

    def _scroll(self,key):
        if key in [ord('w'), ord('W')]:#== ord('w') or key == KEY_UP:
            self.topics_pointer -= 1
            while(self.topics_pointer  in self.locked_buttons):
                self.topics_pointer -= 1
        elif key in [ord('S'), ord('s')]:  # ord('s') or key == KEY_DOWN:
            self.topics_pointer += 1
            while(self.topics_pointer  in self.locked_buttons):
                self.topics_pointer += 1
        self.topics_pointer %= len(self.buttons)

    def refresh(self):
        if self.enabled:
            x = 1
            y = 1
            for button in self.buttons:
                button.refresh()
            box(self.game_menu_interface_window)
            wrefresh(self.game_menu_interface_window)
            update_panels()
            doupdate()


class GameInterface:
    def __init__(self):
        self.game_stat = GameStat()
        self.game_field = GameField()
        self.game_menu_interface = GameMenuInterface()
        self.main_menu = MainMenu(10, 15)
        self.refresh()

    def refresh(self):
        self.game_stat.refresh()
        self.game_field.refresh()
        self.game_menu_interface.refresh()
        self.main_menu.refresh()

    def key_event(self, key):
        pass

def kbhit():
    ch  = getch()
    if (ch != ERR):
        ungetch(ch)
        return  True
    else:
        return False

stdscr = initscr()
clear()
noecho()
cbreak()
curs_set(0)
keypad(stdscr, True)
start_color()
use_default_colors()
nodelay(stdscr, True)
init_pair(1, COLOR_BLACK, COLOR_WHITE)
init_pair(2, COLOR_WHITE, COLOR_BLUE)
init_pair(3, COLOR_BLACK, COLOR_BLUE)
init_pair(4, COLOR_WHITE, COLOR_CYAN)
bkgd(COLOR_PAIR(2))
WHITE_BLACK = COLOR_PAIR(1)
BLUE_WHITE = COLOR_PAIR(2)
BLUE_BLACK = COLOR_PAIR(3)
CYAN_WHITE = COLOR_PAIR(4)
game_interface = GameInterface()




while True:
    if kbhit():
        key = getch()#(menu_win)
        if (key == 27):
            break
        game_interface.game_menu_interface.key_event(key)
        game_interface.refresh()
        if (key == 97):
            game_interface.game_stat.disable()
            game_interface.refresh()
        if key == 98:
            game_interface.game_stat.enable()
            game_interface.refresh()
        if key == 99:
            game_interface.game_field.disable()
            game_interface.refresh()
        if key ==100:
            game_interface.game_field.enable()
            game_interface.refresh()
        if (key == 27):
            break
    """else:
        refresh()"""

refresh()
clear()
endwin()
