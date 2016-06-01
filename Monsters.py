from collections import deque
import sympy.geometry as g

MAX_MONSTER_SPEED = 21
MIN_MONSTER_SPEED = 21

class MonsterWay:  # todo normal point now tuple with pairs x y
    def __init__(self):
        self.Way = ((1, 1), (2, 1), (3, 1), (4, 1), (5, 1), (6, 1), (7, 1), (8, 1), (9, 1), (10, 1), (11, 1),
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
        self.Lobby = 2
        self.City = len(self.Way) - 2

    def in_lobby(self, index):
        return index < self.Lobby

    def in_city(self, index):
        return index > self.City

    def x(self, index):
        return self.Way[index][0]  # todo this safety with processing

    def y(self, index):
        return self.Way[index][1]


class MonsterWave:
    def __init__(self, world, monster_amount, monster_time_interval):
        self.monster_way = MonsterWay()
        self.Monsters_lobby = deque(Monster(world, self, -5, -5) for x in range(0, monster_amount))
        self.Monster_time_interval = monster_time_interval
        self.Monsters_on_map = []  # deque()
        self.World = world
        self.Alive = True

        self.health_on_map = 0
        self.Monster_wave_health = len(self.Monsters_lobby) * 20 + self.health_on_map

    def add_on_map(self):
        if self.Monsters_lobby and self.World.Draw_system.Draw_tick % self.Monster_time_interval == 0:
            self.Monsters_on_map.append(self.Monsters_lobby.popleft())

    def refresh_on_map(self):
        for monster in self.Monsters_on_map:
            if not monster.Alive:
                if monster.Monster_loot:
                    self.World.Player.Monsters_loots.append(monster.Monster_loot)
                    monster.Monster_loot = None
                self.Monsters_on_map.remove(monster)
            monster.refresh()
            self.health_on_map += max(monster.Health, 0)
        self.Monster_wave_health = len(self.Monsters_lobby) * 20 + self.health_on_map
        self.health_on_map = 0
        self.World.Player.wave_health = self.Monster_wave_health

    def refresh(self):
        self.add_on_map()
        self.refresh_on_map()
        if not(self.Monsters_lobby or self.Monsters_on_map):
            self.Alive = False


class MonsterArmor:
    def __init__(self, monster, monster_armor):
        self.Froze = monster_armor["Froze"]
        self.Fire = monster_armor["Fire"]
        self.Poison = monster_armor["Poison"]
        self.Electricity = monster_armor["Electricity"]
        self.Physical = monster_armor["Physical"]
        self.Monster = monster


class MonsterLoot:
    def __init__(self, monster):
        self.Monster = monster
        self.Money = 10
        self.Citizen_annihilation = 1
        self.Experience = 5
        self.In_city = False
        self.available = True


class MonsterEffects:
    def __init__(self, monster):
        self.Froze = 0
        self.Fire = 0
        self.Poison = 0
        self.Electricity = 0
        self.Slowing = 5
        self.Direction = 0
        self.Towers_attacks = []
        self.Damage = 0
        self.Monster = monster

    def _effects_collecting(self):
        for tower_attack in self.Towers_attacks:
            electricity = tower_attack.Electricity_attack - self.Monster.Armor.Electricity
            poison = tower_attack.Poison_attack - self.Monster.Armor.Poison
            fire = tower_attack.Fire_attack - self.Monster.Armor.Fire
            froze = tower_attack.Froze_attack - self.Monster.Armor.Fire
            damage = tower_attack.Physical_attack - self.Monster.Armor.Physical
            self.Slowing += tower_attack.Slowing_change
            self.Direction = tower_attack.Direction_change
            self.Electricity += max(electricity, 0)
            self.Poison += max(poison, 0)
            self.Froze += max(froze, 0)
            self.Fire += max(fire, 0)
            self.Damage += max(damage, 0)
        self.Towers_attacks = []

    def _effects_calculation(self):
        effcoff = {"electricity": self.Electricity, "froze": self.Froze, "poison": self.Poison, "fire": self.Fire}
        elecoff = {"electricity": 0, "froze": 0.33, "poison": -0.17, "fire": -0.13}
        fircoff = {"electricity": 0.46, "froze": -1, "poison": 0.08, "fire": 0}
        frocoff = {"electricity": 0.193, "froze": 0, "poison": 0, "fire": -1}
        poicoff = {"electricity": -0.17, "froze": -0.37, "poison": 0, "fire": -0.3}
        slocoff = {"electricity": -0.33, "froze": 0.83, "poison": 0, "fire": -0.43}
        dmgcoff = {"electricity": 0.76, "froze": 0.56, "poison": 0.86, "fire": 0.63}
        electricity = sum(map(lambda x, y: x * y, list(effcoff.values()), list(elecoff.values())))
        fire = sum(map(lambda x, y: x * y, list(effcoff.values()), list(fircoff.values())))
        froze = sum(map(lambda x, y: x * y, list(effcoff.values()), list(frocoff.values())))
        poison = sum(map(lambda x, y: x * y, list(effcoff.values()), list(poicoff.values())))
        slowing = sum(map(lambda x, y: x * y, list(effcoff.values()), list(slocoff.values())))
        self.Slowing += slowing
        self.Electricity = max(self.Electricity + electricity, 0)
        self.Poison = max(self.Poison + poison, 0)
        self.Froze = max(self.Froze + froze, 0)
        self.Fire = max(self.Fire + fire, 0)
        effcoff = {"electricity": self.Electricity, "froze": self.Froze, "poison": self.Poison, "fire": self.Fire}
        damage = sum(map(lambda x, y: x * y, list(effcoff.values()), list(dmgcoff.values())))
        self.Damage += damage

    def _tick_effects_update(self):
        self.Damage = 0
        self.Poison *= 0.88
        self.Froze *= 0.67
        self.Fire *= 0.44
        self.Electricity *= 0.2
        self.Slowing *= 0.76
        if self.Monster.World.Draw_system.Draw_tick % 200 == 0:
            self.Direction = 1
        else:
            self.Direction = self.Direction

    def refresh_effects(self):
        self._effects_collecting()
        self._effects_calculation()
        self.Monster.Health -= self.Damage

        self.Monster.Speed_now = self.Monster.Speed_base - int(self.Slowing + 0.5)  # TODO make armotization for this
        self._tick_effects_update()


class Monster:
    def __init__(self, world, wave, x, y):
        self.World = world
        self.wave = wave
        self.X = x
        self.Y = y
        self.Width = 2
        self.Height = 2
        self.Polygon = self._init_polygon()
        self.Speed_base = 5
        self.Speed_now = self._Speed_base
        self.Health = 20
        self.Monster_loot = MonsterLoot(self)
        self.Lived_ticks = 0
        self.Alive = True
        self.Armor = MonsterArmor(self, {"Froze": 0, "Fire": 0, "Poison": 0, "Electricity": 0, "Physical": 0})
        self.Texture = "M"
        self.Effects = MonsterEffects(self)
        self.Type = "all"
        self.Ai_points = 0
        self.Way_position = 0
        self.Monster_way = wave.monster_way
        self.Step = 1  # in future it resizing objects configure

    @property
    def Speed_base(self):
            return self._Speed_base

    @Speed_base.setter
    def Speed_base(self, Speed_base):
        self._Speed_base = max(-MIN_MONSTER_SPEED, min(Speed_base, MAX_MONSTER_SPEED - 1))
    @property
    def Speed_now(self):
        return self._Speed_now

    @Speed_now.setter
    def Speed_now(self, Speed_now):
        self._Speed_now = min(MIN_MONSTER_SPEED + MAX_MONSTER_SPEED - 2, max(MAX_MONSTER_SPEED - Speed_now, 1))

    def is_can_be_attacked(self, typeof):
        return typeof in ("all", self.Type) and self.Alive

    def _init_polygon(self):
        x = self.X
        y = self.Y
        w = self.Width - 1
        h = self.Height - 1
        return g.polygon.Polygon(g.Point(x, y), g.Point(x + w, y), g.Point(x + w, y + h), g.Point(x, y + h))

    def refresh(self):
        if self.Alive:
            self.Polygon = self._init_polygon()
            self.Effects.refresh_effects()
            self.Lived_ticks += 1
            self.Lived_ticks %= 100
            self.refresh_ai()
            if self.Health < 1:
                self.Alive = False
                self.X = -1
                self.Y = -1

    def refresh_ai(self):
        if self.Monster_way.in_city(self.Way_position):
            self.Monster_loot.In_city = True
            self.Effects.Direction = 0
            self.Alive = False
        if self.World.Draw_system.Draw_tick % self.Speed_now == 0:
            self.Lived_ticks += 1
            self.Lived_ticks %= 100
            if self.Monster_way.in_lobby(self.Way_position):
                self.Effects.Direction = 1
            self.move()

    def _movement(self, x, y):
        if self.Alive:
            self.X += x
            self.Y += y

    def move(self):
        self.Way_position += self.Step * self.Effects.Direction
        self.X = self.Monster_way.x(self.Way_position)
        self.Y = self.Monster_way.y(self.Way_position)

    def in_screen(self, window_width, window_height):
        return 0 <= self.X <= window_width + self.Width and 0 <= self.Y <= window_height + self.Height and self.Alive

    def effect_on_tick(self):
        pass
