import pygame
import random
import math
import time

pygame.init()

WIDTH, HEIGHT = 960, 720
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("TypeBlast — Type Faster!")
clock = pygame.time.Clock()

FONT_WORD = pygame.font.SysFont("monospace", 26, bold=True)
FONT_HUD = pygame.font.SysFont("monospace", 20, bold=True)
FONT_BIG = pygame.font.SysFont("monospace", 52, bold=True)
FONT_SMALL = pygame.font.SysFont("monospace", 16, bold=True)

NEON_COLORS = [
    (255, 80, 80),   # red
    (255, 180, 0),   # yellow
    (80, 255, 120),  # green
    (80, 200, 255),  # cyan
    (200, 80, 255),  # purple
    (255, 120, 200), # pink
    (255, 140, 40),  # orange
]

BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GREEN = (80, 255, 120)
DARK_GREEN = (40, 180, 70)
GRAY = (100, 100, 120)
DARK = (10, 10, 20)

WORDS_L1 = ["cat","dog","run","fly","big","top","sun","hot","cup","map","box","zip","win","key","log","ask","sit","fix","cut","dig","pop","mix","tip","row","nap","tow","pit","sew","hem","jot"]
WORDS_L2 = ["flame","blast","quick","ghost","storm","plant","creek","fence","sword","brick","glass","crowd","scale","bench","grove","chess","trick","frost","clamp","flask","drill","grasp","cloth","swing","brisk","stump","crane","scout","proud","blaze"]
WORDS_L3 = ["courage","monster","captain","kingdom","thunder","dolphin","whisper","blanket","factory","current","balance","curtain","dynamic","element","fiction","genuine","harvest","journey","machine","network"]
WORDS_L4 = ["function","keyboard","variable","password","internet","describe","favorite","movement","pleasant","computer","absolute","practice","birthday","increase","aughter","consider","neighbor","language","thousand","together","probably","yourself","complete","position","remember","question","straight","standing","decision","possible"]
WORDS_PROG = ["python","pygame","render","screen","sprite","vector","buffer","shader","lambda","cursor","server","client","output","widget","module","method","import","return","define","struct","object","string","binary","matrix","tensor","deploy","format","encode","kernel","packet"]

WORD_POOL = [WORDS_L1, WORDS_L2, WORDS_L3, WORDS_L4 + WORDS_PROG]

WORDS_PER_LEVEL = 15
BASE_SPEED = 55
SPEED_INCREMENT = 18
MAX_WORDS_ON_SCREEN = 6
SPAWN_INTERVAL_BASE = 2.2


class Star:
    def __init__(self):
        self.reset(random.randint(0, HEIGHT))

    def reset(self, y=0):
        self.x = random.randint(0, WIDTH)
        self.y = y
        self.speed = random.uniform(15, 60)
        self.size = random.randint(1, 3)
        self.brightness = random.randint(80, 200)

    def update(self, dt):
        self.y += self.speed * dt
        if self.y > HEIGHT:
            self.reset()

    def draw(self, surf):
        c = self.brightness
        pygame.draw.circle(surf, (c, c, c), (int(self.x), int(self.y)), self.size)


class Particle:
    def __init__(self, x, y, color):
        angle = random.uniform(0, math.tau)
        speed = random.uniform(60, 280)
        self.x = x
        self.y = y
        self.vx = math.cos(angle) * speed
        self.vy = math.sin(angle) * speed
        self.color = color
        self.life = random.uniform(0.4, 0.9)
        self.max_life = self.life
        self.size = random.randint(2, 6)

    def update(self, dt):
        self.x += self.vx * dt
        self.y += self.vy * dt
        self.vy += 200 * dt  # gravity
        self.life -= dt
        return self.life > 0

    def draw(self, surf):
        alpha = self.life / self.max_life
        r = max(1, int(self.size * alpha))
        c = tuple(int(ch * alpha) for ch in self.color)
        pygame.draw.circle(surf, c, (int(self.x), int(self.y)), r)


