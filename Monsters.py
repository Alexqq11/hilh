import sympy.geometry as g

monster_armor1 = {"Froze": 0, "Fire": 0, "Poison": 0, "Electricity": 0, "Physical": 0}
MAX_MONSTER_SPEED = 21


class MonsterArmor:
    def __init__(self, monster, monster_armor):
        self.Froze = monster_armor["Froze"]
        self.Fire = monster_armor["Fire"]
        self.Poison = monster_armor["Poison"]
        self.Electricity = monster_armor["Electricity"]
        self.Physical = monster_armor["Physical"]
        self.Monster = monster


class MonsterEffects:
    def __init__(self, monster):
        self.Froze = 0
        self.Fire = 0
        self.Poison = 0
        self.Electricity = 0
        self.Slowing = 5
        self.Direction = 0
        self.Citizen_annihilation = 1
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
        self.Direction = 1 if self.Monster.Lived_ticks % 7 == 6 else self.Direction

    def refresh_effects(self):
        self._effects_collecting()
        self._effects_calculation()
        self.Monster.Health -= self.Damage
        self._tick_effects_update()


class Monster:
    def __init__(self, world, x, y):
        self.World = world
        self.X = x
        self.Y = y
        self.Width = 2
        self.Height = 2
        self.Polygon = self._init_polygon()
        self.Speed = 1  # TODO  MAKE GETTER And setter
        self.Health = 1000
        self.Lived_ticks = 0
        self.Alive = True
        self.Armor = MonsterArmor(self, monster_armor1)
        self.Money = 10
        self.Texture = "MMM"
        self.Effects = MonsterEffects(self)
        self.Speed_modificator = 0
        self.InCity = False
        self.Type = "all"
        self.id = 0

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
            if self.Health < 1:  # (remember : here will be  updates param incity)
                self.Alive = False
                self.X = -1
                self.Y = -1
            if self.World.Draw_system.Draw_tick % (MAX_MONSTER_SPEED - self.Speed) == 0:  # check this
                self.move_forward(1)

    def _movement(self, x, y):
        if self.Alive:
            self.X += x
            self.Y += y

    def move_forward(self, step):
        self._movement(step, 0)

    def move_backward(self, step):
        self._movement(-step, 0)

    def move_up(self, step):
        self._movement(0, -step)

    def move_down(self, step):
        self._movement(0, step)

    def in_screen(self, window_width, window_height):
        return ((self.X >= 0) and (self.X + self.Width < window_width) and
                (self.Y >= 0) and (self.Y + self.Height < window_height)) and self.Alive

    def effect_on_tick(self):
        pass
