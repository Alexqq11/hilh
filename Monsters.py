from collections import deque
#import sympy.geometry as g
import Geometry as geo

MAX_MONSTER_SPEED = 21
MIN_MONSTER_SPEED = 21


class MonsterWay:  # todo normal point now tuple with pairs x y
    def __init__(self):
        self.way = ((1, 1), (2, 1), (3, 1), (4, 1), (5, 1), (6, 1), (7, 1), (8, 1), (9, 1), (10, 1), (11, 1),
                    (12, 1), (13, 1), (14, 1), (15, 1), (16, 1), (17, 1), (18, 1), (18, 2), (18, 3), (18, 4),
                    (18, 5), (18, 6), (18, 7), (18, 8), (18, 9), (18, 10), (17, 10), (16, 10), (15, 10), (14, 10),
                    (13, 10), (12, 10), (11, 10), (10, 10), (9, 10), (8, 10), (7, 10), (6, 10), (5, 9), (4, 8),
                    (3, 8), (2, 8), (1, 8), (0, 8), (0, 9), (0, 10), (0, 11), (0, 12), (0, 13), (0, 14), (0, 15),
                    (0, 16), (0, 17), (1, 18), (2, 20), (2, 21), (3, 22), (4, 23), (5, 24), (6, 25), (7, 26), (8, 27),
                    (9, 28), (10, 29), (11, 30), (12, 31), (13, 32), (14, 33), (15, 34), (16, 35), (17, 35), (18, 35),
                    (19, 35), (20, 35), (21, 35), (22, 35), (23, 35), (24, 35), (25, 35), (25, 35), (26, 35),
                    (27, 35), (28, 35), (29, 35), (30, 35), (31, 35), (32, 35), (33, 35), (34, 35), (35, 35), (36, 35),
                    (37, 35), (38, 35), (39, 35), (40, 35), (41, 35), (42, 35), (42, 35), (43, 35), (44, 35), (45, 35),
                    (46, 35), (47, 35), (48, 35), (49, 35), (50, 35), (51, 34), (52, 33), (53, 32), (54, 31), (55, 30),
                    (56, 29), (57, 28), (58, 27), (59, 26), (60, 25), (61, 25)
                    )
        self.lobby = 2
        self.city = len(self.way) - 2

    def in_lobby(self, index):
        return index < self.lobby

    def in_city(self, index):
        return index > self.city

    def x(self, index):
        return self.way[index][0]  # todo this safety with processing

    def y(self, index):
        return self.way[index][1]


class MonsterWave:
    def __init__(self, world, monster_amount, monster_time_interval):
        self.monster_way = MonsterWay()
        self.monsters_lobby = deque(Monster(world, self, -5, -5) for x in range(0, monster_amount))
        self.monster_time_interval = monster_time_interval
        self.monsters_on_map = []  # deque()
        self.world = world
        self.alive = True

        self.health_on_map = 0
        self.monster_wave_health = len(self.monsters_lobby) * 20 + self.health_on_map

    def add_on_map(self):
        if self.monsters_lobby and self.world.draw_system.draw_tick % self.monster_time_interval == 0:
            self.monsters_on_map.append(self.monsters_lobby.popleft())

    def refresh_on_map(self):
        for monster in self.monsters_on_map:
            if not monster.alive:
                if monster.monster_loot:
                    self.world.player.monsters_loots.append(monster.monster_loot)
                    monster.monster_loot = None
                self.monsters_on_map.remove(monster)
            monster.refresh()
            self.health_on_map += max(monster.health, 0)
        self.monster_wave_health = len(self.monsters_lobby) * 20 + self.health_on_map
        self.health_on_map = 0
        self.world.player.wave_health = self.monster_wave_health

    def refresh(self):
        self.add_on_map()
        self.refresh_on_map()
        if not (self.monsters_lobby or self.monsters_on_map):
            self.alive = False


class MonsterArmor:
    def __init__(self, monster, monster_armor):
        self.froze = monster_armor["Froze"]
        self.fire = monster_armor["Fire"]
        self.poison = monster_armor["Poison"]
        self.electricity = monster_armor["Electricity"]
        self.physical = monster_armor["Physical"]
        self.monster = monster


class MonsterLoot:
    def __init__(self, monster):
        self.monster = monster
        self.money = 10
        self.citizen_annihilation = 1
        self.experience = 5
        self.in_city = False
        self.available = True


