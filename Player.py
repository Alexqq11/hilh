class Player:
    def __init__(self):
        self.Citizens = 22
        self.Money = 200
        self.Experience = 0
        self.Tower_amount = 0
        self.Waves_amount = 5
        self.Lived_waves = 5
        self.Wave_timeout = 20
        self.Level = 1
        self.Killed_monsters = 0
        self.Monsters_loots = []
        self.Alive = True

    def refresh(self):
        for loot in self.Monsters_loots:
            if loot.In_city:
                self.Citizens -= loot.Citizen_annihilation
                if self.Citizens <= 0:
                    self.Alive = False
            self.Money += loot.Money
            self.Experience += loot.Experience
