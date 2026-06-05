import pygame
import math
from settings import BULLET_SPEED, YELLOW, INTERNAL_W, INTERNAL_H


class Bullet(pygame.sprite.Sprite):
    def __init__(self, pos, target_pos, groups):
        super().__init__(groups)
        self.image = pygame.Surface((4, 4), pygame.SRCALPHA)
        pygame.draw.rect(self.image, YELLOW, (0, 0, 4, 4))
        self.rect = self.image.get_rect(center=pos)
        self.pos = pygame.math.Vector2(pos)

        direction = pygame.math.Vector2(target_pos) - self.pos
        if direction.length() > 0:
            direction = direction.normalize()
        self.velocity = direction * BULLET_SPEED

    def update(self, dt):
        self.pos += self.velocity * dt
        self.rect.center = (int(self.pos.x), int(self.pos.y))
        if (self.pos.x < -10 or self.pos.x > INTERNAL_W + 10 or
                self.pos.y < -10 or self.pos.y > INTERNAL_H + 10):
            self.kill()
