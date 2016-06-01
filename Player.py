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
        self.strings_info = []
        self.wave_health = 0
        self.get_strings_info()


    def get_strings_info(self):
        data = list()
        data.append("MONEY: " + str(self.Money))
        data.append("EXP: " + str(self.Experience))
        data.append("CITIZENS: " + str(self.Citizens))
        data.append("LEVEL: " + str(self.Level))
        data.append("TOWERS: " + str(self.Tower_amount))
        data.append("WAVE HEALTH: " + str(self.wave_health))
        self.strings_info = data

    def refresh(self):
        for loot in self.Monsters_loots:
            if loot.Avalible:
                if loot.In_city:
                    self.Citizens -= loot.Citizen_annihilation
                    if self.Citizens <= 0:
                        self.Alive = False
                self.Money += loot.Money
                self.Experience += loot.Experience
                loot.Avalible = False

        self.Monsters_loots = []
        self.get_strings_info()
