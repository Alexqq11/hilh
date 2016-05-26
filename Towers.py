import sympy.geometry as g
from collections import deque

tower_abillities1 = {"1": 1, "PhysicalAttac": 1, "attackRadious": 4}


class TowerAbilities:
    def __init__(self, tower_abillities):
        self.PhysicalAttac = tower_abillities["PhysicalAttac"]
        self.FrozeAttac = tower_abillities["1"]
        self.FireAttac = tower_abillities["1"]
        self.PoisonAttac = tower_abillities["1"]
        self.ElectricityAttac = tower_abillities["1"]
        self.SlowingChange = tower_abillities["1"]
        self.DirectionChange = tower_abillities["1"]
        self.AttacRadious = tower_abillities["attackRadious"]
        self.Attacked_monsters_limit = 2 # todo max 6 monsters under attack


class Tower:
    def __init__(self, x, y):
        self.X = x
        self.Y = y
        self.Width = 3
        self.Height = 3
        self.Abilities = TowerAbilities(tower_abillities1)
        self.Price = 10
        self.Level = 1
        self.Locked = 0
        self.Texture = "tow"
        self.Enemy = "all"
        self.AttackZone = self._init_attack_zone()
        self.Kernels = deque()
        # self.Amount_attacked_monsters = 0
        self.Attacked_monsters = deque()

    def _init_attack_zone(self):
        x = self.X + (self.Width + 1) // 2
        y = self.Y + (self.Height + 1) // 2
        r = self.Abilities.AttacRadious + (((self.Width + 1) // 2) + ((self.Height + 1) // 2) + 1) // 2
        return g.ellipse.Circle(g.Point(x, y), r)

    def in_screen(self, window_width, window_height):
        return ((self.X >= 0) and (self.X + self.Width < window_width) and
                (self.Y >= 0) and (self.Y + self.Height < window_height))

    def in_checker_zone(self, monster):
        return len(monster.Polygon.intersection(self.AttackZone)) and monster.is_can_be_attacked(self.Enemy) > 0

    def attack(self, monster):
        if self.in_checker_zone(monster): # may be in the future we will don't use this checker
            self.Kernels.append(Kernel(self, monster))

    def refresh_kernels(self):
        d = deque()
        for kernel in self.Kernels:
            if kernel.Alive:
                kernel.refresh()
                d.append(kernel)  # in this place can be bug
        self.Kernels = d

    def refresh(self, monsters):
        d = deque()
        for x in range(0, len(self.Attacked_monsters)):  # caution
            monster = self.Attacked_monsters.pop()
            if self.in_checker_zone(monster):
                self.attack(monster)
                d.append(monster)
        self.Attacked_monsters = d

        for monster in monsters:
            if self.in_checker_zone(monster):
                if (len(self.Attacked_monsters) < self.Abilities.Attacked_monsters_limit and
                        (monster not in self.Attacked_monsters)):
                    self.attack(monster)
                    self.Attacked_monsters.append(monster)
        self.refresh_kernels()


class Kernel:  # don't panic
    def __init__(self, tower, monster):
        self.X = (tower.Width + 1) // 2  # stupid console
        self.Y = (tower.Width + 1)
        self.Width = 0
        self.Height = 0
        self.Speed = 4
        self.CollisionZone = g.Point(self.X, self.Y)
        self.enemyType = "all"
        self.Alive = True
        self.Target = monster
        self.ParentTower = tower
        self.Texture = "ker"

    def in_screen(self, window_width, window_height):
        return ((self.X >= 0) and (self.X + self.Width < window_width) and
                (self.Y >= 0) and (self.Y + self.Height < window_height)) and self.Alive

    def to_target(self):
        progress_x = 0
        progress_y = 0
        step_x = 0
        step_y = 0
        if self.X < self.Target.X:
            step_x = 1
        else:
            step_x = -1
        if self.Y < self.Target.Y:
            step_y = 1
        else:
            step_y = -1
        while (abs(progress_x) + abs(progress_y)) < self.Speed:
            if abs(self.Target.X - self.X) < abs(self.Target.Y - self.Y):
                self.Y += step_y
                progress_y += step_y
                self.CollisionZone = g.Point(self.X, self.Y)
            else:
                self.X += step_x
                progress_x += step_x
                self.CollisionZone = g.Point(self.X, self.Y)
            if abs(self.Target.X - self.X) + abs(self.Target.Y - self.Y) < self.Target.Width + self.Target.Height:
                self.check_for_collision()

    def check_for_collision(self):
        if len(self.Target.Polygon.intersection(self.CollisionZone)) > 0:
            self.in_target()

    def in_target(self):
        print(self.Target.Health)
        self.Target.Health += self.Target.Armor.Physical - self.ParentTower.Abilities.PhysicalAttac  # TODO write full method of attack with all abbilities
        self.Alive = False

    def refresh(self):
        if not self.ParentTower.in_checker_zone(self.Target):
            self.Alive = False

        if self.Alive:
            self.CollisionZone = g.Point(self.X, self.Y)
            self.to_target()  # TODO in future make queue to kernels
