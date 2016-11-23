from unicurses import *
import copy

from unicurses import A_REVERSE
from unicurses import A_UNDERLINE
from unicurses import CCHAR
from unicurses import COLOR_BLACK
from unicurses import COLOR_BLUE
from unicurses import COLOR_CYAN
from unicurses import COLOR_GREEN
from unicurses import COLOR_PAIR
from unicurses import COLOR_RED
from unicurses import COLOR_WHITE
from unicurses import COLOR_YELLOW
from unicurses import ERR
from unicurses import KEY_DOWN
from unicurses import KEY_LEFT
from unicurses import KEY_RIGHT
from unicurses import KEY_UP
from unicurses import bkgd
from unicurses import box
from unicurses import cbreak
from unicurses import clear
from unicurses import curs_set
from unicurses import delwin
from unicurses import derwin
from unicurses import doupdate
from unicurses import endwin
from unicurses import getch
from unicurses import hide_panel
from unicurses import init_pair
from unicurses import initscr
from unicurses import keypad
from unicurses import mvwaddstr
from unicurses import new_panel
from unicurses import newwin
from unicurses import nodelay
from unicurses import noecho
from unicurses import refresh
from unicurses import show_panel
from unicurses import start_color
from unicurses import ungetch
from unicurses import update_panels
from unicurses import use_default_colors
from unicurses import wattroff
from unicurses import wattron
from unicurses import wbkgd
from unicurses import wborder
from unicurses import wrefresh
from unicurses import *
import GameWorld


class MainMenu:
    def __init__(self, main_interface, width, height):
        self.enabled = True
        self.game_interface = main_interface
        self.y = 15
        self.x = 50
        self.width = width
        self.height = height
        self.menu_window = newwin(height, width, self.y, self.x)
        self.topics = ["NEW GAME", "RESUME GAME", "LOAD GAME", "SAVE GAME", "SETTINGS", "EXIT"]
        self.topics_pointer = 0
        self.locked_topics = [1, 2, 3, 4]
        self.to_stay_lock = []
        self.panel = new_panel(self.menu_window)
        update_panels()
        doupdate()

    def _scroll(self, key):
        if key in [ord('w'), ord('W'), KEY_UP]:
            self.topics_pointer -= 1
            while self.topics_pointer in self.locked_topics:
                self.topics_pointer -= 1
        elif key in [ord('S'), ord('s'), KEY_DOWN]:
            self.topics_pointer += 1
            while self.topics_pointer in self.locked_topics:
                self.topics_pointer += 1
        self.topics_pointer %= len(self.topics)

    def _selected(self):
        if self.topics_pointer == 0:
            if self.game_interface.game_initialized:
                self.game_interface.game_menu_interface.unblock()
                self.game_interface.game_field.unblock()
                self.locked_topics.append(1)
                self.game_interface.game_initialized = False
            self.start_new_game()
        elif self.topics_pointer == 1:
            self.locked_topics.append(1)
            self.game_interface.game_menu_interface.unblock()
            self.game_interface.game.pause()
            if self.game_interface.game_field.blocked:
                self.game_interface.game_field.unblock()
            self.disable()
        elif self.topics_pointer == 5:
            clear()
            endwin()
            exit(0)

    def key_event(self, key):
        if self.enabled:
            if key in [ord('w'), ord('W'), ord('S'), ord('s'), KEY_UP, KEY_DOWN]:
                self._scroll(key)
            elif key == 10:
                self._selected()
            elif key == 27:
                self.topics_pointer = 5
                self._selected()

    def disable(self):
        if self.enabled:
            self.to_stay_lock = copy.copy(self.locked_topics)
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
            if self.topics_pointer == i:
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

    def start_new_game(self):
        self.disable()
        self.game_interface.start_new_game()


