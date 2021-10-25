from pynput import keyboard
import pygame
import random


class LeonardsGame:
    def __init__(self):
        pygame.init()
        pygame.display.set_caption("Leonard's Super Hard Game")
        displ_info = pygame.display.Info()
        self.screen = pygame.display.set_mode((displ_info.current_w, displ_info.current_h))
        self.change_colors()
        self.prev_key = None
        self.lst = keyboard.Listener(on_press=self._update_colors)
        self.lst.start()

    def _update_colors(self, key):
        if self.prev_key == key and key == keyboard.Key.esc:
            self.lst.stop()
            pygame.quit()
        if self.prev_key == key:
            pygame.display.flip()
            return
        self.prev_key = key
        self.change_colors()

    @staticmethod
    def _get_random_colors() -> tuple:
        return tuple(color for color in [random.randint(0, 255) for _ in range(0, 3)])

    def start(self):
        while True:
            event = pygame.event.poll()

            if event.type == pygame.QUIT:
                self.lst.stop()
                pygame.quit()

    def change_colors(self):
        colors = self._get_random_colors()
        self.screen.fill(colors)
        pygame.display.flip()


if __name__ == "__main__":
    lenny_game = LeonardsGame()
    lenny_game.start()