class MonsterEffects:
    def __init__(self, monster):
        self.froze = 0
        self.fire = 0
        self.poison = 0
        self.electricity = 0
        self.slowing = 5
        self.direction = 1
        self.towers_attacks = []
        self.damage = 0
        self.monster = monster

    def _effects_collecting(self):
        for tower_attack in self.towers_attacks:
            electricity = tower_attack.electricity_attack - self.monster.armor.electricity
            poison = tower_attack.poison_attack - self.monster.armor.poison
            fire = tower_attack.fire_attack - self.monster.armor.fire
            froze = tower_attack.froze_attack - self.monster.armor.fire
            damage = tower_attack.physical_attack - self.monster.armor.physical
            self.slowing += tower_attack.slowing_change
            self.direction = tower_attack.direction_change
            self.electricity += max(electricity, 0)
            self.poison += max(poison, 0)
            self.froze += max(froze, 0)
            self.fire += max(fire, 0)
            self.damage += max(damage, 0)
        self.towers_attacks = []

    def _effects_calculation(self):
        effcoff = {"electricity": self.electricity, "froze": self.froze, "poison": self.poison, "fire": self.fire}
        elecoff = {"electricity": 0, "froze": 0.33, "poison": -0.17, "fire": -0.13}
        fircoff = {"electricity": 0.46, "froze": -1, "poison": 0.08, "fire": 0}
        frocoff = {"electricity": 0.193, "froze": 0, "poison": 0, "fire": -1}
        poicoff = {"electricity": -0.17, "froze": -0.37, "poison": 0, "fire": -0.3}
        slocoff = {"electricity": -0.33, "froze": 0.83, "poison": 0, "fire": -0.43}
        dmgcoff = {"electricity": 0.76, "froze": 0.56, "poison": 0.86, "fire": 0.63}
        electricity = sum(map(lambda x, y: x * y, effcoff.values(), elecoff.values()))
        fire = sum(map(lambda x, y: x * y, effcoff.values(), fircoff.values()))
        froze = sum(map(lambda x, y: x * y, effcoff.values(), frocoff.values()))
        poison = sum(map(lambda x, y: x * y, effcoff.values(), poicoff.values()))
        slowing = sum(map(lambda x, y: x * y, effcoff.values(), slocoff.values()))
        self.slowing += slowing
        self.electricity = max(self.electricity + electricity, 0)
        self.poison = max(self.poison + poison, 0)
        self.froze = max(self.froze + froze, 0)
        self.fire = max(self.fire + fire, 0)
        effcoff = {"electricity": self.electricity, "froze": self.froze, "poison": self.poison, "fire": self.fire}
        damage = sum(map(lambda x, y: x * y, effcoff.values(), dmgcoff.values()))
        self.damage += damage

    def _tick_effects_update(self):
        self.damage = 0
        self.poison *= 0.88
        self.froze *= 0.67
        self.fire *= 0.44
        self.electricity *= 0.2
        self.slowing *= 0.76
        if self.monster.world.draw_system.draw_tick % 200 == 0:
            self.direction = 1
        else:
            self.direction = self.direction

    def refresh_effects(self):
        self._effects_collecting()
        self._effects_calculation()
        self.monster.health -= self.damage

        self.monster.speed_now = self.monster.speed_base - int(self.slowing + 0.5)  # TODO make armotization for this
        self._tick_effects_update()


class Monster:
    def __init__(self, world, wave, x, y):
        self.world = world
        self.wave = wave
        self.x = x
        self.y = y
        self.width = 2
        self.height = 2
        self.polygon = self._init_polygon()
        self._speed_base = None
        self._speed_now = None
        self.speed_base = 5
        self.speed_now = self._speed_base
        self.health = 20
        self.monster_loot = MonsterLoot(self)
        self.lived_ticks = 0
        self.alive = True
        self.armor = MonsterArmor(self, {"Froze": 0, "Fire": 0, "Poison": 0, "Electricity": 0, "Physical": 0})
        self.texture = "M"
        self.effects = MonsterEffects(self)
        self.type = "all"
        self.ai_points = 0
        self.way_position = 0
        self.monster_way = wave.monster_way
        self.step = 1
        # in future it resizing objects configure

    @property
    def speed_base(self):
        return self._speed_base

    @speed_base.setter
    def speed_base(self, speed_base):
        self._speed_base = max(-MIN_MONSTER_SPEED, min(speed_base, MAX_MONSTER_SPEED - 1))

    @property
    def speed_now(self):
        return self._speed_now

    @speed_now.setter
    def speed_now(self, speed_now):
        self._speed_now = min(MIN_MONSTER_SPEED + MAX_MONSTER_SPEED - 2, max(MAX_MONSTER_SPEED - speed_now, 1))

    def is_can_be_attacked(self, typeof):
        return typeof in ("all", self.type) and self.alive

    def _init_polygon(self):
        x = self.x
        y = self.y
        w = self.width - 1
        h = self.height - 1
        return geo.Rectangle(x,y,w,h)#//g.polygon.Polygon(g.Point(x, y), g.Point(x + w, y), g.Point(x + w, y + h), g.Point(x, y + h))

    def refresh(self):
        if not self.alive:
            return
        self.polygon = self._init_polygon()
        self.effects.refresh_effects()
        self.lived_ticks += 1
        self.lived_ticks %= 100
        self.refresh_ai()
        if self.health < 1:
            self.alive = False
            self.x = -1
            self.y = -1

    def refresh_ai(self):
        if self.monster_way.in_city(self.way_position):
            self.monster_loot.in_city = True
            self.effects.Direction = 0
            self.alive = False
        if self.world.draw_system.draw_tick % self.speed_now == 0:
            self.lived_ticks += 1
            self.lived_ticks %= 100
            if self.monster_way.in_lobby(self.way_position):
                self.effects.Direction = 1
            self.move()

    def _movement(self, x, y):
        if self.alive:
            self.x += x
            self.y += y

    def move(self):
        self.way_position += self.step * self.effects.direction
        self.x = self.monster_way.x(self.way_position)
        self.y = self.monster_way.y(self.way_position)

    def in_screen(self, window_width, window_height):
        return 0 <= self.x <= window_width + self.width and 0 <= self.y <= window_height + self.height and self.alive

    def effect_on_tick(self):
        pass
