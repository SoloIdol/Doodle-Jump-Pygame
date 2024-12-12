import pygame
import random

# Initialisation de Pygame
pygame.init()

# Définition des dimensions de la fenêtre
SCREEN_WIDTH = 514
SCREEN_HEIGHT = 912
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption('Doodle Jump')

# Configuration de l'horloge et des FPS
clock = pygame.time.Clock()
FPS = 60

# Définition des couleurs
WHITE = (255, 255, 255)

# Définition des polices de caractères
font_small = pygame.font.SysFont('Lucida Sans', 20)
font_big = pygame.font.SysFont('Lucida Sans', 25)

# Variables du jeu
GRAVITY = 1
SCROLL_THRESH = 200
scroll = 0
MAX_PLATFORMS = 10
bg_scroll = 0
game_over = False
score = 0
cycle = 1
score2 = 0

# Lecture du meilleur score depuis un fichier
try:
    with open("topscore.txt", "r") as score_file:
        high_score = int(score_file.read())
except (FileNotFoundError, ValueError):
    high_score = 0

# Chargement des images
bg_image = pygame.image.load('assets/StartCityBg.jpg').convert_alpha()
bg2_image = pygame.image.load('assets/ScrollCityBg1.jpg').convert_alpha()
bg3_image = pygame.image.load('assets/ScrollCityBg2.jpg').convert_alpha()
player_image = pygame.image.load('assets/slime_char_idle.png').convert_alpha()
platform_green_image = pygame.image.load(
    'assets/green_platform.png').convert_alpha()
platform_neon_image = pygame.image.load(
    'assets/neonplatform.png').convert_alpha()

# Fonction pour dessiner le fond d'écran


def draw_bg(bg_scroll, cycle):
    screen.blit(bg_image, (0, 0 + bg_scroll))
    for i in range(cycle):
        screen.blit(bg2_image, (0, i * (-1824) - 912 + bg_scroll))
        screen.blit(bg3_image, (0, i * (-1824) - 1824 + bg_scroll))

# Fonction pour afficher du texte à l'écran


def draw_text(text, font, text_col, x, y):
    img = font.render(text, True, text_col)
    screen.blit(img, (x, y))

# Classe Joueur


class Player():
    def __init__(self, x, y):
        self.image = pygame.transform.scale(player_image, (50, 50))
        self.width = 35
        self.height = 30
        self.rect = pygame.Rect(0, 0, self.width, self.height)
        self.rect.center = (x, y)
        self.vel_y = 0
        self.flip = False

    def move(self):
        scroll = 0
        dx = 0
        dy = 0

        key = pygame.key.get_pressed()

        if key[pygame.K_LEFT]:
            dx = -10
            self.flip = False

        if key[pygame.K_RIGHT]:
            dx = 10
            self.flip = True

        self.vel_y += GRAVITY
        dy += self.vel_y

        if self.rect.left + dx < 0:
            dx += 600
        if self.rect.right + dx > SCREEN_WIDTH:
            dx -= 600

        # Collision avec les plateformes
        for platform in platform_group:
            if platform.rect.colliderect(self.rect.x, self.rect.y + dy, self.width, self.height):
                if self.rect.bottom < platform.rect.centery and self.vel_y > 0:
                    self.rect.bottom = platform.rect.top
                    dy = 0
                    self.vel_y = -18

        if self.rect.top <= SCROLL_THRESH and self.vel_y < 0:
            scroll = -dy

        self.rect.x += dx
        self.rect.y += dy + scroll

        return scroll

    def draw(self):
        screen.blit(pygame.transform.flip(self.image, self.flip, False),
                    (self.rect.x - (10 if not self.flip else 8), self.rect.y - 20))

# Classe Plateforme


class Platform(pygame.sprite.Sprite):
    def __init__(self, x, y, width):
        super().__init__()
        self.image = pygame.transform.scale(platform_neon_image, (width, 10))
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y

    def update(self, scroll):
        self.rect.y += scroll

        if self.rect.top > SCREEN_HEIGHT:
            self.kill()
            score2 += 1

        if score2 >= 10:
            score2 = 0
            cycle += 1


# Initialisation du joueur et des plateformes
Slime = Player(SCREEN_WIDTH // 2, SCREEN_HEIGHT - 150)
platform_group = pygame.sprite.Group()
platform = Platform(SCREEN_WIDTH // 2 - 45, SCREEN_HEIGHT - 90, 80)
platform_group.add(platform)

# Boucle de jeu principale
run = True
while run:
    clock.tick(FPS)

    if not game_over:
        scroll = Slime.move()
        bg_scroll += scroll
        draw_bg(bg_scroll, cycle)

        # Génération des nouvelles plateformes
        if len(platform_group) < MAX_PLATFORMS:
            p_w = random.randint(60, 80)
            p_x = random.randint(0, SCREEN_WIDTH - p_w)
            p_y = platform.rect.y - random.randint(80, 120)
            platform = Platform(p_x, p_y, p_w)
            platform_group.add(platform)

        platform_group.update(scroll)
        platform_group.draw(screen)
        Slime.draw()

        if Slime.rect.top > SCREEN_HEIGHT:
            game_over = True
            score = bg_scroll
    else:
        draw_text('GAME OVER', font_big, WHITE, SCREEN_WIDTH //
                  2 - 70, SCREEN_HEIGHT // 2 - 100)
        draw_text('SCORE: ' + str(score), font_big, WHITE,
                  SCREEN_WIDTH // 2 - 55, SCREEN_HEIGHT // 2 - 50)
        draw_text('HIGH SCORE: ' + str(high_score), font_big, WHITE,
                  SCREEN_WIDTH // 2 - 85, SCREEN_HEIGHT // 2 - 20)
        draw_text('PRESS SPACE TO RESTART', font_big, WHITE,
                  SCREEN_WIDTH // 2 - 150, SCREEN_HEIGHT // 2)
        key = pygame.key.get_pressed()
        if key[pygame.K_SPACE]:
            game_over = False
            score = 0
            bg_scroll = 0
            cycle = 1
            Slime.rect.center = (SCREEN_WIDTH // 2, SCREEN_HEIGHT - 150)
            platform_group.empty()
            platform = Platform(SCREEN_WIDTH // 2 - 45, SCREEN_HEIGHT - 90, 80)
            platform_group.add(platform)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False

    pygame.display.update()

pygame.quit()
