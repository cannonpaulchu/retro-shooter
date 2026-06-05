import pygame
import math
from settings import (PLAYER_SPEED, PLAYER_ACCEL, PLAYER_FRICTION,
                       PLAYER_HP, SHOOT_COOLDOWN,
                       INTERNAL_W, INTERNAL_H, YELLOW)
from src.entities.bullet import Bullet


def _make_player_surface():
    surf = pygame.Surface((14, 14), pygame.SRCALPHA)
    pygame.draw.rect(surf, (80, 160, 255), (2, 2, 10, 10))
    pygame.draw.rect(surf, YELLOW, (10, 5, 5, 4))
    return surf


class Player(pygame.sprite.Sprite):
    def __init__(self, pos, groups):
        super().__init__(groups)
        self._base_image = _make_player_surface()
        self.image = self._base_image.copy()
        self.rect = self.image.get_rect(center=pos)
        self.pos = pygame.math.Vector2(pos)
        self.velocity = pygame.math.Vector2(0, 0)
        self.hp = PLAYER_HP
        self.shoot_timer = 0.0
        self.invincible_timer = 0.0
        self.move_target = None

    def set_move_target(self, target_pos):
        self.move_target = pygame.math.Vector2(target_pos)

    def update(self, dt, keys, mouse_pos_internal, bullet_group, all_sprites):
        # Determine input direction
        direction = pygame.math.Vector2(0, 0)
        if keys[pygame.K_LEFT]  or keys[pygame.K_a]: direction.x -= 1
        if keys[pygame.K_RIGHT] or keys[pygame.K_d]: direction.x += 1
        if keys[pygame.K_UP]    or keys[pygame.K_w]: direction.y -= 1
        if keys[pygame.K_DOWN]  or keys[pygame.K_s]: direction.y += 1

        if direction.length() > 0:
            direction = direction.normalize()
            self.move_target = None
        elif self.move_target is not None:
            to_target = self.move_target - self.pos
            if to_target.length() > 3:
                direction = to_target.normalize()
            else:
                self.move_target = None
                self.velocity *= 0.0  # full stop on arrival

        # Accelerate toward input direction
        if direction.length() > 0:
            self.velocity += direction * PLAYER_ACCEL * dt
            # Clamp to max speed
            if self.velocity.length() > PLAYER_SPEED:
                self.velocity.scale_to_length(PLAYER_SPEED)
        else:
            # Friction — exponential decay gives a car-coast-to-stop feel
            self.velocity *= max(0.0, 1.0 - PLAYER_FRICTION * dt)
            if self.velocity.length() < 1:
                self.velocity = pygame.math.Vector2(0, 0)

        self.pos += self.velocity * dt
        self.pos.x = max(8, min(INTERNAL_W - 8, self.pos.x))
        self.pos.y = max(8, min(INTERNAL_H - 8, self.pos.y))

        # Bounce velocity off walls
        if self.pos.x <= 8 or self.pos.x >= INTERNAL_W - 8:
            self.velocity.x *= -0.3
        if self.pos.y <= 8 or self.pos.y >= INTERNAL_H - 8:
            self.velocity.y *= -0.3

        self.rect.center = (int(self.pos.x), int(self.pos.y))

        # Rotate toward mouse
        dx = mouse_pos_internal[0] - self.pos.x
        dy = mouse_pos_internal[1] - self.pos.y
        angle = -math.degrees(math.atan2(dy, dx))
        self.image = pygame.transform.rotate(self._base_image, angle)
        self.rect = self.image.get_rect(center=self.rect.center)

        # Timers
        self.shoot_timer = max(0.0, self.shoot_timer - dt)
        self.invincible_timer = max(0.0, self.invincible_timer - dt)

    def shoot(self, mouse_pos_internal, bullet_group, all_sprites):
        if self.shoot_timer > 0:
            return
        self.shoot_timer = SHOOT_COOLDOWN
        Bullet(self.rect.center, mouse_pos_internal, [bullet_group, all_sprites])

    def take_damage(self, amount):
        if self.invincible_timer > 0:
            return
        self.hp -= amount
        self.invincible_timer = 0.4

    @property
    def alive_check(self):
        return self.hp > 0
