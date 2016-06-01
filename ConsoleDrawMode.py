import time
import GameWorld as Game


class DrawWorldConsole:
    def __init__(self, width, height, world_speed):
        self.Width = width
        self.Height = height
        self._Game = Game.GameWorld(self, width, height)
        self._Game_map = self._Game.Game_map
        self.Draw_tick = 0
        self.World_speed = world_speed * 0.07
        self.tick_update_()

    def tick_update_(self):
        while True:
            self._Game.refresh_world()
            self._Game_map = self._Game.Game_map
            self.display_map()
            self.Draw_tick += 1
            self.Draw_tick %= 1000
            time.sleep(self.World_speed)

    def display_map(self):
        for y in range(0, self.Height):
            print('+' + '---+' * self.Width)
            print('|', sep='', end='')
            for x in range(0, self.Width):
                if len(self._Game_map[y][x]) == 1:
                    print(" " + self._Game_map[y][x] + " ", end='|')
                elif len(self._Game_map[y][x]) == 2:
                    print(" " + self._Game_map[y][x], end='|')
                else:
                    print(self._Game_map[y][x][0:3], end='|')

            print()
        print('+' + '---+' * self.Width)

a = DrawWorldConsole(128, 43, 1)
