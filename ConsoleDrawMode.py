import time
import GameWorld as Game


class DrawWorldConsole:
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.Game = Game.GameWorld(width, height)
        self.game_map = self.Game.game_map
        self.tick_update_()

    def tick_update_(self):
        while True:
            self.Game.refresh_world()
            self.game_map = self.Game.game_map
            self.display_map()
            time.sleep(1)

    def display_map(self):  # TODO rewrite this with using sys  and draw objects like a progress bars
        for x in range(0, self.width):
            print('+' + '---+' * self.width)
            print('|', sep='', end='')
            for y in range(0, self.height):
                if len(self.game_map[x][y]) == 1:
                    print(" " + self.game_map[x][y] + " ", end='|')
                elif len(self.game_map[x][y]) == 2:
                    print(" " + self.game_map[x][y], end='|')
                else:
                    print(self.game_map[x][y][0:3], end='|')

            print()
        print('+' + '---+' * self.width)

a = DrawWorldConsole(25, 25)
