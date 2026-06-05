from settings import LEVELS
from src.entities.enemy import ENEMY_TYPES


class LevelManager:
    def __init__(self):
        self.level_index = 0
        self.wave_index  = 0
        self.spawn_timer = 0.0
        self.to_spawn    = 0
        self.wave_done   = False
        self.level_done  = False
        self._load_wave()

    def _load_wave(self):
        wave = self._current_wave()
        self.to_spawn  = wave["count"]
        self.spawn_timer = 0.0
        self.wave_done = False

    def _current_level(self):
        return LEVELS[self.level_index]

    def _current_wave(self):
        return self._current_level()["waves"][self.wave_index]

    @property
    def bg_color(self):
        return self._current_level()["bg"]

    @property
    def level_number(self):
        return self._current_level()["number"]

    @property
    def is_last_level(self):
        return self.level_index >= len(LEVELS) - 1

    def update(self, dt, enemy_group, all_sprites, active_enemies):
        if self.wave_done:
            return

        wave = self._current_wave()
        self.spawn_timer -= dt

        if self.to_spawn > 0 and self.spawn_timer <= 0:
            cls = ENEMY_TYPES[wave["type"]]
            cls([enemy_group, all_sprites])
            self.to_spawn -= 1
            self.spawn_timer = wave["spawn_delay"]

        if self.to_spawn == 0 and len(active_enemies) == 0:
            self.wave_done = True
            self._advance()

    def _advance(self):
        level = self._current_level()
        if self.wave_index < len(level["waves"]) - 1:
            self.wave_index += 1
            self._load_wave()
        else:
            self.level_done = True

    def next_level(self):
        if self.level_index < len(LEVELS) - 1:
            self.level_index += 1
            self.wave_index  = 0
            self.level_done  = False
            self._load_wave()

    def reset(self):
        self.level_index = 0
        self.wave_index  = 0
        self.level_done  = False
        self._load_wave()