class GameStat:
    def __init__(self, main_interface):
        self.game_interface = main_interface
        self.enabled = True
        self.x = 0
        self.y = 0
        self.width = 130
        self.height = 5
        self.game_stat_window = newwin(self.height, self.width, self.y, self.x)
        self.game_stat_panel = new_panel(self.game_stat_window)
        wbkgd(self.game_stat_window, CYAN_RED)
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
            mvwaddstr(self.game_stat_window, y, x, " " * 127)
            if self.game_interface.game_initialized:
                for param in self.game_interface.game.player.strings_info:
                    wattron(self.game_stat_window, A_REVERSE)
                    mvwaddstr(self.game_stat_window, y, x, param, RED_WHITE)
                    wattroff(self.game_stat_window, A_REVERSE)
                    x += 5 + len(param)
            wrefresh(self.game_stat_window)
            update_panels()
            doupdate()


class GameFieldSelector:
    def __init__(self, parent, parent_window):
        self.parent = parent
        self.parent_window = parent_window
        self.x = 1
        self.y = 1
        self.width = 3
        self.height = 3
        self.selector_zone = None
        self.create_win()
        self.building_zone_free = False

    def create_win(self):
        local_win = derwin(self.parent_window, self.height, self.width, self.y, self.x)
        box(local_win, 0, 0)
        wrefresh(local_win)
        self.selector_zone = local_win

    def destroy_win(self):
        wborder(self.selector_zone, CCHAR(' '), CCHAR(' '), CCHAR(' '), CCHAR(' '), CCHAR(' '), CCHAR(' '), CCHAR(' '),
                CCHAR(' '))
        wrefresh(self.selector_zone)
        delwin(self.selector_zone)

    def refresh_for_draw(self):
        self.building_zone_free = self.parent.game_interface.game.can_be_added(self.x - 1, self.y - 1)
        box(self.selector_zone, 0, 0)
        if self.building_zone_free:
            wbkgd(self.selector_zone, BLACK_GREEN)
        else:
            wbkgd(self.selector_zone, BLACK_RED)
        wrefresh(self.selector_zone)

    def key_event(self, key):
        if key in [ord('w'), ord('W'), KEY_UP]:
            if self.y - 1 > 0:
                self.destroy_win()
                self.y -= 1
                self.create_win()
        elif key in [ord('S'), ord('s'), KEY_DOWN]:
            if self.y + self.height < self.parent.height - 1:
                self.destroy_win()
                self.y += 1
                self.create_win()
        elif key in [ord('a'), ord('A'), KEY_LEFT]:
            if self.x - 1 > 0:
                self.destroy_win()
                self.x -= 1
                self.create_win()
        elif key in [ord("d"), ord("D"), KEY_RIGHT]:
            if self.x + self.width < self.parent.width - 1:
                self.destroy_win()
                self.x += 1
                self.create_win()
        elif key == 10:
            if self.building_zone_free:
                self.destroy_win()


