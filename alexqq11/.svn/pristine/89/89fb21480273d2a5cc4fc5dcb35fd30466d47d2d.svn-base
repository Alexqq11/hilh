import Towers
import Monsters
import Player
import copy


class GameWorld:
    def __init__(self, draw_system, width, height):
        self.game_map_static = None
        self.width = width
        self.height = height
        self.monster_wave = Monsters.MonsterWave(self, 5, 60)
        self.towers_list = []
        self.init_map()
        self.game_map = copy.deepcopy(self.game_map_static)
        self.player = Player.Player()
        self.draw_system = draw_system
        self.game_run = True

    def add_tower(self, x, y):
        self.towers_list.append(Towers.Tower(self, x, y))
        self.player.tower_amount += 1

    def can_be_added(self, x, y):
        building_zone_free = True
        for w in range(0, 3):
            for h in range(0, 3):
                if not self.game_map[y + h][x + w] == ':':
                    building_zone_free = False
        return building_zone_free

    def init_map(self):
        self.game_map_static = [[':' for x in range(self.width)] for y in range(self.height)]
        self.game_map_static[-1] = list(":~~~~~~:" * 16)
        self.game_map_static[-2] = list(":~~~~~~:" * 16)
        self.game_map_static[-3] = list("~~~~~~~~" * 16)
        self.game_map_static[-4] = list("~~~~" * 32)
        self.game_map_static[-5] = list("~~~~~~~~" * 16)
        self.game_map_static[-6] = list(":~~~~~~:" * 16)
        for cell in self.monster_wave.monster_way.way:
            self.init_cell(cell, ' ')
        self.init_cell(self.monster_wave.monster_way.way[0], "#")
        self.init_cell(self.monster_wave.monster_way.way[-1], "C")

    def init_cell(self, cell, symbol):
        for w in range(0, 2):  # monster width
            for h in range(0, 2):  # monster height
                if 0 <= cell[0] < self.width + w and 0 <= cell[1] < self.height + w:
                    self.game_map_static[cell[1] + h][cell[0] + w] = symbol

    def pause(self):
        if self.game_run:
            self.game_run = False
        else:
            self.game_run = True

    def run(self):
        if self.game_run:
            self.refresh_world()

    def refresh_world(self):
        self.refresh_exist()
        self.refresh_world_state()

    def refresh_exist(self):
        self.game_map = copy.deepcopy(self.game_map_static)  # deepcopy(self.game_map_static)
        for a in self.monster_wave.monsters_on_map:
            if a.in_screen(self.width, self.height):
                for x in range(a.x, a.x + a.width):
                    for y in range(a.y, a.y + a.height):
                        self.game_map[y][x] = a.texture  # !!!
        for b in self.towers_list:
            if b.in_screen(self.width, self.height):
                for x in range(b.x, b.x + b.width):
                    for y in range(b.y, b.y + b.height):
                        self.game_map[y][x] = b.texture

            for kernel in b.kernels:
                if kernel.in_screen(self.width, self.height):
                    self.game_map[kernel.y][kernel.x] = kernel.texture

    def refresh_world_state(self):
        for tower in self.towers_list:
            tower.refresh()
        self.monster_wave.refresh()
        self.player.refresh()
        if not self.player.alive:
            self.game_run = False
        if not self.monster_wave.alive:
            self.game_run = False
