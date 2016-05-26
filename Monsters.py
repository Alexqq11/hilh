import sympy.geometry as g

monster_armor1 = {"Froze": 0, "Fire": 0, "Poison": 0, "Electricity": 0, "Physical": 0}


class MonsterArmor:
    def __init__(self, monster_armor):
        self.Froze = monster_armor["Froze"]
        self.Fire = monster_armor["Fire"]
        self.Poison = monster_armor["Poison"]
        self.Electricity = monster_armor["Electricity"]
        self.Physical = monster_armor["Physical"]


class MonsterEffects:
    def __init__(self):
        self.Frozen = 0
        self.Fired = 0
        self.Poisoned = 0
        self.Electricity = 0
        self.Slowing = 5
        self.Direction = 0
        self.Cityzen_Anigilation = 1


class Monster:
    def __init__(self, x, y):
        self.X = x
        self.Y = y
        self.Width = 2
        self.Height = 2
        self.Polygon = self._init_polygon()
        self.Speed = 1
        self.Health = 10
        self.Alive = True
        self.Armor = MonsterArmor(monster_armor1)
        self.Money = 10
        self.Texture = "MMM"
        self.EffectsList = MonsterEffects()
        self.speed_modificator = 0
        self.InCity = False
        self.Type = "all"
        self.id = 0

    def is_can_be_attacked(self, typeof):
        return (typeof == "all" or typeof == self.Type) and self.Alive

    def _init_polygon(self):
        x = self.X
        y = self.Y
        w = self.Width
        h = self.Height
        return g.polygon.Polygon(g.Point(x, y), g.Point(x + w, y), g.Point(x + w, y + h), g.Point(x, y + h))

    def refresh(self):
        if self.Alive:
            self.Polygon = self._init_polygon()                 # TODO write full effects for monster over time (remember : here will be  updates param incity)
            if self.Health < 1:
                self.Alive = False
                self.X = -1
                self.Y = -1
    """
    def death
    def update(self):
        i
    """
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
