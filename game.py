import pygame
from settings import INTERNAL_W, INTERNAL_H, SCALE, SCREEN_W, SCREEN_H, FPS, TITLE


class Game:
    def __init__(self):
        pygame.init()
        self.screen   = pygame.display.set_mode((SCREEN_W, SCREEN_H))
        pygame.display.set_caption(TITLE)
        self.canvas   = pygame.Surface((INTERNAL_W, INTERNAL_H))
        self.clock    = pygame.time.Clock()
        self.running  = True
        self._state   = None
        self._pending = "menu"

    def _load_state(self, name, score=0):
        from src.states.menu      import MenuState
        from src.states.playing   import PlayingState
        from src.states.game_over import GameOverState

        if name == "menu":
            self._state = MenuState()
        elif name == "playing":
            self._state = PlayingState()
        elif name == "retry":
            self._state = PlayingState()
        elif name == "won":
            self._state = GameOverState(score, won=True)
        elif name == "dead":
            self._state = GameOverState(score, won=False)
        self._pending = None

    def run(self):
        while self.running:
            dt = self.clock.tick(FPS) / 1000.0

            if self._pending:
                self._load_state(self._pending,
                                 getattr(self._state, "score", 0))

            events = pygame.event.get()
            for event in events:
                if event.type == pygame.QUIT:
                    self.running = False

            result = self._state.handle_events(events)
            if result:
                self._pending = result

            update_result = self._state.update(dt)
            if update_result:
                self._pending = update_result

            self._state.draw(self.canvas)
            scaled = pygame.transform.scale(self.canvas, (SCREEN_W, SCREEN_H))
            self.screen.blit(scaled, (0, 0))
            pygame.display.flip()

        pygame.quit()
