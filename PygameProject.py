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
pygame.mixer.music.load('audio/Intro.mp3') # Audio Credit: Ghost King's Revenge by Good Kid | Link - https://goodkid.bandcamp.com/album/ghost-kings-revenge-ost
pygame.mixer.music.play(-1)
arrow_whoosh = pygame.mixer.Sound('audio/arrow_whoosh.mp3') # Audio Source: Link - https://www.epidemicsound.com/sound-effects/tracks/74aa6c2d-9f66-49e1-b5cb-f9bd95fcaad3/
arrow_collision=pygame.mixer.Sound("audio/arrow_collision.mp3") # Audio Source: Link - https://www.epidemicsound.com/sound-effects/tracks/b0f11b27-abae-4de2-b5ac-f13b9c4f45e0/
win_sound=pygame.mixer.Sound("audio/win.wav") # Audio Source: Link - https://www.epidemicsound.com/sound-effects/tracks/451b246a-c10a-4c3b-99de-5adc399efea4/

#images
player_sprite = pygame.image.load("images/Viking_Player_sprite.png").convert_alpha() # Image Source: Artist - klyaksun | Link - https://www.bigstockphoto.com/image-457712987/stock-vector-viking-cartoon-character-sprite-sheet-animation-for-2d-rpg-game-scandinavian-warrior-personage-figh
push_box = pygame.image.load("images/push_box.png").convert_alpha() # Image Source: Artist - Kaleb da Silva Pereira | Link - https://www.vecteezy.com/vector-art/9877773-pixel-art-wooden-box-vector-icon-for-8bit-game-on-white-background
push_box_sized= pygame.transform.scale(push_box,(40,40))

# Game state
class GameState:
    def __init__(self):
        self.state = "menu"
        self.start_time = None
        self.current_room = "start"

# Player
class Player(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = pygame.Surface((40, 40), pygame.SRCALPHA)
        self.image.fill((0, 0, 0, 0))  # Transparent background

        self.rect = self.image.get_rect(topleft=(x, y))
        player_sprite_resized = pygame.transform.scale(player_sprite, (40,40))
        self.image.blit(player_sprite_resized, (0, 0))
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
        text = self.font.render("Press SPACE to try again", True, WHITE)
        screen.blit(text, (190, 250))

# Puzzle Room
class PuzzleRoom:
    def __init__(self):
        self.border = pygame.image.load("images/puzzleborder.png") # Image Source: Link - https://www.craiyon.com/image/jX_EGhdrTXCHwBjO4ZBs7Q
        self.border_thickness=10
        originalBg = pygame.image.load("images/puzzlebg.jpg") # Image Source: Artist - user2122532 | Link - https://www.freepik.com/premium-vector/pixel-brick-wall-seamless-pattern-vector-art-8-bit-design-stickers-logo-mobile-app_22754932.htm
        self.bg = pygame.transform.scale(originalBg, (WIDTH-2*self.border_thickness, HEIGHT-2*self.border_thickness))
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
            if block.x<0:
                block.x=0
            if block.x>WIDTH-40:
                block.x=WIDTH-40
            if block.y<0:
                block.y=0
            if block.y>(HEIGHT-40):
                block.y=HEIGHT-40

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
        screen.blit(self.border, (0, 0))
        screen.blit(self.bg, (self.border_thickness, self.border_thickness))
        screen.blit(self.player.image, self.player.rect)
        for plate in self.plates:
            pygame.draw.rect(screen, DARK, plate)
        for block in self.blocks:
            screen.blit(push_box_sized, block)
        if not (0<self.player.rect.x<(WIDTH-32) and (0<self.player.rect.y<(HEIGHT-32))):
            self.player.rect.topleft=(100,100)

# Arrow Room
class ArrowRoom:
    def __init__(self):
        self.border=pygame.image.load("images/arrowborder.png") # Image Source: AI Generated
        originalBg = pygame.image.load("images/arrowbg.jpg") # Image Source: Artist - pikisuperstar | Link - https://www.freepik.es/vector-gratis/fondo-paisaje-futurista-estilo-retro_5172179.htm
        self.border_thickness=10
        self.bg = pygame.transform.scale(originalBg, (WIDTH-2*self.border_thickness, HEIGHT-2*self.border_thickness))
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
        if not (0<self.player.rect.x<(WIDTH-32) and (0<self.player.rect.y<(HEIGHT-32))):
            self.player.rect.topleft=(400,500)

    def draw(self, screen):
        screen.blit(self.border, (0, 0))
        screen.blit(self.bg, (self.border_thickness, self.border_thickness))

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
        screen.blit(text, (150, 275))

# Function to render text
def drawText(text, x, y):
    font = pygame.font.SysFont(None, 50)
    render = font.render(text, True, BLACK)
    screen.blit(render, (x, y))

# Menu function
def drawMenu():
    screen.fill((180, 180, 180))
    drawText("Start Game", 300, 150)
    drawText("Reset Game", 300, 220)
    drawText("Exit", 300, 290)


# Main Game Loop
def main():
    game_state = GameState()
    rooms = {
        "start": StartRoom(),
        "puzzle": PuzzleRoom(),
        "arrows": ArrowRoom(),
        "exit": ExitRoom()
    }

    font = pygame.font.SysFont(None, 50)

    while True:
        screen.fill(BLACK)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if game_state.state == "menu" and event.type == pygame.MOUSEBUTTONDOWN:
                x, y =event.pos
                if 300 < x < 500:
                    if 150 < y < 200:
                        game_state.state = "playing"
                        game_state.current_room = "puzzle"
                    elif 220 < y < 270:
                        game_state.state = "playing"
                        game_state.current_room = "puzzle"
                        rooms["puzzle"] = PuzzleRoom()
                    elif 290 < y < 340:
                        pygame.quit()
                        sys.exit()

        if game_state.state == "menu":
            drawMenu()
        elif game_state.state == "playing":
            current_room = rooms[game_state.current_room]
            current_room.update(game_state)
            current_room.draw(screen)

        keys = pygame.key.get_pressed()
        if keys[pygame.K_ESCAPE]:
            game_state.state = "menu"

        pygame.display.flip()
        clock.tick(60)

if __name__ == "__main__":
    main()
