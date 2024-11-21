# -----------------Libs----------------------------------------------------------------------------------------------------------------------------

import pygame

import random

# -----------------Initializer----------------------------------------------------------------------------------------------------------------------

pygame.init()

# -----------------Window---------------------------------------------------------------------------------------------------------------------------

screen_width = 300
screen_height = 600

screen = pygame.display.set_mode((screen_width,screen_height))
pygame.display.set_caption('Doodle Jump')

clock = pygame.time.Clock()
FPS = 60

# -----------------Colors---------------------------------------------------------------------------------------------------------------------------

WHITE = (255,255,255)

# -----------------Fonts---------------------------------------------------------------------------------------------------------------------------

font_small = pygame.font.SysFont('Lucida Sans',20)

font_big = pygame.font.SysFont('Lucida Sans',25)

# -----------------Game Vars-------------------------------------------------------------------------------------------------------------------------

GRAVITY = 1

SCROLL_THRESH = 200

scroll = 0

MAX_PLATFORMS = 10

bg_scroll = 0

game_over = False

score = 0

# -----------------Images---------------------------------------------------------------------------------------------------------------------------

bg_image=pygame.image.load('assets/doodle_background.jpg').convert_alpha()
player_image=pygame.image.load('assets/slime_char_idle.png').convert_alpha()
platform_green_image=pygame.image.load('assets/green_platform.png').convert_alpha()

# -----------------Bgfunc---------------------------------------------------------------------------------------------------------------------------

def draw_bg(bg_scroll):
    screen.blit(bg_image, (0,0+bg_scroll))
    screen.blit(bg_image, (0,-600+bg_scroll))   # 600 ---> высота БГ 

# -----------------Text output func---------------------------------------------------------------------------------------------------------------------------

def draw_text(text,font,text_col,x,y):
    img = font.render(text, True, text_col)
    screen.blit(img,(x,y))

# -----------------Classes--------------------------------------------------------------------------------------------------------------------------

class Player():
    def __init__(self, x, y):
        self.image = pygame.transform.scale(player_image, (50,50))
        self.width = 35
        self.height = 30
        self.rect = pygame.Rect(0, 0, self.width,self.height)
        self.rect.center = (x,y)
        self.vel_y = 0 
        self.flip = False

    def move(self):
        scroll = 0
        dx = 0
        dy = 0

        key = pygame.key.get_pressed()

        if key[pygame.K_a] == True:
            dx = -10
            self.flip = False

        if key[pygame.K_d] == True: 
            dx = 10
            self.flip = True

        self.vel_y += GRAVITY
        dy += self.vel_y
        
        if self.rect.left + dx < 0:
            dx = -self.rect.left 
        if self.rect.right + dx > screen_width:
            dx = screen_width - self.rect.right

        for platform in platform_group:
            if platform.rect.colliderect(self.rect.x,self.rect.y+dy,self.width,self.height):
                if self.rect.bottom < platform.rect.centery: #ахахаха чё я накодил. Все настройки через жопу !! centery можно на top поменять, но надо тестить стабильность
                    if self.vel_y > 0:
                        self.rect.bottom = platform.rect.top
                        dy = 0
                        self.vel_y = -17 #ахахаха чё я накодил. Все настройки через жопу

        if self.rect.top <= SCROLL_THRESH:
            if self.vel_y < 0:
                scroll = -dy

        self.rect.x += dx    
        self.rect.y += dy + scroll


        return scroll

   


    
    def draw(self):
        if self.flip == False:
            drect=10
        else:
            drect=8

        screen.blit(pygame.transform.flip(self.image, self.flip, False),(self.rect.x-drect,self.rect.y-20))
        pygame.draw.rect(screen,WHITE, self.rect,2)


class Platform(pygame.sprite.Sprite):
    def __init__(self,x,y,width):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.transform.scale(platform_green_image,(width,10))
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
    
    def update(self,scroll):
        self.rect.y += scroll

        if self.rect.top > screen_height:
            self.kill()
    


Slime = Player(screen_width // 2,screen_height-150)

platform_group = pygame.sprite.Group()

platform = Platform(screen_width // 2 - 45, screen_height-90, 80)
platform_group.add(platform)
# -----------------Game----------------------------------------------------------------------------------------------------------------------------

run = True

while run == True:

    clock.tick(FPS)

    if game_over == False:

        scroll = Slime.move()

        bg_scroll += scroll

        if bg_scroll >= 600:  # высота БГ
            bg_scroll = 0 

        draw_bg(bg_scroll)

        if len(platform_group) < MAX_PLATFORMS:
            p_w = random.randint(40,60)
            p_x = random.randint(0,screen_width - p_w)
            p_y = platform.rect.y - random.randint(80,120)
            platform = Platform(p_x,p_y,p_w)
            platform_group.add(platform)

        
        #pygame.draw.line(screen,WHITE,(0,SCROLL_THRESH),(screen_width,SCROLL_THRESH)) #на проверочку

        platform_group.update(scroll)
        

        platform_group.draw(screen)

        Slime.draw()

        if Slime.rect.top > screen_height:
            game_over = True

        print(game_over)

    else:
        draw_text('GAME OVER',font_big,WHITE,80,200)
        draw_text('SCORE: ' + str(score),font_big,WHITE,100,250)
        draw_text('PRESS SPACE TO RESTART',font_big,WHITE,0,300)
        key = pygame.key.get_pressed()
        if key[pygame.K_SPACE]:
            game_over=False
            score = 0
            scroll = 0 
            bg_scroll = 0
            Slime.rect.center = (screen_width // 2,screen_height-150)
            platform_group.empty()
            # спавним платформу потому что она вне gameloop
            platform = Platform(screen_width // 2 - 45, screen_height-90, 80)
            platform_group.add(platform)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False

    pygame.display.update()


pygame.quit()