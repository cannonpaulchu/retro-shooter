import pygame
from settings import INTERNAL_W, INTERNAL_H, WHITE, RED, YELLOW, DARK, GREEN


class GameOverState:
    def __init__(self, score, won=False):
        self.score = score
        self.won   = won
        self.font_big   = pygame.font.SysFont("monospace", 16, bold=True)
        self.font_small = pygame.font.SysFont("monospace", 7, bold=True)
        self.blink_timer = 0.0
        self.show_prompt = True

    def handle_events(self, events):
        for event in events:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    return "menu"
                if event.key == pygame.K_r:
                    return "playing"
            if event.type == pygame.MOUSEBUTTONDOWN:
                return "menu"
        return None

    def update(self, dt):
        self.blink_timer += dt
        if self.blink_timer > 0.55:
            self.show_prompt = not self.show_prompt
            self.blink_timer = 0.0

    def draw(self, surface):
        surface.fill(DARK)
        if self.won:
            header = self.font_big.render("YOU WIN!", True, YELLOW)
        else:
            header = self.font_big.render("GAME OVER", True, RED)
        surface.blit(header, (INTERNAL_W // 2 - header.get_width() // 2, 70))

        score_s = self.font_small.render(f"SCORE: {self.score}", True, WHITE)
        surface.blit(score_s, (INTERNAL_W // 2 - score_s.get_width() // 2, 110))

        if self.show_prompt:
            p1 = self.font_small.render("ENTER / CLICK : MENU", True, GREEN)
            p2 = self.font_small.render("R             : RETRY", True, GREEN)
            surface.blit(p1, (INTERNAL_W // 2 - p1.get_width() // 2, 140))
            surface.blit(p2, (INTERNAL_W // 2 - p2.get_width() // 2, 154))
