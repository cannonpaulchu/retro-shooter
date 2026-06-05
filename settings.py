import pygame

# Display
INTERNAL_W, INTERNAL_H = 320, 240
SCALE = 3
SCREEN_W, SCREEN_H = INTERNAL_W * SCALE, INTERNAL_H * SCALE
FPS = 60
TITLE = "RetroShooter"

# Colors
BLACK   = (0, 0, 0)
WHITE   = (255, 255, 255)
GREEN   = (80, 220, 80)
RED     = (220, 60, 60)
YELLOW  = (255, 220, 0)
ORANGE  = (230, 140, 30)
BLUE    = (60, 120, 220)
GRAY    = (120, 120, 120)
DARK    = (15, 15, 30)

# Player
PLAYER_SPEED    = 90   # pixels/sec at internal res
PLAYER_HP       = 100
BULLET_SPEED    = 220
BULLET_DAMAGE   = 25
SHOOT_COOLDOWN  = 0.25  # seconds

# Enemies
ENEMY_DAMAGE    = 10   # HP lost on contact per second

# Levels
LEVELS = [
    {
        "number": 1,
        "bg": (18, 18, 38),
        "waves": [
            {"count": 5, "type": "basic", "spawn_delay": 1.2},
            {"count": 7, "type": "basic", "spawn_delay": 0.9},
        ],
    },
    {
        "number": 2,
        "bg": (30, 12, 12),
        "waves": [
            {"count": 5, "type": "basic",   "spawn_delay": 0.8},
            {"count": 4, "type": "strafer", "spawn_delay": 1.2},
            {"count": 6, "type": "basic",   "spawn_delay": 0.6},
        ],
    },
    {
        "number": 3,
        "bg": (10, 28, 14),
        "waves": [
            {"count": 6, "type": "basic",   "spawn_delay": 0.6},
            {"count": 4, "type": "strafer", "spawn_delay": 0.9},
            {"count": 2, "type": "tank",    "spawn_delay": 2.0},
            {"count": 4, "type": "strafer", "spawn_delay": 0.8},
        ],
    },
    {
        "number": 4,
        "bg": (28, 14, 28),
        "waves": [
            {"count": 8, "type": "basic",   "spawn_delay": 0.5},
            {"count": 5, "type": "strafer", "spawn_delay": 0.7},
            {"count": 3, "type": "tank",    "spawn_delay": 1.5},
            {"count": 6, "type": "strafer", "spawn_delay": 0.6},
            {"count": 3, "type": "tank",    "spawn_delay": 1.5},
        ],
    },
]