class FallingWord:
    def __init__(self, text, speed, color):
        self.text = text
        self.speed = speed
        self.color = color
        self.typed_index = 0
        self.active = True
        w = FONT_WORD.size(text)[0]
        self.x = random.randint(30, WIDTH - w - 30)
        self.y = -30
        self.wobble = random.uniform(0, math.tau)
        self.wobble_amp = random.uniform(0, 18)

    def update(self, dt):
        self.y += self.speed * dt
        self.wobble += dt * 1.5

    def draw(self, surf, is_target):
        x = self.x + math.sin(self.wobble) * self.wobble_amp
        # glow behind if targeted
        if is_target:
            glow = FONT_WORD.render(self.text, True, (255, 255, 255))
            for ox, oy in [(-2,0),(2,0),(0,-2),(0,2)]:
                surf.blit(glow, (x + ox, self.y + oy))
        # typed portion (green)
        typed_text = self.text[:self.typed_index]
        remaining_text = self.text[self.typed_index:]
        tx = x
        if typed_text:
            s = FONT_WORD.render(typed_text, True, GREEN)
            surf.blit(s, (tx, self.y))
            tx += FONT_WORD.size(typed_text)[0]
        if remaining_text:
            s = FONT_WORD.render(remaining_text, True, self.color)
            surf.blit(s, (tx, self.y))

    @property
    def bottom(self):
        return self.y + 30


class ScoreFlash:
    def __init__(self, x, y, text, color):
        self.x = x
        self.y = y
        self.text = text
        self.color = color
        self.life = 0.8

    def update(self, dt):
        self.y -= 60 * dt
        self.life -= dt
        return self.life > 0

    def draw(self, surf):
        alpha = self.life / 0.8
        c = tuple(min(255, int(ch * alpha)) for ch in self.color)
        s = FONT_HUD.render(self.text, True, c)
        surf.blit(s, (self.x, self.y))


class LevelBanner:
    def __init__(self, level):
        self.text = f"LEVEL {level}!"
        self.life = 1.8

    def update(self, dt):
        self.life -= dt
        return self.life > 0

    def draw(self, surf):
        alpha = min(1.0, self.life / 0.4) * min(1.0, (self.life) / 0.3 if self.life < 0.3 else 1.0)
        scale = 1.0 + 0.3 * max(0, 1.0 - self.life / 0.5)
        font_size = int(52 * scale)
        try:
            f = pygame.font.SysFont("monospace", font_size, bold=True)
        except Exception:
            f = FONT_BIG
        s = f.render(self.text, True, (255, 220, 50))
        r = s.get_rect(center=(WIDTH // 2, HEIGHT // 2))
        # dark overlay
        overlay = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, int(120 * alpha)))
        surf.blit(overlay, (0, 0))
        surf.blit(s, r)


