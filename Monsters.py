from collections import deque
import sympy.geometry as g


class MonsterWay:  # todo normal point now tuple with pairs x y
    def __init__(self, monster_way1):
        self.Way = monster_way1
        self.Lobby = 2
        self.City = len(monster_way1) - 2

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
        self.Monsters_lobby = deque(Monster(world, -5, -5) for x in range(0, monster_amount))
        self.Monster_time_interval = monster_time_interval
        self.Monsters_on_map = []  # deque()
        self.World = world
        self.Alive = True
        self.monster_way = monster_way

    def add_on_map(self):
        if self.Monsters_lobby and self.World.Draw_system.Draw_tick % self.Monster_time_interval == 0:
            self.Monsters_on_map.append(self.Monsters_lobby.popleft())

    def refresh_on_map(self):
        for monster in self.Monsters_on_map:
            if monster.Monster_loot.In_city:
                self.World.Player.Monsters_loots.append(monster.Monster_loot)
                monster.Health = 0
            monster.refresh()
            if not monster.Alive:
                self.Monsters_on_map.remove(monster)

    def refresh(self):
        self.add_on_map()
        self.refresh_on_map()
        if not(self.Monsters_lobby or self.Monsters_on_map):
            self.Alive = False





monster_armor1 = {"Froze": 0, "Fire": 0, "Poison": 0, "Electricity": 0, "Physical": 0}
monster_way = MonsterWay(((1,1), (2,1),(3,1),(4,1),(5,1),(6,1),(7,1),(8,1),(9,1),(10,1),(11,1),
                          (12,1),(13,1),(14,1),(15,1),(16,1),(17,1),(18,1),(18,2),(18,3),(18,4),(18,5),
                          (18,6),(18,7),(18,8),(18,9),(18,10),(17,10),(16,10),(15,10),(14,10),(13,10),(12,10),
                          (11,10),(10,10),(9,10),(8,10),(7,10),(6,10),(5,9),(4,8),(3,8),(2,8),(1,8),(0,8),(-1,8)))

MAX_MONSTER_SPEED = 21
MIN_MONSTER_SPEED = 21


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
        self.Monster = Monster
        self.Money = 10
        self.Citizen_annihilation = 1
        self.Experience = 5
        self.In_city = False


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
        if len(self.Towers_attacks) > 0:
            for tower_attack in self.Towers_attacks:
                electricity = tower_attack.Electricity_attack - self.Monster.Armor.Electricity
                poison = tower_attack.Poison_attack - self.Monster.Armor.Poison
                fire = tower_attack.Fire_attack - self.Monster.Armor.Fire
                froze = tower_attack.Froze_attack - self.Monster.Armor.Fire
                damage = tower_attack.Physical_attack - self.Monster.Armor.Physical
                self.Slowing += tower_attack.Slowing_change
                self.Direction = tower_attack.Direction_change
                self.Electricity += electricity if electricity > 0 else 0
                self.Poison += poison if poison > 0 else 0
                self.Froze += froze if froze > 0 else 0
                self.Fire += fire if fire > 0 else 0
                self.Damage += damage if damage > 0 else 0
            self.Towers_attacks = []

    def _effects_calculation(self):
        electricity = 0.33 * self.Froze + (-0.17) * self.Poison + (-0.13) * self.Fire
        fire = 0.46 * self.Electricity + 0.08 * self.Poison + (-1) * self.Froze
        froze = 0.193 * self.Electricity + 0 * self.Poison + (-1) * self.Fire
        poison = (-0.17) * self.Electricity + (-0.37) * self.Froze + (-0.3) * self.Fire
        slowing = 0.83 * self.Froze + (-0.43) * self.Fire + (-0.33) * self.Electricity
        self.Slowing += slowing
        self.Electricity = (self.Electricity + electricity) if self.Electricity + electricity > 0 else 0
        self.Poison = (self.Poison + poison) if self.Poison + poison > 0 else 0
        self.Froze = (self.Froze + froze) if self.Froze + froze > 0 else 0
        self.Fire = (self.Fire + fire) if self.Fire + fire > 0 else 0
        damage = 0.76 * self.Electricity + 0.86 * self.Poison + 0.56 * self.Froze + 0.63 * self.Fire
        self.Damage += damage

    def _tick_effects_update(self):
        self.Damage = 0
        self.Poison *= 0.88
        self.Froze *= 0.67
        self.Fire *= 0.44
        self.Electricity *= 0.2
        self.Slowing *= 0.76
        self.Direction = 1 if self.Monster.World.Draw_system.Draw_tick % 200 == 0 else self.Direction

    def refresh_effects(self):
        self._effects_collecting()
        self._effects_calculation()
        self.Monster.Health -= self.Damage

        self.Monster.Speed_now = self.Monster.Speed_base - int(self.Slowing + 0.5)  # TODO make armotization for this
        self._tick_effects_update()


class Monster:
    def __init__(self, world, x, y):
        self.World = world
        self.X = x
        self.Y = y
        self.Width = 2
        self.Height = 2
        self.Polygon = self._init_polygon()
        self.Speed_base = 5
        self.Speed_now = self._Speed_base
        self.Health = 100
        self.Monster_loot = MonsterLoot(self)
        self.Lived_ticks = 0
        self.Alive = True
        self.Armor = MonsterArmor(self, monster_armor1)
        self.Texture = "MMM"
        self.Effects = MonsterEffects(self)
        self.Type = "all"
        self.Ai_points = 0
        self.Way_position = 0
        self.Monster_way = monster_way
        self.Step = 1  # in future it resizing objects configure

    @property
    def Speed_base(self):
            return self._Speed_base

    @Speed_base.setter
    def Speed_base(self, Speed_base):
        if Speed_base > MAX_MONSTER_SPEED - 1:
            self._Speed_base = MAX_MONSTER_SPEED - 1
        elif Speed_base < -MIN_MONSTER_SPEED:
            self._Speed_base = -MIN_MONSTER_SPEED
        else:
            self._Speed_base = Speed_base

    @property
    def Speed_now(self):
            return self._Speed_now

    @Speed_now.setter
    def Speed_now(self, Speed_now):
        if MAX_MONSTER_SPEED - Speed_now < 1:
            self._Speed_now = 1
        elif Speed_now > MIN_MONSTER_SPEED + MAX_MONSTER_SPEED - 2:
            self._Speed_now = MIN_MONSTER_SPEED + MAX_MONSTER_SPEED - 2
        else:
            self._Speed_now = MAX_MONSTER_SPEED - Speed_now

    def is_can_be_attacked(self, typeof):
        return (typeof == "all" or typeof == self.Type) and self.Alive

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
        if self.World.Draw_system.Draw_tick % self.Speed_now == 0:
            self.Lived_ticks += 1
            self.Lived_ticks %= 100
            if self.Monster_way.in_city(self.Way_position):
                self.Monster_loot.In_city = True
                self.Effects.Direction = 0
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
        return ((self.X >= 0) and (self.X + self.Width <= window_width) and
                (self.Y >= 0) and (self.Y + self.Height <= window_height)) and self.Alive

    def effect_on_tick(self):
        pass
