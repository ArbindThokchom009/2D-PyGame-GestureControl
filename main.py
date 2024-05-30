import pygame

from fighter import Fighter

import time

from pygame import mixer

import cv2
from cvzone.HandTrackingModule import HandDetector
from directkeys import PressKey, ReleaseKey
from directkeys import space_pressed,r_pressed,t_pressed,a_pressed,d_pressed,w_pressed
import time
detector=HandDetector(detectionCon=0.8, maxHands=1)


pygame.init()
mixer.init()

# Game Window
SCREEN_WIDTH = 1000
SCREEN_HEIGHT = 600

screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))

pygame.display.set_caption("Free Fighter")

# Set Framerate
clock = pygame.time.Clock()
FPS = 60

# Game variable
intro_count = 3
last_count_update = pygame.time.get_ticks()
score = [0, 0]  # player score [p1, p2]
round_over = False
ROUND_COOLDOWN = 2000

# Define fighter variables
WARRIROR_SIZE = 162
WARRIROR_SCALE = 4
WARRIOR_OFFSET = [72, 56]
WARRIROR_DATA = [WARRIROR_SIZE, WARRIROR_SCALE, WARRIOR_OFFSET]


WIZARD_SIZE = 250
WIZARD_SCALE = 3
WIZARD_OFFSET = [112, 107]
WIZARD_DATA = [WIZARD_SIZE, WIZARD_SCALE, WIZARD_OFFSET]


#music
pygame.mixer.music.load("assets/audio/play.wav")
pygame.mixer.music.set_volume(0.5)#half
pygame.mixer.music.play(-1,0.0,5000)

sword_fx = pygame.mixer.Sound("assets/audio/warrior_slice.wav")
sword_fx.set_volume(0.5)
wizard_fx = pygame.mixer.Sound("assets/audio/wizard_slice.wav")
wizard_fx.set_volume(0.5)

victory_fx = pygame.mixer.Sound("assets/audio/victory.wav")
victory_fx.set_volume(0.5)

# Load spreadsheets image

warrior_sheet = pygame.image.load(
    "assets/characters/warrior/Sprites/warrior.png").convert_alpha()
wizard_sheet = pygame.image.load(
    "assets/characters/wizard/wizard.png").convert_alpha()

# load victory image

# Define number of steps in each animation
WARRIROR_ANIMATION_STEPS = [10, 8, 1, 7, 7, 3, 7]

WIZARD_ANIMATION_STEPS = [8, 8, 1, 8, 8, 3, 7]

# Define font
count_font = pygame.font.Font("assets/font/FONT.ttf", 80)
score_text = pygame.font.Font("assets/font/FONT.ttf", 24)

# Function for drawing text


def draw_text(text, font, text_col, x, y):
    img = font.render(text, True, text_col)
    screen.blit(img, (x, y))


# Load Bg
bg_image = pygame.image.load("assets/background.png").convert_alpha()

# Background image

def draw_bg():
    scale_bg = pygame.transform.scale(bg_image, (SCREEN_WIDTH, SCREEN_HEIGHT))
    screen.blit(scale_bg, (0, 0))

# Health bar

def draw_health_bar(health, x, y):
    ratio = health/100
    pygame.draw.rect(screen, 'white', (x-2, y-2, 401, 34))
    pygame.draw.rect(screen, 'red', (x, y, 400, 30))
    pygame.draw.rect(screen, 'green', (x, y, 400*ratio, 30)
                     )  # Pos and pixel of health bar


# Create two instances of fighters

Fighter_1 = Fighter(1, 200, 410, False, WARRIROR_DATA, warrior_sheet,
                    WARRIROR_ANIMATION_STEPS,sword_fx)
Fighter_2 = Fighter(2, 700, 410, True, WIZARD_DATA,
                    wizard_sheet, WIZARD_ANIMATION_STEPS,wizard_fx)

