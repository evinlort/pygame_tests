from typing import Tuple

from pynput import keyboard
import pygame
import random


class LeonardGame:
    def __init__(self):
        pygame.init()
        pygame.display.set_caption("Leonard's Super Hard Game")
        display_info = pygame.display.Info()
        self.X, self.Y = display_info.current_w, display_info.current_h
        self.screen = pygame.display.set_mode((self.X, self.Y))
        self.change_colors()
        self.prev_key = None
        self.font = pygame.font.Font('freesansbold.ttf', 128)
        self.lst = keyboard.Listener(on_press=self._update_colors)
        self.lst.start()

    def start(self):
        while True:
            event = pygame.event.poll()
            if event.type == pygame.QUIT:
                self.stop_game()

    def _update_colors(self, key):
        if self.prev_key == key and key == keyboard.Key.esc:
            self.stop_game()
        if self.prev_key == key:
            pygame.display.flip()
            return

        if len(str(key).strip("'")) > 1:
            self.change_colors()
        elif 33 <= ord(str(key).strip("'")) <= 126:
            self.change_colors()
            self.show_letter(key)
        self.prev_key = key


    @staticmethod
    def _get_random_colors() -> Tuple[int, int, int]:
        return random.randint(0, 255), random.randint(0, 255), random.randint(0, 255)

    def change_colors(self):
        colors = self._get_random_colors()
        self.screen.fill(colors)
        pygame.display.flip()

    def show_letter(self, char: str):
        text = self.font.render(str(char).strip("'").upper(), True, self._get_random_colors(), (0, 0, 0))
        textRect = text.get_rect()
        textRect.center = (self.X // 2, self.Y // 2)
        self.screen.blit(text, textRect)
        pygame.display.update()

    def stop_game(self):
        self.lst.stop()
        pygame.quit()


if __name__ == "__main__":
    lenny_game = LeonardGame()
    lenny_game.start()
