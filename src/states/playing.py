import pygame
from settings import INTERNAL_W, INTERNAL_H, SCALE, WHITE, ENEMY_DAMAGE, LEVELS
from src.entities.player import Player
from src.level import LevelManager
from src.hud import HUD


class PlayingState:
    def __init__(self, level_index=0):
        self.all_sprites   = pygame.sprite.Group()
        self.enemy_group   = pygame.sprite.Group()
        self.bullet_group  = pygame.sprite.Group()
        self.player_group  = pygame.sprite.GroupSingle()

        cx, cy = INTERNAL_W // 2, INTERNAL_H // 2
        self.player = Player((cx, cy), [self.all_sprites, self.player_group])

        self.level_manager = LevelManager()
        self.level_manager.level_index = level_index
        self.level_manager._load_wave()

        self.score = 0
        self.hud   = HUD()

        self.level_clear_timer = 0.0  # pause before advancing level
        self.showing_clear     = False
        self.font_mid = pygame.font.SysFont("monospace", 10, bold=True)

    def handle_events(self, events):
        for event in events:
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                mp = pygame.math.Vector2(pygame.mouse.get_pos()) / SCALE
                self.player.shoot(mp, self.bullet_group, self.all_sprites)
        return None

    def update(self, dt):
        keys = pygame.key.get_pressed()
        mp   = pygame.math.Vector2(pygame.mouse.get_pos()) / SCALE

        # Shoot on held mouse button
        if pygame.mouse.get_pressed()[0]:
            self.player.shoot(mp, self.bullet_group, self.all_sprites)

        self.player.update(dt, keys, mp, self.bullet_group, self.all_sprites)
        self.bullet_group.update(dt)

        # Update enemies — pass player pos
        for enemy in self.enemy_group:
            enemy.update(dt, self.player.pos)

        # Bullet-enemy collisions
        hits = pygame.sprite.groupcollide(self.bullet_group, self.enemy_group,
                                          True, False)
        for bullet, enemies in hits.items():
            for enemy in enemies:
                enemy.take_damage(25)
                self.score += enemy.score

        # Player-enemy collisions
        if self.player.invincible_timer <= 0:
            contacts = pygame.sprite.spritecollide(self.player, self.enemy_group,
                                                   False,
                                                   pygame.sprite.collide_circle_ratio(0.7))
            if contacts:
                self.player.take_damage(ENEMY_DAMAGE)

        # Level progression
        if self.showing_clear:
            self.level_clear_timer -= dt
            if self.level_clear_timer <= 0:
                self.showing_clear = False
                if self.level_manager.is_last_level:
                    return "won"
                self.level_manager.next_level()
                for e in self.enemy_group:
                    e.kill()
        else:
            self.level_manager.update(dt, self.enemy_group,
                                      self.all_sprites, self.enemy_group)
            if self.level_manager.level_done:
                self.showing_clear    = True
                self.level_clear_timer = 2.5

        # Death
        if self.player.hp <= 0:
            return "dead"

        return None

    def draw(self, surface):
        surface.fill(self.level_manager.bg_color)
        self.all_sprites.draw(surface)

        if self.showing_clear:
            msg = self.font_mid.render("LEVEL CLEAR!", True, (255, 220, 0))
            surface.blit(msg, (INTERNAL_W // 2 - msg.get_width() // 2,
                               INTERNAL_H // 2 - 10))

        total_waves = len(LEVELS[self.level_manager.level_index]["waves"])
        self.hud.draw(surface, self.player, self.score,
                      self.level_manager.level_number,
                      self.level_manager.wave_index,
                      total_waves)
