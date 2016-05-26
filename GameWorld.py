import Towers
import Monsters
import Player
import sympy.geometry as g


class GameWorld:
    def __init__(self, width, height):
        self.game_map_static = [['_' for x in range(width)] for y in range(height)]
        self.game_map = [['_' for x in range(width)] for y in range(height)]
        self.width = width
        self.height = height
        self.test_monster = Monsters.Monster(1, 1)
        self.test_tower = Towers.Tower(3, 4)
        self.Player = Player.Player()

    def refresh_world(self, ):

        a = self.test_monster
        b = self.test_tower

        if not a.Alive:
            self.Player.Momey += a.Money
            a.Money -= a.Money
        print(a.X, " ", a.Y, " ", a.Health, self.Player.Momey)
        self.game_map = [['_' for x in range(self.width)] for y in range(self.height)]  # deepcopy(self.game_map_static)

        if a.in_screen(self.width, self.height):
            for x in range(a.X, a.X + a.Width):
                for y in range(a.Y, a.Y + a.Height):
                    self.game_map[y][x] = a.Texture  # !!!

        if b.in_screen(self.width, self.height):
            for x in range(b.X, b.X + b.Width):
                for y in range(b.Y, b.Y + b.Height):
                    self.game_map[y][x] = b.Texture # !!!

        for kernel in b.Kernels:
            if kernel.in_screen(self.width, self.height):
                self.game_map[kernel.Y][kernel.X] = kernel.Texture

        b.refresh([a])  # todo write full wawes class
        a.move_forward(1)
        a.refresh()
