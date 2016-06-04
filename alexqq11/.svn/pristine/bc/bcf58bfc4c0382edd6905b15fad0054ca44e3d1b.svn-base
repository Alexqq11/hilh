import time
import GameWorld as Game


class DrawWorldConsole:
    def __init__(self, width, height, world_speed):
        self.width = width
        self.height = height
        self._game = Game.GameWorld(self, width, height)
        self._game_map = self._game.game_map
        self.draw_tick = 0
        self.world_speed = world_speed * 0.07
        self.tick_update_()

    def tick_update_(self):
        while True:
            self._game.refresh_world()
            self._game_map = self._game.game_map
            self.display_map()
            self.draw_tick += 1
            self.draw_tick %= 1000
            time.sleep(self.world_speed)

    def display_map(self):
        for y in range(0, self.height):
            print('+' + '---+' * self.width)
            print('|', sep='', end='')
            for x in range(0, self.width):
                if len(self._game_map[y][x]) == 1:
                    print(" " + self._game_map[y][x] + " ", end='|')
                elif len(self._game_map[y][x]) == 2:
                    print(" " + self._game_map[y][x], end='|')
                else:
                    print(self._game_map[y][x][0:3], end='|')

            print()
        print('+' + '---+' * self.width)


a = DrawWorldConsole(128, 43, 1)
