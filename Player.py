class Player:
    def __init__(self):
        self.citizens = 22
        self.money = 200
        self.experience = 0
        self.tower_amount = 0
        self.waves_amount = 5
        self.lived_waves = 5
        self.wave_timeout = 20
        self.level = 1
        self.killed_monsters = 0
        self.monsters_loots = []
        self.alive = True
        self.strings_info = []
        self.wave_health = 0
        self.get_strings_info()

    def get_strings_info(self):
        data = []
        data.append("MONEY: " + str(self.money))
        data.append("EXP: " + str(self.experience))
        data.append("CITIZENS: " + str(self.citizens))
        data.append("LEVEL: " + str(self.level))
        data.append("TOWERS: " + str(self.tower_amount))
        data.append("WAVE HEALTH: " + str(self.wave_health))
        self.strings_info = data

    def refresh(self):
        for loot in self.monsters_loots:
            if loot.available:
                if loot.in_city:
                    self.citizens -= loot.citizen_annihilation
                    if self.citizens <= 0:
                        self.alive = False
                self.money += loot.money
                self.experience += loot.experience
                loot.available = False

        self.monsters_loots = []
        self.get_strings_info()
