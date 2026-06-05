import pygame
from settings import WHITE, GREEN, RED, GRAY, PLAYER_HP, BLACK


class HUD:
    def __init__(self):
        self.font = pygame.font.SysFont("monospace", 7, bold=True)

    def draw(self, surface, player, score, level_number, wave_index, total_waves):
        # HP bar background
        pygame.draw.rect(surface, GRAY,  (4, 4, 60, 6))
        hp_w = int(60 * max(0, player.hp) / PLAYER_HP)
        hp_color = GREEN if player.hp > 40 else (220, 180, 0) if player.hp > 20 else RED
        pygame.draw.rect(surface, hp_color, (4, 4, hp_w, 6))
        pygame.draw.rect(surface, WHITE, (4, 4, 60, 6), 1)

        # Score
        score_surf = self.font.render(f"SCORE:{score}", True, WHITE)
        surface.blit(score_surf, (4, 12))

        # Level / wave
        lw_surf = self.font.render(f"LVL {level_number}  W{wave_index+1}/{total_waves}", True, WHITE)
        surface.blit(lw_surf, (4, 20))
