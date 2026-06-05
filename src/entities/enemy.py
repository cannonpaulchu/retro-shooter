import pygame
import math
import random
from settings import INTERNAL_W, INTERNAL_H, RED, ORANGE, BULLET_DAMAGE


def _spawn_pos():
    edge = random.randint(0, 3)
    if edge == 0:   return (random.randint(0, INTERNAL_W), -12)
    elif edge == 1: return (random.randint(0, INTERNAL_W), INTERNAL_H + 12)
    elif edge == 2: return (-12, random.randint(0, INTERNAL_H))
    else:           return (INTERNAL_W + 12, random.randint(0, INTERNAL_H))


class Enemy(pygame.sprite.Sprite):
    speed  = 40
    hp     = 50
    color  = RED
    size   = 10
    score  = 10

    def __init__(self, groups):
        super().__init__(groups)
        self.image = pygame.Surface((self.size * 2, self.size * 2), pygame.SRCALPHA)
        self._draw_shape()
        self.rect = self.image.get_rect(center=_spawn_pos())
        self.pos = pygame.math.Vector2(self.rect.center)
        self._orbit_angle = random.uniform(0, math.pi * 2)

    def _draw_shape(self):
        raise NotImplementedError

    def update(self, dt, player_pos):
        self._move(dt, player_pos)
        self.rect.center = (int(self.pos.x), int(self.pos.y))

    def _move(self, dt, player_pos):
        direction = pygame.math.Vector2(player_pos) - self.pos
        if direction.length() > 0:
            direction = direction.normalize()
        self.pos += direction * self.speed * dt

    def take_damage(self, amount):
        self.hp -= amount
        if self.hp <= 0:
            self.kill()
            return True
        return False


class BasicEnemy(Enemy):
    speed = 45
    hp    = 50
    color = (220, 60, 60)
    size  = 6
    score = 10

    def _draw_shape(self):
        pygame.draw.circle(self.image, self.color,
                           (self.size, self.size), self.size)
        pygame.draw.circle(self.image, (255, 100, 100),
                           (self.size, self.size), self.size - 2, 2)


class StraferEnemy(Enemy):
    speed = 55
    hp    = 40
    color = (230, 140, 30)
    size  = 6
    score = 20

    def _draw_shape(self):
        s = self.size
        pts = [(s, 0), (s*2, s), (s, s*2), (0, s)]
        pygame.draw.polygon(self.image, self.color, pts)
        pygame.draw.polygon(self.image, (255, 180, 80), pts, 2)

    def _move(self, dt, player_pos):
        target = pygame.math.Vector2(player_pos)
        to_player = target - self.pos
        dist = to_player.length()
        if dist > 0:
            toward = to_player.normalize()
        else:
            toward = pygame.math.Vector2(1, 0)
        self._orbit_angle += 2.5 * dt
        strafe = pygame.math.Vector2(math.cos(self._orbit_angle),
                                      math.sin(self._orbit_angle))
        move = (toward * 0.7 + strafe * 0.5).normalize()
        self.pos += move * self.speed * dt


class TankEnemy(Enemy):
    speed = 22
    hp    = 200
    color = (80, 180, 80)
    size  = 10
    score = 50

    def _draw_shape(self):
        s = self.size * 2
        pygame.draw.rect(self.image, self.color, (2, 2, s - 4, s - 4))
        pygame.draw.rect(self.image, (120, 220, 120), (2, 2, s - 4, s - 4), 2)


ENEMY_TYPES = {
    "basic":   BasicEnemy,
    "strafer": StraferEnemy,
    "tank":    TankEnemy,
}
