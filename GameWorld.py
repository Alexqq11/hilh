import Towers
import Monsters
import Player

class GameWorld:
    def __init__(self, draw_system, width, height):
        self.Game_map_static = [['_' for x in range(width)] for y in range(height)]
        self.Game_map = [['_' for x in range(width)] for y in range(height)]
        self.Width = width
        self.Height = height
        self.Monster_wave = Monsters.MonsterWave(self, 5, 20)
        self.Test_monster = Monsters.Monster(self, 1, 1)
        self.Test_tower = Towers.Tower(self, 3, 4)
        self.Player = Player.Player()
        self.Test_tower_2 = Towers.Tower(self, 9, 4)
        self.Draw_system = draw_system
        self.Game_run = True

    def refresh_world(self, ):
        #a = self.Test_monster
        b = self.Test_tower
        c = self.Test_tower_2

        ###print(a.X, " ", a.Y, " ", a.Health, self.Player.Money)
        self.Game_map = [['_' for x in range(self.Width)] for y in range(self.Height)]  # deepcopy(self.game_map_static)
        for a in self.Monster_wave.Monsters_on_map:
            if a.in_screen(self.Width, self.Height):
                for x in range(a.X, a.X + a.Width):
                    for y in range(a.Y, a.Y + a.Height):
                        self.Game_map[y][x] = a.Texture  # !!!

        if b.in_screen(self.Width, self.Height):
            for x in range(b.X, b.X + b.Width):
                for y in range(b.Y, b.Y + b.Height):
                    self.Game_map[y][x] = b.Texture  # !!!
        if c.in_screen(self.Width, self.Height):
            for x in range(c.X, c.X + c.Width):
                for y in range(c.Y, c.Y + c.Height):
                    self.Game_map[y][x] = c.Texture  # !!!

        for kernel in b.Kernels:
            if kernel.in_screen(self.Width, self.Height):
                self.Game_map[kernel.Y][kernel.X] = kernel.Texture

        for kernel in c.Kernels:
            if kernel.in_screen(self.Width, self.Height):
                self.Game_map[kernel.Y][kernel.X] = kernel.Texture

        b.refresh()

        c.refresh()  # todo write full wawes class
        self.Monster_wave.refresh()
        self.Player.refresh()
        if not self.Player.Alive:
            self.Game_run = False
            print("loser")
        if not self.Monster_wave.Alive:
            self.Game_run = False
            print("lol you did it")