class GameField:
    def __init__(self, main_interface):
        self.game_interface = main_interface
        self.enabled = True
        self.blocked = False
        self.x = 0
        self.y = 5
        self.point_x = 1
        self.point_y = 1
        self.width = 130
        self.height = 45
        self.field_data_pull = None
        self.game_field_window = newwin(self.height, self.width, self.y, self.x)
        self.game_field_panel = new_panel(self.game_field_window)
        self.selector = None
        wbkgd(self.game_field_window, CYAN_RED)
        update_panels()
        doupdate()

    def block(self):
        self.blocked = True

    def unblock(self):
        self.blocked = False

    def key_event(self, key):
        self.building(key)

    def building(self, key):
        if not self.selector:
            self.selector = GameFieldSelector(self, self.game_field_window)
        self.selector.key_event(key)
        if key == 10:
            if self.selector.building_zone_free:
                self.game_interface.game.add_tower(self.selector.x - 1, self.selector.y - 1)
                self.exit_building()
        elif key == 27:
            self.exit_building()
        wrefresh(self.game_field_window)
        update_panels()
        doupdate()

    def exit_building(self):
        self.selector = None
        self.game_interface.game.refresh_exist()
        self.game_interface.game_menu_interface.unblock()
        self.game_interface.game.pause()
        self.game_interface.game_field.unblock()

    def disable(self):
        if self.enabled:
            self.enabled = False
            hide_panel(self.game_field_panel)

    def enable(self):
        if not self.enabled:
            self.enabled = True
            show_panel(self.game_field_panel)

    def draw(self):
        if self.game_interface.game_initialized:
            self.field_data_pull = self.game_interface.game.game_map
            x = 1
            y = 1

            for line in self.field_data_pull:
                for cell in line:
                    if cell == ':':
                        mvwaddstr(self.game_field_window, y, x, cell, GREEN_YELLOW)
                    elif cell == '~':
                        mvwaddstr(self.game_field_window, y, x, cell, BLUE_WHITE)
                    elif cell == '#':
                        mvwaddstr(self.game_field_window, y, x, cell, BLACK_RED)
                    elif cell == 'C':
                        mvwaddstr(self.game_field_window, y, x, cell, BLUE_WHITE)
                    else:
                        mvwaddstr(self.game_field_window, y, x, cell, WHITE_BLACK)
                    x += 1
                x = 1
                y += 1
            wrefresh(self.game_field_window)
            if self.selector:
                self.selector.refresh_for_draw()
            update_panels()
            doupdate()

    def refresh(self):
        if self.enabled and not self.blocked:
            self.draw()
            box(self.game_field_window)
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
        wbkgd(self.button_window, BLUE_WHITE)
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


class GameMenuInterface:  # make buttons
    def __init__(self, main_interface):
        self.game_interface = main_interface
        self.x = 130
        self.y = 0
        self.width = 20
        self.height = 50
        self.game_menu_interface_window = newwin(self.height, self.width, self.y, self.x)
        self.game_menu_interface_panel = new_panel(self.game_menu_interface_window)
        self.buttons = []
        self.buttons_list = ["MAIN MENU", "TASKS", "FASTER", "SLOWER", "BUILD TOWER", "READY", "PAUSE"]
        self._init_buttons()
        self.topics_pointer = 0
        self.locked_buttons = [1, 2, 3, 5]
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
            self.locked_buttons = list(range(0, len(self.buttons)))
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
            self.to_stay_lock = copy.copy(self.locked_buttons)
            self.locked_buttons = list(range(0, len(self.buttons)))
            self.enabled = False
            hide_panel(self.game_menu_interface_panel)

    def enable(self):
        if not self.enabled:
            self.locked_buttons = copy.copy(self.to_stay_lock)
            self.to_stay_lock = []
            show_panel(self.game_menu_interface_panel)
            self.enabled = True

    def _init_buttons(self):
        buttons_list = self.buttons_list
        x = 1
        y = 1
        buttons_interval = 1
        button_width = 18
        button_height = 4
        for e in range(0, len(buttons_list)):
            self.buttons.append(Button(self, buttons_list[e], x, y, button_width, button_height, e))
            y += button_height + buttons_interval

    def key_event(self, key):
        if self.enabled and not self.blocked:
            if key in [ord('w'), ord('W'), ord('S'), ord('s'), KEY_UP, KEY_DOWN]:
                self._scroll(key)
            if key == 10:
                self.selected()
                # may be it need to refresh

    def selected(self):
        if self.topics_pointer == 6:
            self.game_interface.game.pause()
        elif self.topics_pointer == 4:
            if self.game_interface.game.game_run:
                self.game_interface.game.pause()
            self.block()
        elif self.topics_pointer == 0:
            self.block()
            self.game_interface.game_field.block()
            if self.game_interface.game.game_run:
                self.game_interface.game.pause()
            self.game_interface.main_menu.enable()
            self.game_interface.main_menu.locked_topics.remove(1)

    def _scroll(self, key):
        if key in [ord('w'), ord('W'), KEY_UP]:  # == ord('w') or key == KEY_UP:
            self.topics_pointer -= 1
            while self.topics_pointer in self.locked_buttons:
                self.topics_pointer -= 1
        elif key in [ord('S'), ord('s'), KEY_DOWN]:  # ord('s') or key == KEY_DOWN:
            self.topics_pointer += 1
            while self.topics_pointer in self.locked_buttons:
                self.topics_pointer += 1
        self.topics_pointer %= len(self.buttons)

    def refresh(self):
        if self.enabled:
            for button in self.buttons:
                button.refresh()
            box(self.game_menu_interface_window)
            wrefresh(self.game_menu_interface_window)
            update_panels()
            doupdate()


