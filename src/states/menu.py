import pygame
from settings import INTERNAL_W, INTERNAL_H, WHITE, YELLOW, DARK, GREEN


class MenuState:
    def __init__(self):
        self.font_big  = pygame.font.SysFont("monospace", 16, bold=True)
        self.font_small= pygame.font.SysFont("monospace", 7, bold=True)
        self.blink_timer = 0.0
        self.show_prompt = True

    def handle_events(self, events):
        for event in events:
            if event.type == pygame.KEYDOWN and event.key == pygame.K_RETURN:
                return "playing"
            if event.type == pygame.MOUSEBUTTONDOWN:
                return "playing"
        return None

    def update(self, dt):
        self.blink_timer += dt
        if self.blink_timer > 0.55:
            self.show_prompt = not self.show_prompt
            self.blink_timer = 0.0

    def draw(self, surface):
        surface.fill(DARK)

        # Title
        title = self.font_big.render("RETRO SHOOTER", True, YELLOW)
        surface.blit(title, (INTERNAL_W // 2 - title.get_width() // 2, 60))

        # Subtitle decoration
        line_y = 80
        pygame.draw.line(surface, YELLOW, (20, line_y), (INTERNAL_W - 20, line_y), 1)

        # Controls hint
        lines = [
            "ARROW KEYS : MOVE",
            "MOUSE      : AIM",
            "CLICK      : SHOOT",
        ]
        for i, line in enumerate(lines):
            s = self.font_small.render(line, True, WHITE)
            surface.blit(s, (INTERNAL_W // 2 - s.get_width() // 2, 100 + i * 12))

        # Prompt
        if self.show_prompt:
            prompt = self.font_small.render("PRESS ENTER OR CLICK TO START", True, GREEN)
            surface.blit(prompt, (INTERNAL_W // 2 - prompt.get_width() // 2, 160))
