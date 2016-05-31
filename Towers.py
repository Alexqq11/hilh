import sympy.geometry as g
from collections import deque

tower_abilities1 = {"1": 1, "PhysicalAttack": 1, "attackRadius": 4, "Attack_speed": 1}
MAX_TOWER_SPEED_ATTACK = 11


class TowerAbilities:
    def __init__(self, tower_abilities):
        self.Physical_attack = tower_abilities["PhysicalAttack"]
        self.Froze_attack = tower_abilities["1"]
        self.Fire_attack = tower_abilities["1"]
        self.Poison_attack = tower_abilities["1"]
        self.Electricity_attack = tower_abilities["1"]
        self.Slowing_change = tower_abilities["1"]
        self.Direction_change = tower_abilities["1"]
        self.Attack_radius = tower_abilities["attackRadius"]
        self.Attack_speed = tower_abilities["Attack_speed"]
        self.Attacked_monsters_limit = 2  # todo max 6 monsters under attack

    @property
    def Attack_speed(self):
            return self._Attack_speed

    @Attack_speed.setter
    def Attack_speed(self, Attack_speed):
        if 1 > MAX_TOWER_SPEED_ATTACK - Attack_speed:
            self._Attack_speed = 1
        elif Attack_speed < 1:
            self._Attack_speed = 11
        else:
            self._Attack_speed = MAX_TOWER_SPEED_ATTACK - Attack_speed


class Tower:
    def __init__(self, world, x, y):
        self.World = world
        self.X = x
        self.Y = y
        self.Width = 3
        self.Height = 3
        self.Abilities = TowerAbilities(tower_abilities1)  # TODO initial configs
        self.Price = 10
        self.Level = 1
        self.Locked = 0
        self.Texture = "tow"
        self.Enemy = "all"
        self.Attack_zone = self._init_attack_zone()
        self.Kernels = deque()
        self.Attacked_monsters = deque()

    def _init_attack_zone(self):  # TODO this to come up with another way
        x = self.X - self.Abilities.Attack_radius
        y = self.Y - self.Abilities.Attack_radius
        w = self.Width - 1 + 2 * self.Abilities.Attack_radius
        h = self.Height - 1 + 2 * self.Abilities.Attack_radius
        return g.polygon.Polygon(g.Point(x, y), g.Point(x + w, y), g.Point(x + w, y + h), g.Point(x, y + h))

    def in_screen(self, window_width, window_height):
        return ((self.X >= 0) and (self.X + self.Width <= window_width) and
                (self.Y >= 0) and (self.Y + self.Height <= window_height))

    def in_checker_zone(self, monster):
        return (len(monster.Polygon.intersection(self.Attack_zone)) > 0 or
                len(self.Attack_zone.intersection(monster.Polygon)) > 0 or
                self.Attack_zone.encloses(monster.Polygon)) and monster.is_can_be_attacked(self.Enemy)

    def attack(self, monster):
        if self.in_checker_zone(monster):  # may be in the future we will don't use this checker
            self.Kernels.append(Kernel(self, monster))

    def refresh_kernels(self):
        d = deque()
        for kernel in self.Kernels:
            if kernel.Alive:
                kernel.refresh()
                d.append(kernel)  # in this place can be bug
        self.Kernels = d

    def refresh(self):
        monsters = self.World.Monster_wave.Monsters_on_map   # caution
        if self.World.Draw_system.Draw_tick % self.Abilities.Attack_speed == 0:  # check this
            self._refresh(monsters)

    def _refresh(self, monsters):
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
        self.X = tower.X - 1 + (tower.Width + 1) // 2  # stupid console
        self.Y = tower.Y - 1 + (tower.Height + 1) // 2
        self.Width = 0
        self.Height = 0
        self.Speed = 4
        self.Collision_zone = g.Point(self.X, self.Y)
        self.Enemy_type = "all"
        self.Alive = True
        self.Target = monster
        self.Parent_tower = tower
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
        # while (abs(progress_x) + abs(progress_y)) < self.Speed:
        if abs(self.Target.X - self.X) < abs(self.Target.Y - self.Y):
            self.Y += step_y
            progress_y += step_y
            self.Collision_zone = g.Point(self.X, self.Y)
        else:
            self.X += step_x
            progress_x += step_x
            self.Collision_zone = g.Point(self.X, self.Y)
        if abs(self.Target.X - self.X) + abs(self.Target.Y - self.Y) < self.Target.Width + self.Target.Height:
            self.check_for_collision()

    def check_for_collision(self):
        if self.Target.Polygon.encloses_point(self.Collision_zone) or \
                len(self.Target.Polygon.intersection(self.Collision_zone)) > 0:
            self.in_target()

    def refresh(self):
        if not self.Parent_tower.in_checker_zone(self.Target):
            self.Alive = False

        if self.Alive:
            self.Collision_zone = g.Point(self.X, self.Y)
            self.to_target()

    def in_target(self):  # monster attack linked with monster effects
        self.Target.Effects.Towers_attacks.append(self.Parent_tower.Abilities)
        self.Alive = False