class GameInterface:
    def __init__(self):
        self.game_stat = GameStat(self)
        self.game_field = GameField(self)
        self.game_menu_interface = GameMenuInterface(self)
        self.main_menu = MainMenu(self, 35, 15)
        self.game = None
        self.game_initialized = False
        self.draw_tick = 0
        self.world_speed = 0.07  # world_speed * 0.07
        self.refresh()

    def start_new_game(self):
        self.game = GameWorld.GameWorld(self, self.game_field.width - 2, self.game_field.height - 2)
        self.game_field.enable()
        self.game_stat.enable()
        self.game_menu_interface.enable()
        self.game_initialized = True

    def refresh(self):
        self.game_stat.refresh()
        self.game_field.refresh()
        self.game_menu_interface.refresh()
        self.main_menu.refresh()
        if self.game_initialized:
            self.game.run()

    def first_launch(self):
        self.game_stat.disable()
        self.game_field.disable()
        self.game_menu_interface.disable()

    def key_event(self, key):
        if not self.game_menu_interface.enabled and not self.game_field.enabled and not self.game_stat.enabled:
            self.main_menu.key_event(key)
        elif self.main_menu.enabled and self.game_menu_interface.blocked:
            self.main_menu.key_event(key)
        elif not self.main_menu.enabled and self.game_menu_interface.blocked:
            self.game_field.key_event(key)
        else:
            self.game_menu_interface.key_event(key)

if __name__ == "__main__":
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
    init_pair(5, COLOR_YELLOW, COLOR_GREEN)
    init_pair(6, COLOR_GREEN, COLOR_BLACK)
    init_pair(7, COLOR_RED, COLOR_BLACK)
    init_pair(8, COLOR_BLUE, COLOR_YELLOW)
    init_pair(9, COLOR_RED, COLOR_YELLOW)
    init_pair(10, COLOR_WHITE, COLOR_RED)
    init_pair(11, COLOR_RED, COLOR_CYAN)

    WHITE_BLACK = COLOR_PAIR(1)
    BLUE_WHITE = COLOR_PAIR(2)
    BLUE_BLACK = COLOR_PAIR(3)
    CYAN_WHITE = COLOR_PAIR(4)
    GREEN_YELLOW = COLOR_PAIR(5)
    BLACK_GREEN = COLOR_PAIR(6)
    BLACK_RED = COLOR_PAIR(7)
    YELLOW_BLUE = COLOR_PAIR(8)
    YELLOW_RED = COLOR_PAIR(9)
    RED_WHITE = COLOR_PAIR(10)
    CYAN_RED = COLOR_PAIR(11)

    bkgd(COLOR_PAIR(2))

    game_interface = GameInterface()
    game_interface.refresh()
    game_interface.first_launch()


    def kbhit():
        ch = getch()
        if ch != ERR:
            ungetch(ch)
            return True
        else:
            return False


    while True:
        if kbhit():
            key = getch()
            game_interface.key_event(key)
            game_interface.refresh()
        else:
            game_interface.refresh()
        game_interface.draw_tick += 1
        game_interface.draw_tick %= 1000

    refresh()
    clear()
    endwin()
