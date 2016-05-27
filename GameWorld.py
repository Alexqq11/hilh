import Towers
import Monsters
import Player


class GameWorld:
    def __init__(self, width, height):
        self.Game_map_static = [['_' for x in range(width)] for y in range(height)]
        self.Game_map = [['_' for x in range(width)] for y in range(height)]
        self.Width = width
        self.Height = height
        self.Test_monster = Monsters.Monster(1, 1)
        self.Test_tower = Towers.Tower(3, 4)
        self.Player = Player.Player()

    def refresh_world(self, ):

        a = self.Test_monster
        b = self.Test_tower

        if not a.Alive:
            self.Player.Momey += a.Money
            a.Money -= a.Money
        print(a.X, " ", a.Y, " ", a.Health, self.Player.Momey)
        self.Game_map = [['_' for x in range(self.Width)] for y in range(self.Height)]  # deepcopy(self.game_map_static)

        if a.in_screen(self.Width, self.Height):
            for x in range(a.X, a.X + a.Width):
                for y in range(a.Y, a.Y + a.Height):
                    self.Game_map[y][x] = a.Texture  # !!!

        if b.in_screen(self.Width, self.Height):
            for x in range(b.X, b.X + b.Width):
                for y in range(b.Y, b.Y + b.Height):
                    self.Game_map[y][x] = b.Texture  # !!!

        for kernel in b.Kernels:
            if kernel.in_screen(self.Width, self.Height):
                self.Game_map[kernel.Y][kernel.X] = kernel.Texture

        b.refresh([a])  # todo write full wawes class
        a.move_forward(1)
        a.refresh()
