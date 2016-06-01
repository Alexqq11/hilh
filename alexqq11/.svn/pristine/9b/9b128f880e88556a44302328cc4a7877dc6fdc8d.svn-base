import Towers
import Monsters
import Player
import copy


class GameWorld:
    def __init__(self, draw_system, width, height):
        self.Game_map_static = None
        self.Width = width
        self.Height = height
        self.Monster_wave = Monsters.MonsterWave(self, 5, 60)
        self.Towers_list = []
        self.init_map()
        self.Game_map = copy.deepcopy(self.Game_map_static)
        self.Player = Player.Player()
        self.Draw_system = draw_system
        self.Game_run = True

    def add_tower(self, x, y):
        self.Towers_list.append(Towers.Tower(self, x, y))
        self.Player.Tower_amount += 1

    def can_be_added(self, x, y):
        building_zone_free = True
        for w in range(0, 3):
            for h in range(0,3):
                if not self.Game_map[y+h][x+w] == ':':
                    building_zone_free = False
        return building_zone_free

    def init_map(self):
        self.Game_map_static = [[':' for x in range(self.Width)] for y in range(self.Height)]
        self.Game_map_static[-1] = list(":~~~~~~:" * 16)
        self.Game_map_static[-2] = list(":~~~~~~:" * 16)
        self.Game_map_static[-3] = list("~~~~~~~~" * 16)
        self.Game_map_static[-4] = list("~~~~" * 32)
        self.Game_map_static[-5] = list("~~~~~~~~" * 16)
        self.Game_map_static[-6] = list(":~~~~~~:" * 16)
        for cell in self.Monster_wave.monster_way.Way:
            self.init_cell(cell, ' ')
        self.init_cell(self.Monster_wave.monster_way.Way[0], "#")
        self.init_cell(self.Monster_wave.monster_way.Way[-1], "C")

    def init_cell(self, cell, symbol):
        for w in range(0, 2): # monster width
                for h in range(0, 2): # monster height
                    if 0 <= cell[0] < self.Width + w and 0 <= cell[1] < self.Height + w:
                        self.Game_map_static[cell[1] + h][cell[0] + w] = symbol

    def pause(self):
        if self.Game_run:
            self.Game_run = False
        else:
            self.Game_run = True

    def run(self):
        if self.Game_run:
            self.refresh_world()

    def refresh_world(self):
        self.refresh_exist()
        self.refresh_world_state()

    def refresh_exist(self):
        self.Game_map = copy.deepcopy(self.Game_map_static)  # deepcopy(self.game_map_static)
        for a in self.Monster_wave.Monsters_on_map:
            if a.in_screen(self.Width, self.Height):
                for x in range(a.X, a.X + a.Width):
                    for y in range(a.Y, a.Y + a.Height):
                        self.Game_map[y][x] = a.Texture  # !!!
        for b in self.Towers_list:
            if b.in_screen(self.Width, self.Height):
                for x in range(b.X, b.X + b.Width):
                    for y in range(b.Y, b.Y + b.Height):
                        self.Game_map[y][x] = b.Texture

            for kernel in b.Kernels:
                if kernel.in_screen(self.Width, self.Height):
                    self.Game_map[kernel.Y][kernel.X] = kernel.Texture

    def refresh_world_state(self):
        for tower in self.Towers_list:
            tower.refresh()
        self.Monster_wave.refresh()
        self.Player.refresh()
        if not self.Player.Alive:
            self.Game_run = False
        if not self.Monster_wave.Alive:
            self.Game_run = False
