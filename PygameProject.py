# cse1321
# class project
import pygame
import sys
import random
import time

# Initialize pygame
pygame.init()
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Room Puzzle Game")
clock = pygame.time.Clock()

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (200, 50, 50)
GREEN = (50, 200, 50)
BLUE = (50, 50, 200)
YELLOW = (240, 240, 0)
DARK = (30, 30, 30)

# Music/Sounds
pygame.mixer.init()
pygame.mixer.music.load('Intro.mp3')
pygame.mixer.music.play(-1)
arrow_whoosh = pygame.mixer.Sound('arrow_whoosh.mp3')
arrow_collision=pygame.mixer.Sound("arrow_collision.mp3")
win_sound=pygame.mixer.Sound("win.wav")

# Game state
class GameState:
    def __init__(self):
        self.current_room = "start"
        self.start_time = None

# Player
class Player(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = pygame.Surface((40, 40), pygame.SRCALPHA)
        self.image.fill((0, 0, 0, 0))  # Transparent background

        # Draw green square with white outline
        pygame.draw.rect(self.image, GREEN, (4, 4, 32, 32))
        pygame.draw.rect(self.image, WHITE, (4, 4, 32, 32), 2)

        self.rect = self.image.get_rect(topleft=(x, y))
        self.speed = 5

    def handle_keys(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT]:
            self.rect.x -= self.speed
        if keys[pygame.K_RIGHT]:
            self.rect.x += self.speed
        if keys[pygame.K_UP]:
            self.rect.y -= self.speed
        if keys[pygame.K_DOWN]:
            self.rect.y += self.speed

# Start Room
class StartRoom:
    def __init__(self):
        self.font = pygame.font.SysFont(None, 48)

    def update(self, game_state):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_SPACE]:
            game_state.current_room = "puzzle"

    def draw(self, screen):
        screen.fill(BLACK)
        text = self.font.render("Press SPACE to start the puzzle", True, WHITE)
        screen.blit(text, (150, 250))

# Puzzle Room
class PuzzleRoom:
    def __init__(self):
        originalBg = pygame.image.load("Puzzle Room Background.tiff")
        self.bg = pygame.transform.scale(originalBg, (WIDTH, HEIGHT))
        self.player = Player(100, 100)
        self.blocks = [
            pygame.Rect(150, 200, 40, 40),
            pygame.Rect(200, 300, 40, 40),
            pygame.Rect(250, 400, 40, 40)
        ]
        self.plates = [
            pygame.Rect(600, 150, 40, 40),
            pygame.Rect(600, 250, 40, 40),
            pygame.Rect(600, 350, 40, 40)
        ]

    def update(self, game_state):
        self.player.handle_keys()

        for block in self.blocks:
            if self.player.rect.colliderect(block):
                dx = self.player.rect.centerx - block.centerx
                dy = self.player.rect.centery - block.centery
                if abs(dx) > abs(dy):
                    block.x += 40 if dx < 0 else -40
                else:
                    block.y += 40 if dy < 0 else -40

        matched = 0
        for plate in self.plates:
            for block in self.blocks:
                if plate.colliderect(block):
                    matched += 1
                    break
        if matched == 3:
            game_state.current_room = "arrows"
            game_state.start_time = time.time()

    def draw(self, screen):
        screen.blit(self.bg, (0, 0))
        screen.blit(self.player.image, self.player.rect)
        for block in self.blocks:
            pygame.draw.rect(screen, BLUE, block)
        for plate in self.plates:
            pygame.draw.rect(screen, YELLOW, plate)

# Arrow Room
class ArrowRoom:
    def __init__(self):
        originalBg = pygame.image.load("Arrow Background.tiff")
        self.bg = pygame.transform.scale(originalBg, (WIDTH, HEIGHT))
        self.player = Player(400, 500)
        self.arrows = []
        self.spawn_timer = 0

    def update(self, game_state):
        self.player.handle_keys()
        now = pygame.time.get_ticks()
        if now - self.spawn_timer > 500:
            arrow = pygame.Rect(random.randint(0, WIDTH - 10), 0, 10, 30)
            self.arrows.append(arrow)
            self.spawn_timer = now
            arrow_whoosh.play()

        for arrow in self.arrows:
            arrow.y += 10

        for arrow in self.arrows:
            if arrow.colliderect(self.player.rect):
                game_state.current_room = "start"  # Restart game
                arrow_collision.play()
                self.arrows=[]

        if time.time() - game_state.start_time > 30:
            game_state.current_room = "exit"
            win_sound.play()

    def draw(self, screen):
        screen.blit(self.bg, (0, 0))

        # Optional dimming overlay (comment out if not needed)
        # dim_overlay = pygame.Surface((WIDTH, HEIGHT))
        # dim_overlay.set_alpha(100)
        # dim_overlay.fill((0, 0, 0))
        # screen.blit(dim_overlay, (0, 0))

        screen.blit(self.player.image, self.player.rect)
        for arrow in self.arrows:
            pygame.draw.rect(screen, YELLOW, arrow)

# Exit Room
class ExitRoom:
    def __init__(self):
        self.font = pygame.font.SysFont(None, 60)

    def update(self, game_state):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_ESCAPE]:
            pygame.quit()
            sys.exit()

    def draw(self, screen):
        screen.fill((0, 100, 0))
        text = self.font.render("You Win! Press ESC to Quit", True, WHITE)
        screen.blit(text, (180, 250))

# Main Game Loop
def main():
    game_state = GameState()
    rooms = {
        "start": StartRoom(),
        "puzzle": PuzzleRoom(),
        "arrows": ArrowRoom(),
        "exit": ExitRoom()
    }

    while True:
        screen.fill(BLACK)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        current_room = rooms[game_state.current_room]
        current_room.update(game_state)
        current_room.draw(screen)

        pygame.display.flip()
        clock.tick(60)

if __name__ == "__main__":
    main()
