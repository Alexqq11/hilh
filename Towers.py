import sympy.geometry as g
from collections import deque

MAX_TOWER_SPEED_ATTACK = 11


class TowerAbilities:
    def __init__(self, tower_abilities):
        self.physical_attack = tower_abilities["PhysicalAttack"]
        self.froze_attack = tower_abilities["1"]
        self.fire_attack = tower_abilities["1"]
        self.poison_attack = tower_abilities["1"]
        self.electricity_attack = tower_abilities["1"]
        self.slowing_change = tower_abilities["1"]
        self.direction_change = tower_abilities["1"]
        self.attack_radius = tower_abilities["attackRadius"]
        self._attack_speed = None
        self.attack_speed = tower_abilities["Attack_speed"]
        self.attacked_monsters_limit = 2  # todo max 6 monsters under attack

    @property
    def attack_speed(self):
        return self._attack_speed

    @attack_speed.setter
    def attack_speed(self, attack_speed):
        if 1 < attack_speed:
            self._attack_speed = MAX_TOWER_SPEED_ATTACK
        else:
            self._attack_speed = max(MAX_TOWER_SPEED_ATTACK - attack_speed, 1)


class Tower:
    def __init__(self, world, x, y):
        self.world = world
        self.x = x
        self.y = y
        self.width = 3
        self.height = 3
        self.abilities = TowerAbilities(
            {"1": 1, "PhysicalAttack": 1, "attackRadius": 4, "Attack_speed": 1})  # TODO initial configs
        self.price = 10
        self.level = 1
        self.locked = 0
        self.texture = "T"
        self.enemy = "all"
        self.attack_zone = self._init_attack_zone()
        self.kernels = deque()
        self.attacked_monsters = deque()

    def _init_attack_zone(self):  # TODO this to come up with another way
        x = self.x - self.abilities.attack_radius
        y = self.y - self.abilities.attack_radius
        w = self.width - 1 + 2 * self.abilities.attack_radius
        h = self.height - 1 + 2 * self.abilities.attack_radius
        return g.polygon.Polygon(g.Point(x, y), g.Point(x + w, y), g.Point(x + w, y + h), g.Point(x, y + h))

    def in_screen(self, window_width, window_height):
        return 0 <= self.x <= window_width + self.width and 0 <= self.y <= window_height + self.height

    def in_checker_zone(self, monster):
        return (len(monster.polygon.intersection(self.attack_zone)) > 0 or
                len(self.attack_zone.intersection(monster.polygon)) > 0 or
                self.attack_zone.encloses(monster.polygon)) and monster.is_can_be_attacked(self.enemy)

    def attack(self, monster):
        if self.in_checker_zone(monster):  # may be in the future we will don't use this checker
            self.kernels.append(Kernel(self, monster))

    def refresh_kernels(self):
        d = deque()
        for kernel in self.kernels:
            if kernel.alive:
                kernel.refresh()
                d.append(kernel)  # in this place can be bug
        self.kernels = d

    def refresh(self):
        monsters = self.world.monster_wave.monsters_on_map  # caution
        if self.world.draw_system.draw_tick % self.abilities.attack_speed == 0:  # check this
            self._refresh(monsters)

    def _refresh(self, monsters):
        d = deque()
        for x in range(0, len(self.attacked_monsters)):  # caution
            monster = self.attacked_monsters.pop()
            if self.in_checker_zone(monster):
                self.attack(monster)
                d.append(monster)
        self.attacked_monsters = d

        for monster in monsters:
            if self.in_checker_zone(monster):
                if (len(self.attacked_monsters) < self.abilities.attacked_monsters_limit and
                        (monster not in self.attacked_monsters)):
                    self.attack(monster)
                    self.attacked_monsters.append(monster)
        self.refresh_kernels()


class Kernel:  # don't panic
    def __init__(self, tower, monster):
        self.x = tower.x - 1 + (tower.width + 1) // 2
        self.y = tower.y - 1 + (tower.height + 1) // 2
        self.width = 0
        self.height = 0
        self.speed = 4
        self.collision_zone = g.Point(self.x, self.y)
        self.enemy_type = "all"
        self.alive = True
        self.target = monster
        self.parent_tower = tower
        self.texture = "*"

    def in_screen(self, window_width, window_height):
        return 0 <= self.x <= window_width + self.width and 0 <= self.y <= window_height + self.height and self.alive

    def to_target(self):
        progress_x = 0
        progress_y = 0
        step_x = 0
        step_y = 0
        if self.x < self.target.x:
            step_x = 1
        else:
            step_x = -1
        if self.y < self.target.y:
            step_y = 1
        else:
            step_y = -1
        # while (abs(progress_x) + abs(progress_y)) < self.Speed:
        if abs(self.target.x - self.x) < abs(self.target.y - self.y):
            self.y += step_y
            progress_y += step_y
            self.collision_zone = g.Point(self.x, self.y)
        else:
            self.x += step_x
            progress_x += step_x
            self.collision_zone = g.Point(self.x, self.y)
        if abs(self.target.x - self.x) + abs(self.target.y - self.y) < self.target.width + self.target.height:
            self.check_for_collision()

    def check_for_collision(self):
        if (
            self.target.polygon.encloses_point(self.collision_zone) or
            len(self.target.polygon.intersection(self.collision_zone)) > 0
        ):
            self.in_target()

    def refresh(self):
        if not self.parent_tower.in_checker_zone(self.target):
            self.alive = False

        if self.alive:
            self.collision_zone = g.Point(self.x, self.y)
            self.to_target()

    def in_target(self):  # monster attack linked with monster effects
        self.target.effects.towers_attacks.append(self.parent_tower.abilities)
        self.alive = False
