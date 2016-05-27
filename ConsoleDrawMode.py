import time
import GameWorld as Game


class DrawWorldConsole:
    def __init__(self, width, height):
        self.Width = width
        self.Height = height
        self.Game = Game.GameWorld(width, height)
        self.Game_map = self.Game.Game_map
        self.tick_update_()

    def tick_update_(self):
        while True:
            self.Game.refresh_world()
            self.Game_map = self.Game.Game_map
            self.display_map()
            time.sleep(1)

    def display_map(self):  # TODO rewrite this with using sys  and draw objects like a progress bars
        for x in range(0, self.Width):
            print('+' + '---+' * self.Width)
            print('|', sep='', end='')
            for y in range(0, self.Height):
                if len(self.Game_map[x][y]) == 1:
                    print(" " + self.Game_map[x][y] + " ", end='|')
                elif len(self.Game_map[x][y]) == 2:
                    print(" " + self.Game_map[x][y], end='|')
                else:
                    print(self.Game_map[x][y][0:3], end='|')

            print()
        print('+' + '---+' * self.Width)

a = DrawWorldConsole(25, 25)
