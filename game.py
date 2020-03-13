import os
import random
import time

import pygame


pygame.font.init()
menu = pygame.display.set_mode((556, 313))
font = pygame.font.Font(pygame.font.match_font('arial'), 14)
text1 = 'PLAY'
text2 = 'CONTROLS'
color = (255, 255, 255)

button1 = pygame.Rect(160, 240, 100, 50)
play_button = font.render(text1, True, color)
button2 = pygame.Rect(310, 240, 100, 50)
controls_button = font.render(text2, True, color)
bg = pygame.image.load('background.png')
option = 0


def music():
    pygame.mixer.init()
    pygame.mixer.music.load('music.mp3')
    pygame.mixer.music.play()


def controls():
    global option
    ok = False
    A = pygame.image.load('Letter_A.png')
    D = pygame.image.load('Letter_D.png')
    W = pygame.image.load('Letter_W.png')
    while not ok:
        menu = pygame.display.set_mode((556, 313))
        bg = pygame.image.load('background.png')
        menu.blit(bg, (0, 0))
        menu.blit(A, (556 / 3 - 30, 2 * 313 / 3))
        menu.blit(D, (2 * 556 / 3 - 30, 2 * 313 / 3))
        menu.blit(W, (250,170))
        pygame.display.update()
        time.sleep(3.5)
        option = 1
        redirect()
        return False


class Viking:
    x = 500
    y = 480
    icon = pygame.image.load('viking.png')
    health = 100

    def __init__(self, x, y, icon, health):
        self.x = x
        self.y = y
        self.icon = icon
        self.health = health


def get():
    x = random.randint(5, 980)
    if Viking.x - 15 < x < Viking.x + 15:
        return x
    else:
        return False
class Enemies:
    x = get()
    y = 480
    iconE = pygame.image.load('enemy.png')
    health = 100

    def __init__(self, x, y, iconE, health):
        self.x = x
        self.y = y
        self.iconE = iconE
        self.health = health

    def move(self):
        if self.x < Viking.x:
            self.x += 0.1
        else:
            self.x -= 0.1

def geticon():
    if Enemies.x < Viking.x:
        icon = pygame.image.load('arrowright.png')
        return icon
    else:
        icon = pygame.image.load('arrowleft.png')
        return icon

class Arrow:

    x = Enemies.x + 10
    y = Viking.y + 15
    icon = geticon()
    def __init__(self,x, y,icon):
        self.x = x
        self.y = y
        self.icon = icon

def arrow_shot(where):
    Arrow.icon = geticon()
    where.blit(Arrow.icon, (Arrow.x, Arrow.y))




def left_leg(obj):
    if obj.y == 480:
        return pygame.Rect(obj.x + 12, obj.y + 64, 16, 32)
    else:
        return pygame.Rect((obj.x + 12, obj.y + 64,16,12))


def right_leg(obj):
    if obj.y == 480:
        return pygame.Rect(obj.x + 36, obj.y + 64, 16, 32)
    else:
        return pygame.Rect(obj.x + 36, obj.y + 64, 16, 12)

def ground(M):
    ground = pygame.Rect(0, 544 + 32, 1000, 1000)
    return pygame.draw.rect(M, (96, 128, 56), ground)




def tree(N):
    pygame.draw.rect(N, (165, 42, 42), [260, 480, 30, 100])
    pygame.draw.polygon(N, (51, 102, 0), [[350, 480], [275, 330], [200, 480]])
    pygame.draw.polygon(N, (51, 102, 0), [[340, 430], [275, 310], [210, 430]])
    pygame.draw.rect(N, (165, 42, 42), [860, 480, 45, 100])
    pygame.draw.polygon(N, (51, 102, 0), [[950, 480], [875, 330], [800, 480]])
    pygame.draw.polygon(N, (51, 102, 0), [[950, 430], [875, 285], [800, 430]])



def limits(obj):
    if obj.x < -5 or obj.x > 1000:
        return False
    else:
        return True

def play():
    os.environ['SDL_VIDEO_WINDOW_POS'] = "%d,%d" % (20, 20)
    pygame.init()
    wid = 1000
    hei = 600
    world = pygame.display.set_mode((wid, hei))
    alive = True
    while alive:
        world.fill((157, 215, 239))
        tree(world)
        world.blit(Viking.icon, (Viking.x, Viking.y))
        world.blit(Enemies.iconE, (Enemies.x, Enemies.y))
        arrow_shot(world)
        if Enemies.x < Viking.x:
            Arrow.x += 0.3
        else:
            Arrow.x -= 0.3
        Enemies.move(Enemies)
        if 0 > Arrow.x or Arrow.x > 1000:
            Arrow.__init__(Arrow, x=Enemies.x + 10, y= Viking.y + 15, icon=geticon())
        if Viking.y < 480:
            Viking.y += 0.3
        else:
            Viking.y = 480
        if Enemies.health == 0:
            Enemies.new(x=random.randint(0, 1000), y=480)


        pygame.draw.rect(world, (115, 77, 38), left_leg(Viking))
        pygame.draw.rect(world, (115, 77, 38), right_leg(Viking))
        pygame.draw.rect(world, (115, 77, 38), left_leg(Enemies))
        pygame.draw.rect(world, (115, 77, 38), right_leg(Enemies))
        alive = limits(Viking)


        ground(world)
        if (Arrow.x - 5 < Viking.x < Arrow.x + 5) and (Viking.y == 480):
            alive = False
        for event in pygame.event.get():
            keys = pygame.key.get_pressed()
            if keys[pygame.K_d]:
                Viking.x += 10

            elif keys[pygame.K_a]:
                Viking.x -= 10

            elif  keys[pygame.K_w] and Viking.y == 480:
                Viking.y -= 75

            elif event.type == pygame.QUIT:
                alive = False

        pygame.display.update()


def redirect():
    if option == 1:
        return play()

    elif option == 2:
        return controls()


def main():
    global option
    while True:
        menu.blit(bg, (0, 0))
        pygame.draw.ellipse(bg, [49, 121, 176], button1)
        menu.blit(play_button, (190, 255))
        pygame.draw.ellipse(bg, [49, 121, 176], button2)
        menu.blit(controls_button, (330, 255))
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.display.quit()
                return False

            if event.type == pygame.MOUSEBUTTONDOWN:
                x, y = event.pos
                if button1.collidepoint(x, y):
                    option = 1
                    redirect()
                    pygame.display.quit()
                    return False
                elif button2.collidepoint(x, y):
                    option = 2
                    redirect()
                    pygame.display.quit()
                    return False

        pygame.display.update()


music()
main()