class TypeBlast:
    def __init__(self):
        self.state = "menu"
        self.stars = [Star() for _ in range(120)]
        self.reset_game()

    def reset_game(self):
        self.words = []
        self.particles = []
        self.flashes = []
        self.banners = []
        self.score = 0
        self.lives = 3
        self.level = 1
        self.combo = 0
        self.max_combo = 0
        self.words_destroyed = 0
        self.total_chars = 0
        self.wpm = 0
        self.wpm_times = []  # list of (chars, elapsed_time) tuples
        self.target_word = None
        self.current_input = ""
        self.spawn_timer = 0
        self.spawn_interval = SPAWN_INTERVAL_BASE
        self.word_speed = BASE_SPEED
        self.game_start_time = time.time()
        self.last_word_time = time.time()

    def get_word_pool(self):
        idx = min(self.level - 1, len(WORD_POOL) - 1)
        return WORD_POOL[idx]

    def spawn_word(self):
        if len(self.words) >= MAX_WORDS_ON_SCREEN:
            return
        pool = self.get_word_pool()
        existing = {w.text for w in self.words}
        candidates = [w for w in pool if w not in existing]
        if not candidates:
            candidates = pool
        text = random.choice(candidates)
        color = random.choice(NEON_COLORS)
        self.words.append(FallingWord(text, self.word_speed, color))

    def handle_keypress(self, char):
        char = char.lower()
        if not char.isalpha():
            return

        # if no target, find word starting with this char
        if self.target_word is None or self.target_word not in self.words:
            self.target_word = None
            for w in sorted(self.words, key=lambda w: -w.y):
                if w.typed_index == 0 and w.text[0] == char:
                    self.target_word = w
                    break
            if self.target_word is None:
                return

        w = self.target_word
        if w.text[w.typed_index] == char:
            w.typed_index += 1
            if w.typed_index == len(w.text):
                self.complete_word(w)
        else:
            # wrong key — reset this word
            w.typed_index = 0
            self.target_word = None
            self.combo = 0

    def complete_word(self, w):
        self.words.remove(w)
        if self.target_word is w:
            self.target_word = None

        self.combo += 1
        self.max_combo = max(self.max_combo, self.combo)
        multiplier = min(self.combo, 4)
        pts = len(w.text) * 10 * multiplier
        self.score += pts

        now = time.time()
        elapsed = now - self.last_word_time
        self.last_word_time = now
        self.wpm_times.append((len(w.text), elapsed))
        if len(self.wpm_times) > 10:
            self.wpm_times.pop(0)
        total_chars = sum(c for c, _ in self.wpm_times)
        total_time = sum(t for _, t in self.wpm_times)
        if total_time > 0:
            self.wpm = int((total_chars / 5) / (total_time / 60))

        self.words_destroyed += 1
        self.total_chars += len(w.text)

        # particles
        cx = w.x + FONT_WORD.size(w.text)[0] // 2
        cy = int(w.y) + 15
        for _ in range(30):
            self.particles.append(Particle(cx, cy, w.color))
        for _ in range(10):
            self.particles.append(Particle(cx, cy, WHITE))

        # score flash
        label = f"+{pts}"
        if multiplier > 1:
            label += f" x{multiplier}!"
        self.flashes.append(ScoreFlash(cx, cy - 20, label, w.color))

        # level up?
        if self.words_destroyed % WORDS_PER_LEVEL == 0:
            self.level += 1
            self.word_speed = BASE_SPEED + SPEED_INCREMENT * (self.level - 1)
            self.spawn_interval = max(0.8, SPAWN_INTERVAL_BASE - 0.18 * (self.level - 1))
            self.banners.append(LevelBanner(self.level))

    def miss_word(self, w):
        self.words.remove(w)
        if self.target_word is w:
            self.target_word = None
        self.lives -= 1
        self.combo = 0
        # red flash particles
        cx = int(w.x + FONT_WORD.size(w.text)[0] // 2)
        for _ in range(15):
            self.particles.append(Particle(cx, HEIGHT - 10, (255, 50, 50)))
        self.flashes.append(ScoreFlash(cx, HEIGHT - 50, "MISS!", (255, 80, 80)))
        if self.lives <= 0:
            self.state = "gameover"

    def update(self, dt):
        for star in self.stars:
            star.update(dt)

        if self.state == "playing":
            self.spawn_timer += dt
            if self.spawn_timer >= self.spawn_interval:
                self.spawn_timer = 0
                self.spawn_word()

            for w in list(self.words):
                w.update(dt)
                if w.bottom >= HEIGHT:
                    self.miss_word(w)

            self.particles = [p for p in self.particles if p.update(dt)]
            self.flashes = [f for f in self.flashes if f.update(dt)]
            self.banners = [b for b in self.banners if b.update(dt)]

    def draw_menu(self):
        screen.fill(DARK)
        for star in self.stars:
            star.draw(screen)

        title = FONT_BIG.render("TypeBlast", True, (255, 220, 50))
        screen.blit(title, title.get_rect(center=(WIDTH // 2, 220)))

        sub = FONT_HUD.render("Destroy words before they reach the bottom!", True, (180, 180, 220))
        screen.blit(sub, sub.get_rect(center=(WIDTH // 2, 300)))

        tip1 = FONT_SMALL.render("Type the first letter to lock onto a word, then finish it!", True, GRAY)
        screen.blit(tip1, tip1.get_rect(center=(WIDTH // 2, 345)))

        # color samples
        sample_y = 400
        sample_words = ["python", "fast", "neon", "code", "blast"]
        sx = WIDTH // 2 - sum(FONT_WORD.size(w)[0] + 20 for w in sample_words) // 2
        for i, word in enumerate(sample_words):
            color = NEON_COLORS[i % len(NEON_COLORS)]
            s = FONT_WORD.render(word, True, color)
            screen.blit(s, (sx, sample_y))
            sx += s.get_width() + 20

        pulse = abs(math.sin(time.time() * 2.5))
        g = int(180 + 75 * pulse)
        start = FONT_HUD.render("[ PRESS ENTER TO START ]", True, (100, g, 100))
        screen.blit(start, start.get_rect(center=(WIDTH // 2, 500)))

        tips = [
            "Combo multiplier up to x4 for chaining words!",
            "Words get faster each level.",
            "You have 3 lives — don't let words slip through!",
        ]
        tip = tips[int(time.time() / 3) % len(tips)]
        ts = FONT_SMALL.render(tip, True, (120, 120, 160))
        screen.blit(ts, ts.get_rect(center=(WIDTH // 2, 580)))

    def draw_playing(self):
        screen.fill(DARK)
        for star in self.stars:
            star.draw(screen)

        for p in self.particles:
            p.draw(screen)

        # draw words
        for w in self.words:
            w.draw(screen, w is self.target_word)

        for f in self.flashes:
            f.draw(screen)

        self.draw_hud()

        for b in self.banners:
            b.draw(screen)

    def draw_hud(self):
        # top bar background
        pygame.draw.rect(screen, (15, 15, 30), (0, 0, WIDTH, 44))
        pygame.draw.line(screen, (60, 60, 100), (0, 44), (WIDTH, 44), 1)

        # score
        sc = FONT_HUD.render(f"SCORE  {self.score:,}", True, (255, 220, 50))
        screen.blit(sc, (16, 12))

        # wpm
        wpm_s = FONT_HUD.render(f"WPM  {self.wpm}", True, (80, 200, 255))
        screen.blit(wpm_s, (260, 12))

        # level
        lv = FONT_HUD.render(f"LVL  {self.level}", True, (200, 80, 255))
        screen.blit(lv, (430, 12))

        # combo
        if self.combo > 1:
            pulse = abs(math.sin(time.time() * 6))
            g = int(100 + 155 * pulse)
            cc = FONT_HUD.render(f"COMBO  x{min(self.combo, 4)}", True, (255, g, 80))
            screen.blit(cc, (580, 12))

        # lives (hearts)
        for i in range(3):
            color = (255, 60, 60) if i < self.lives else (60, 30, 30)
            hx = WIDTH - 30 - i * 36
            hy = 14
            self._draw_heart(screen, hx, hy, color)

        # current input echo
        if self.current_input:
            inp = FONT_SMALL.render(f"> {self.current_input}", True, GREEN)
            screen.blit(inp, (16, HEIGHT - 28))

        # combo bar
        if self.combo > 0:
            bar_w = int((min(self.combo, 4) / 4) * 300)
            pulse = abs(math.sin(time.time() * 4))
            r = int(200 + 55 * pulse)
            pygame.draw.rect(screen, (40, 40, 60), (WIDTH // 2 - 150, HEIGHT - 20, 300, 10), border_radius=5)
            pygame.draw.rect(screen, (r, 100, 50), (WIDTH // 2 - 150, HEIGHT - 20, bar_w, 10), border_radius=5)

    def _draw_heart(self, surf, x, y, color):
        pygame.draw.circle(surf, color, (x - 5, y), 7)
        pygame.draw.circle(surf, color, (x + 5, y), 7)
        points = [(x - 12, y + 4), (x, y + 18), (x + 12, y + 4)]
        pygame.draw.polygon(surf, color, points)

    def draw_gameover(self):
        screen.fill(DARK)
        for star in self.stars:
            star.draw(screen)

        title = FONT_BIG.render("GAME OVER", True, (255, 60, 60))
        screen.blit(title, title.get_rect(center=(WIDTH // 2, 180)))

        elapsed = max(1, time.time() - self.game_start_time)
        lines = [
            (f"Score:      {self.score:,}", (255, 220, 50)),
            (f"WPM:        {self.wpm}", (80, 200, 255)),
            (f"Level:      {self.level}", (200, 80, 255)),
            (f"Words:      {self.words_destroyed}", (80, 255, 120)),
            (f"Best Combo: x{min(self.max_combo, 4)}", (255, 140, 40)),
        ]
        for i, (line, color) in enumerate(lines):
            s = FONT_HUD.render(line, True, color)
            screen.blit(s, s.get_rect(center=(WIDTH // 2, 290 + i * 42)))

        pulse = abs(math.sin(time.time() * 2.5))
        g = int(180 + 75 * pulse)
        restart = FONT_HUD.render("[ ENTER to Play Again ]   [ ESC to Quit ]", True, (100, g, 100))
        screen.blit(restart, restart.get_rect(center=(WIDTH // 2, 530)))

    def run(self):
        running = True
        prev_time = time.time()
        while running:
            now = time.time()
            dt = min(now - prev_time, 0.05)
            prev_time = now

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False

                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        if self.state in ("playing", "gameover"):
                            self.state = "menu"
                        else:
                            running = False

                    elif event.key == pygame.K_RETURN:
                        if self.state in ("menu", "gameover"):
                            self.reset_game()
                            self.state = "playing"
                            self.spawn_word()

                    elif self.state == "playing":
                        if event.unicode and event.unicode.isalpha():
                            self.current_input += event.unicode
                            self.handle_keypress(event.unicode)
                        elif event.key == pygame.K_BACKSPACE:
                            if self.current_input:
                                self.current_input = self.current_input[:-1]
                            if self.target_word:
                                self.target_word.typed_index = max(0, self.target_word.typed_index - 1)
                                if self.target_word.typed_index == 0:
                                    self.target_word = None

            self.update(dt)

            if self.state == "menu":
                self.draw_menu()
            elif self.state == "playing":
                self.draw_playing()
            elif self.state == "gameover":
                self.draw_gameover()

            pygame.display.flip()
            clock.tick(60)

        pygame.quit()


if __name__ == "__main__":
    TypeBlast().run()
