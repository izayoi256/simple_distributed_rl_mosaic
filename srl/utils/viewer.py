from typing import Tuple

import numpy as np

try:
    import pygame
except ImportError:
    pass


class Viewer:
    def __init__(self, width: int, height: int, fps: int = 30):
        self.width = width
        self.height = height
        self.fps = fps

        pygame.init()
        self.clock = pygame.time.Clock()
        self.screen = pygame.display.set_mode((self.width, self.height))
        self.fonts = {}

    def __del__(self):
        self.close()

    def close(self):
        pygame.quit()

    def registration_font(self, name: str, font: str = "arial", fontsize: int = 22):
        self.fonts[name] = pygame.font.SysFont(font, fontsize)

    def draw_start(self, color: Tuple[int, int, int] = (255, 255, 255)):
        self.screen.fill(color)

        # event
        # for event in pygame.event.get():
        #    pass

    def draw_end(self):
        pygame.display.flip()
        self.clock.tick(self.fps)

    def get_rgb_array(self) -> np.ndarray:
        return np.transpose(
            np.array(pygame.surfarray.pixels3d(self.screen)), axes=(1, 0, 2)
        )

    # --------------------
    def draw_line(
        self,
        x1: int,
        y1: int,
        x2: int,
        y2: int,
        color: Tuple[int, int, int] = (0, 0, 0),
        width: int = 1,
    ):
        pygame.draw.line(self.screen, color, (x1, y1), (x2, y2), width=width)

    def draw_box(
        self,
        x: int,
        y: int,
        w: int,
        h: int,
        color: Tuple[int, int, int],
        filled: bool = True,
        width: int = 1,
    ):
        if filled:
            self.screen.fill(color, (x, y, w, h))
        else:
            lines = [
                (x, y),
                (x, y + h),
                (x + w, y + h),
                (x + w, y),
                (x, y),
            ]
            pygame.draw.lines(self.screen, color, False, lines, width=width)

    def draw_circle(
        self,
        x: int,
        y: int,
        radius: int,
        color: Tuple[int, int, int],
        filled: bool = False,
        width: int = 1,
    ):
        if filled:
            width = 0
        pygame.draw.circle(self.screen, color, (x, y), radius, width=width)

    def draw_text(self, x, y, text, fontname: str = "", color=(0, 0, 0)):
        if fontname not in self.fonts:
            if fontname == "":
                self.fonts[""] = pygame.font.SysFont("arial", 22)
            else:
                raise ValueError()
        font = self.fonts[fontname]
        self.screen.blit(font.render(text, False, color), (x, y))