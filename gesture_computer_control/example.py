# Pygame шаблон - скелет для нового проекта Pygame
import pygame
import random
import time
import cv2
import mediapipe as mp
from pygame import mixer

import gb_model

WIDTH = 800
HEIGHT = 650
FPS = 30

# Задаем цвета
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)



mpHands = mp.solutions.hands
hands = mpHands.Hands(False)
npDraw = mp.solutions.drawing_utils

class Player(pygame.sprite.Sprite):
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.Surface((50, 50))
        self.image.fill(GREEN)
        self.rect = self.image.get_rect()
        self.x = x
        self.y = y
        self.rect.center = (x, y)


    def update(self):
        self.rect.center = (self.x, self.y)
        # self.rect.x += 5
        # if self.rect.left > WIDTH:
        #     self.rect.right = 0

    def left(self):
        self.x -= 50
        print (self.x)
        if self.x <= left_border.x:
            self.x = 450

    def right(self):
        self.x += 50
        print (self.x)
        if self.x >= right_border.x:
            self.x = 350




class Cube(pygame.sprite.Sprite):
    def __init__(self, x, y, speed):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.Surface((50, 50 + random.randint(0, 50)))
        self.image.fill(RED)
        self.rect = self.image.get_rect()
        self.x = x
        self.y = y
        self.speed = speed + min (score, 50)/100.0 + random.randint(0, 1)
        self.rect.center = (self.x, self.y)


    def update(self):
        self.rect.y += self.speed
        global score
        if self.rect.top > HEIGHT:
            score = score + 1
            print ("del")
            all_sprites.remove(self)

        if self.rect.center[0] == player.rect.center[0]:
            if self.rect.center[1] + self.image.get_size()[1]/2 > player.rect.center[1] - 25 and self.rect.center[1] - self.image.get_size()[1]/2 < player.rect.center[1] + 25:
                print ("Game over")
                all_sprites.remove(player)
                global running
                running = False

class Border(pygame.sprite.Sprite):
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.Surface((10, HEIGHT))
        self.image.fill(GREEN)
        self.rect = self.image.get_rect()
        self.x = x
        self.y = y
        self.rect.center = (self.x, self.y)

class ProgressImpuls (pygame.sprite.Sprite):
    def __init__(self, ind):
        pygame.sprite.Sprite.__init__(self)
        self.ind = ind
        self.image = pygame.Surface((10, 10))
        self.image.fill(GREEN)
        self.rect = self.image.get_rect()
        self.rect.center = (WIDTH - 100, HEIGHT - 10 - 10 * self.ind)

    def update(self):
        global label_count
        if (label_count[6] > self.ind):
            pygame.Surface.set_alpha(self.image, 255)
        else:
            pygame.Surface.set_alpha(self.image, 0)






# Создаем игру и окно
pygame.init()
pygame.mixer.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("My Game")
clock = pygame.time.Clock()
all_sprites = pygame.sprite.Group()
player = Player(400, HEIGHT - 50)
all_sprites.add(player)

left_border = Border(300, HEIGHT/2)
right_border = Border(500, HEIGHT/2)

all_sprites.add(left_border)
all_sprites.add(right_border)

cubes = []
score = 0
bar = []
label_count = None
running = True
cube_speed = 5

for i in range (4):
    bar.append(ProgressImpuls (i))
    all_sprites.add(bar[-1])

start_time = time.time()

mixer.init()
mixer.music.load('song.mp3')
mixer.music.set_volume(0.5)

def get_label (cap, label_count, num_comands):

    # mpHands = mp.solutions.hands
    # hands = mpHands.Hands(False)
    # npDraw = mp.solutions.drawing_utils
    # if (time.time() - start_time > 0.1):
    #     start_time = time.time()
    # else:
    #     continue
    success, img = cap.read()
    img = cv2.flip(img,1) # Mirror flip

    imgRGB = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    results = hands.process(imgRGB)
    if results.multi_hand_landmarks:
        for handLms in results.multi_hand_landmarks:
            points_hand = []
            for id, lm in enumerate(handLms.landmark):
                h,w,c = img.shape
                cx, cy = int(lm.x*w), int(lm.y*h)
                points_hand = points_hand + [lm.x * w, lm.y * w, lm.z * w]
               # print(id, lm)
                if  id == 8 or id == 12:
                    cv2.circle(img, (cx,cy),10,(255,0,255),cv2.FILLED)

            #npDraw.draw_landmarks(img, handLms, mpHands.HAND_CONNECTIONS)



            # with open('eggs.csv', "a", newline="") as file:
            #     user = points_hand
            #     writer = csv.writer(file)
            #     writer.writerow(user)

            # with open('readme.txt', 'a') as f:
            #     s = ''
            #     i = 0
            #     for x in points_hand:
            #         s += (str(x) + ' ')
            #         i += 1
            #
            #     f.write(s)
            #     f.write('\n')
            #     f.write('new')
            #     f.write(str(len(points_hand)))
            #     f.write(str(i))

            label = gb_model.pred([points_hand])
            l = int(label)
            label_count[l] += 1;
            for i in range(1, num_comands):
                if (l + i) % num_comands != 6:
                    label_count[(l + i) % num_comands] = 0

            return label

def play_cikle(num_comands, cap):
    global label_count, running
    label_count = [0] * num_comands
    # Цикл игры
    running = True
    j = 0
    mixer.music.play()
    while running:
        print (running)
        # Держим цикл на правильной скорости
        clock.tick(FPS)

        # Ввод процесса (события)
        for event in pygame.event.get():
            # check for closing window
            if event.type == pygame.QUIT:
                running = False

        # Обновление
        all_sprites.update()

        if (j > (1 - (min(score, 50)/100.0)) * FPS):
            place = random.randint(0, 3)
            if place < 1:
                cubes.append(Cube(350, 50, cube_speed))
            elif place < 2:
                cubes.append(Cube(400, 50, cube_speed))
            else:
                cubes.append(Cube(450, 50, cube_speed))
            all_sprites.add(cubes[-1])
            j = 0

        label = get_label(cap, label_count, num_comands)


        match label:
                case 4:
                    if label_count[4] > 1 and label_count[6] > 4:
                            player.left()
                            label_count[4] = 0
                            label_count[6] = 0

                case 5:
                    if label_count[5] > 1 and label_count[6] > 4:
                        player.right()
                        label_count[5] = 0
                        label_count[6] = 0




        # Рендеринг
        screen.fill(BLACK)
        font = pygame.font.Font(None, 36)
        score_text = font.render(f'Score: {score}', True, (255, 255, 255))
        screen.blit(score_text, (10, 10))
        print (score)
        all_sprites.draw(screen)
        j += 1
        # После отрисовки всего, переворачиваем экран
        pygame.display.flip()

    time.sleep(1)
    pygame.quit()




cap = cv2.VideoCapture(0)
cap.set(3, 640) # Width
cap.set(4, 480) # Lenght
cap.set(10, 100) # Brightness

play_cikle(7, cap)