#loading Screen
loading_screen = True
while loading_screen:
    screen.fill((75, 45, 214))
    draw_text("Press Space to Play", score_text, 'WHITE',
              SCREEN_WIDTH/2-200, SCREEN_HEIGHT/2)
    pygame.display.update()
    for event in pygame.event.get():
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                loading_screen = False
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()


#Camera
spaced_key_pressed = space_pressed
r_key_pressed = r_pressed
t_key_pressed = t_pressed
a_key_pressed = a_pressed
d_key_pressed = d_pressed
w_key_pressed = w_pressed
 
time.sleep(2.0)

current_key_pressed = set()

video=cv2.VideoCapture(0)

# Game loop

run = True
while run:

    clock.tick(FPS)
    
    # Detection
    ret,frame=video.read()
    
    keyPressed = False
    
    spacePressed=False
    r_Pressed = False
    t_Pressed = False
    a_Pressed = False
    d_Pressed = False
    
    
    key_count=0
    key_pressed=0  
     
    hands,img=detector.findHands(frame)
    cv2.rectangle(img, (0, 480), (300, 425),(50, 50, 255), -2)
    cv2.rectangle(img, (640, 480), (400, 425),(50, 50, 255), -2)
    
    if hands:
        lmList=hands[0]
        fingerUp=detector.fingersUp(lmList)
        #print(fingerUp)
        if fingerUp==[0,0,0,0,0]:
            cv2.putText(frame, 'Finger Count: 0', (20,460), cv2.FONT_HERSHEY_COMPLEX, 1, (255,255,255), 1, cv2.LINE_AA)
            cv2.putText(frame, 'idle', (440,460), cv2.FONT_HERSHEY_COMPLEX, 1, (255,255,255), 1, cv2.LINE_AA)
            PressKey(spaced_key_pressed)
            spacePressed=True
            current_key_pressed.add(spaced_key_pressed)
            key_pressed=spaced_key_pressed
            keyPressed = True
            key_count=key_count+1
        if fingerUp==[0,1,0,0,0]:
            cv2.putText(frame, 'Finger Count: 1', (20,460), cv2.FONT_HERSHEY_COMPLEX, 1, (255,255,255), 1, cv2.LINE_AA)
            cv2.putText(frame, 'Attack-1', (420,460), cv2.FONT_HERSHEY_COMPLEX, 1, (255,255,255), 1, cv2.LINE_AA)
            
            PressKey(r_key_pressed)
            r_Pressed=True
            current_key_pressed.add(r_key_pressed)
            key_pressed=r_key_pressed
            keyPressed = True
            key_count=key_count+1
            
        if fingerUp==[0,1,1,0,0]:
            cv2.putText(frame, 'Finger Count: 2', (20,460), cv2.FONT_HERSHEY_COMPLEX, 1, (255,255,255), 1, cv2.LINE_AA)
            cv2.putText(frame, 'Right Move', (420,460), cv2.FONT_HERSHEY_COMPLEX, 1, (255,255,255), 1, cv2.LINE_AA)
            PressKey(d_key_pressed)
            d_Pressed=True
            current_key_pressed.add(d_key_pressed)
            key_pressed=d_key_pressed
            keyPressed = True
            key_count=key_count+1
            
        if fingerUp==[0,1,1,1,0]:
            cv2.putText(frame, 'Finger Count: 3', (20,460), cv2.FONT_HERSHEY_COMPLEX, 1, (255,255,255), 1, cv2.LINE_AA)
            cv2.putText(frame, 'Left Move', (420,460), cv2.FONT_HERSHEY_COMPLEX, 1, (255,255,255), 1, cv2.LINE_AA)
            
            PressKey(a_key_pressed)
            a_Pressed=True
            current_key_pressed.add(a_key_pressed)
            key_pressed=a_key_pressed
            keyPressed = True
            key_count=key_count+1
            
        if fingerUp==[0,1,1,1,1]:
            cv2.putText(frame, 'Finger Count: 4', (20,460), cv2.FONT_HERSHEY_COMPLEX, 1, (255,255,255), 1, cv2.LINE_AA)
            cv2.putText(frame, 'Jumping', (420,460), cv2.FONT_HERSHEY_COMPLEX, 1, (255,255,255), 1, cv2.LINE_AA)
            '''PressKey(w_key_pressed)
            w_Pressed=True
            current_key_pressed.add(w_key_pressed)
            key_pressed=w_key_pressed
            keyPressed = True
            key_count=key_count+1'''
            
        if fingerUp==[1,1,1,1,1]:
            cv2.putText(frame, 'Finger Count: 5', (20,460), cv2.FONT_HERSHEY_COMPLEX, 1, (255,255,255), 1, cv2.LINE_AA)
            cv2.putText(frame, 'Attack-2', (420,460), cv2.FONT_HERSHEY_COMPLEX, 1, (255,255,255), 1, cv2.LINE_AA)
            PressKey(t_key_pressed)
            t_Pressed=True
            current_key_pressed.add(t_key_pressed)
            key_pressed=t_key_pressed
            keyPressed = True
            key_count=key_count+1
            
        if not keyPressed and len(current_key_pressed) != 0:
            for key in current_key_pressed:
                ReleaseKey(key)
            current_key_pressed = set()
        elif key_count==1 and len(current_key_pressed)==2:    
            for key in current_key_pressed:             
                if key_pressed!=key:
                    ReleaseKey(key)
            current_key_pressed = set()
            for key in current_key_pressed:
                ReleaseKey(key)
            current_key_pressed = set()
    
    # Draw bg
    
    draw_bg()

    # Player health(stats)

    draw_health_bar(Fighter_1.health, 20, 30)
    draw_health_bar(Fighter_2.health, 580, 30)
    draw_text("Player1: "+str(score[0]), score_text, 'RED', 20, 60)
    draw_text("Player2: "+str(score[1]), score_text, 'RED', 580, 60)

    # update countdown
    if intro_count <= 0:
        # Move Fighter and Attacking
        Fighter_1.move(SCREEN_WIDTH, SCREEN_HEIGHT,
                       screen, Fighter_2, round_over)
        Fighter_2.move(SCREEN_WIDTH, SCREEN_HEIGHT,
                       screen, Fighter_1, round_over)
        #draw_text('Fight', count_font, 'RED', 345, 227)
    else:
        # Display count-timer
        
        draw_text(str(intro_count), count_font, 'RED',
                  SCREEN_WIDTH/2, SCREEN_HEIGHT/3)

        # update count timer
        if(pygame.time.get_ticks()-last_count_update) >= 1000:
            intro_count -= 1
            last_count_update = pygame.time.get_ticks()

    # update fighters
    Fighter_1.update()
    Fighter_2.update()

    # Draw Figter
    Fighter_1.draw(screen)
    Fighter_2.draw(screen)

    # Check the player defeat
    if round_over == False:
        if Fighter_1.alive == False:
            score[1] += 1
            round_over = True
            round_over_time = pygame.time.get_ticks()
        elif Fighter_2.alive == False:
            score[0] += 1
            round_over = True
            round_over_time = pygame.time.get_ticks()
    else:
        draw_text("VICTORY",count_font,'YELLOW',360, 150)
        victory_fx.play()
        if pygame.time.get_ticks() - round_over_time > ROUND_COOLDOWN:
            round_over = False
            intro_count = 3
            Fighter_1 = Fighter(1, 200, 410, False, WARRIROR_DATA, warrior_sheet,
                                    WARRIROR_ANIMATION_STEPS,sword_fx)
            Fighter_2 = Fighter(2, 700, 410, True, WIZARD_DATA,
                                    wizard_sheet, WIZARD_ANIMATION_STEPS,wizard_fx)

    # event handler
    for event in pygame.event.get():
        '''if event.type==pygame.KEYDOWN:
            if event.key==pygame.K_SPACE:
                Loading_screen = True
                print("pause")'''
        if event.type == pygame.QUIT:
            run = False
        

    # Update the display
    pygame.display.update()

# exit pygame
pygame.quit()
