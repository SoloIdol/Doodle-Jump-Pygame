# V2




# -----------------Libs----------------------------------------------------------------------------------------------------------------------------

import pygame

import random

# -----------------Initializer----------------------------------------------------------------------------------------------------------------------

pygame.init()

# -----------------Window---------------------------------------------------------------------------------------------------------------------------

SCREEN_WIDTH = 514
SCREEN_HEIGHT = 912

screen = pygame.display.set_mode((SCREEN_WIDTH ,SCREEN_HEIGHT))
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

cycle = 1

score2 = 0

# -----------------Images---------------------------------------------------------------------------------------------------------------------------

bg_image=pygame.image.load('assets/StartCityBg.jpg').convert_alpha()
bg2_image=pygame.image.load('assets/ScrollCityBg1.jpg').convert_alpha()
bg3_image=pygame.image.load('assets/ScrollCityBg2.jpg').convert_alpha()
player_image=pygame.image.load('assets/slime_char_idle.png').convert_alpha()
platform_green_image=pygame.image.load('assets/green_platform.png').convert_alpha()

# -----------------Bgfunc---------------------------------------------------------------------------------------------------------------------------

def draw_bg(bg_scroll,cycle):
    #screen.blit(bg_image, (0,0+bg_scroll))
    screen.blit(bg_image, (0,0+bg_scroll))   # 912??
    for i in range(cycle):
        screen.blit(bg2_image, (0,i*(-1824)-912+bg_scroll))
        screen.blit(bg3_image, (0,i*(-1824)-1824+bg_scroll))


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
        if self.rect.right + dx > SCREEN_WIDTH :
            dx = SCREEN_WIDTH - self.rect.right

        for platform in platform_group:
            if platform.rect.colliderect(self.rect.x,self.rect.y+dy,self.width,self.height):
                if self.rect.bottom < platform.rect.centery: #ахахаха чё я накодил. Все настройки через жопу !! centery можно на top поменять, но надо тестить стабильность
                    if self.vel_y > 0:
                        self.rect.bottom = platform.rect.top
                        dy = 0 
                        self.vel_y = -25 #ахахаха чё я накодил. Все настройки через жопу 17

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
        #pygame.draw.rect(screen,WHITE, self.rect,2)


class Platform(pygame.sprite.Sprite):
    def __init__(self,x,y,width):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.transform.scale(platform_green_image,(width,10))
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
    
    def update(self,scroll):
        global score
        global score2
        global cycle
        self.rect.y += scroll

        if self.rect.top > SCREEN_HEIGHT:
            self.kill()
            score += 1
            score2 += 1
            #print(score2) ---> на проверку
        if score2 >= 10:
            score2 = 0
            cycle += 1
            #print(f'cycle :{cycle}') ---> на проверку

        


Slime = Player(SCREEN_WIDTH  // 2,SCREEN_HEIGHT-150)

platform_group = pygame.sprite.Group()

platform = Platform(SCREEN_WIDTH  // 2 - 45, SCREEN_HEIGHT-90, 80)
platform_group.add(platform)
# -----------------Game----------------------------------------------------------------------------------------------------------------------------

run = True

while run == True:

    clock.tick(FPS)

    if game_over == False:

        scroll = Slime.move()

        bg_scroll += scroll
        
        draw_bg(bg_scroll,cycle)

        if len(platform_group) < MAX_PLATFORMS:
            p_w = random.randint(40,60)
            p_x = random.randint(0,SCREEN_WIDTH  - p_w)
            p_y = platform.rect.y - random.randint(80,120)
            platform = Platform(p_x,p_y,p_w)
            platform_group.add(platform)

        
        #pygame.draw.line(screen,WHITE,(0,SCROLL_THRESH),(SCREEN_WIDTH ,SCROLL_THRESH)) #на проверочку

        platform_group.update(scroll)
        

        platform_group.draw(screen)

        Slime.draw()

        if Slime.rect.top > SCREEN_HEIGHT:
            game_over = True

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
            cycle = 1
            Slime.rect.center = (SCREEN_WIDTH  // 2,SCREEN_HEIGHT-150)
            platform_group.empty()
            # спавним платформу потому что она вне gameloop
            platform = Platform(SCREEN_WIDTH  // 2 - 45, SCREEN_HEIGHT-90, 80)
            platform_group.add(platform)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False

    pygame.display.update()


pygame.quit()