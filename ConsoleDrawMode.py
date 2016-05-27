import time
import GameWorld as Game


class DrawWorldConsole:
    def __init__(self, width, height):
        self.Width = width
        self.Height = height
        self._Game = Game.GameWorld(self, width, height)
        self._Game_map = self._Game.Game_map
        self.Draw_tick = 0
        self.WorldSpeed = 1
        self.tick_update_()

    def tick_update_(self):  # TODO make normal timer that works with world ? search about qt  timers
        while True:
            self._Game.refresh_world()
            self._Game_map = self._Game.Game_map
            self.display_map()
            self.Draw_tick += 1
            time.sleep(0.07)  # TODO world speed generation

    def display_map(self):  # TODO rewrite this with using sys  and draw objects like a progress bars
        for x in range(0, self.Width):
            print('+' + '---+' * self.Width)
            print('|', sep='', end='')
            for y in range(0, self.Height):
                if len(self._Game_map[x][y]) == 1:
                    print(" " + self._Game_map[x][y] + " ", end='|')
                elif len(self._Game_map[x][y]) == 2:
                    print(" " + self._Game_map[x][y], end='|')
                else:
                    print(self._Game_map[x][y][0:3], end='|')

            print()
        print('+' + '---+' * self.Width)

a = DrawWorldConsole(25, 25)
