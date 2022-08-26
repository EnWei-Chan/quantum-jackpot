# -*- coding: utf-8 -*-

import sys
import pygame
import time
import math

from pygame.locals import QUIT

import numpy as np

from qiskit import *
from qiskit.tools.monitor import job_monitor

clock = pygame.time.Clock()
fps = 60
size = [200, 200]

HEIGHT = 8
WIDTH = 8
MINES = 7

BLACK = (0, 0, 0)
GRAY = (180, 180, 180)
WHITE = (255, 255, 255)

pygame.init()
size = width, height = 1024, 576
screen = pygame.display.set_mode(size)
window_surface = pygame.display.set_mode((1024,576))

pygame.mixer.init()

pygame.mixer.music.load("./musics/welcome.mp3")
pygame.mixer.music.play(-1)
pygame.mixer.music.set_volume(0.15)
congrat=pygame.mixer.Sound("./musics/Congratulations.mp3")
congrat.set_volume(2)
fail=pygame.mixer.Sound("./musics/Fail.mp3")
fail.set_volume(2)
bankrupt=pygame.mixer.Sound("./musics/BANKRUPT.mp3")
bankrupt.set_volume(2)
OPEN_SANS = "./fonts/Apple_Chancery.ttf"


smallFont = pygame.font.Font(OPEN_SANS, 30)
mediumFont = pygame.font.Font(OPEN_SANS, 42)
largeFont = pygame.font.Font(OPEN_SANS, 60)
window_surface.fill((255, 255, 255))
bg = pygame.image.load("./images/bg.png")

    #INSIDE OF THE GAME LOOP
screen.blit(bg, (0, 0))

# For chinese word
#Place after the OPEN_SANS path
OPEN_mj = "./fonts/msjh.ttf"
miniFont = pygame.font.Font(OPEN_mj, 18)
smallFont2 = pygame.font.Font(OPEN_mj, 30)

head_font = pygame.font.SysFont(None, 90)
button = pygame.Rect(100, 100, 50, 50)
instructions = True
Played = False
remaining_money = 20000
earned_money = 0

# Input textbox
text = ""
input_active = True
length_limit = 6
results = []

# User define function

def random_generator():
    
    q = QuantumRegister(16,'q')
    c = ClassicalRegister(16,'c')
    circuit = QuantumCircuit(q,c)
    circuit.h(q) # Applies hadamard gate to all qubits
    circuit.measure(q,c) # Measures all qubits 

    backend = Aer.get_backend('qasm_simulator')
    job = execute(circuit, backend, shots=1)

    # print('Executing Job...\n')                 
    # job_monitor(job)
    counts = job.result().get_counts()

    # print('RESULT: ',counts,'\n')
    
    for i in counts.keys():
        cnt = int(i, 2)
    
    before_theta = cnt * 2 / 65535 - 1

    theta = math.acos(before_theta)
    
    return theta

def get_ball():
    
    box = [0,1,2,3,4,5,6,7,8,9]
    number = []
    remained_ball = 9
    
    for i in range(0,6):

        q = QuantumRegister(6,'q')
        c = ClassicalRegister(6,'c')
        circuit = QuantumCircuit(q,c)
        for i in range(0,6):
            circuit.u3(random_generator(), 0, 0, i) # Applies u gate to all qubits
        
        circuit.measure(q,c) # Measures all qubits 

        from qiskit import Aer
        backend = Aer.get_backend('qasm_simulator')
        job = execute(circuit, backend, shots=1)

        # print('Executing Job...\n')                 
        # job_monitor(job)
        counts = job.result().get_counts()

        # print('RESULT: ',counts,'\n')

        for i in counts.keys():
            cnt = int(i, 2)

        # print(cnt)

        selected_ball = round(cnt * remained_ball / 63)
        # print(selected_ball)

        ball = box.pop(selected_ball)

        # print(ball)

        number.append(ball)

        remained_ball -= 1
        
    return number

def check(number,input_str):
    sum=0
    prize=0
    for i in range(0,6):
      if(int(input_str[i])==number[i]):
        sum+=1
    if(sum==6):
      prize=10000000
    elif(sum==5):
      prize=500000
    elif(sum==4):
      prize=40000
    else:
      sum=0
      for i in range(6):
        for j in range(6):
          if(number[i]==int(input_str[j])):
            sum+=1
      if(sum>=4):
        prize=1000
    return prize

# greenButton = button((0,255,0),150,225,250,100,'Click Me')
while True:
    bg = pygame.image.load("./images/bg.png")
    screen.blit(bg, (0, 0))
 # Show game instructions
    if instructions:

        # Title
        title = pygame.image.load("./images/Quantum_Jackpot.png")
        titleRect = title.get_rect()
        titleRect.center = ((width / 2), 50)
        screen.blit(title, titleRect)

        # Rules
        rule_title = pygame.image.load("./images/instructions.png")
        rule_titleRect = rule_title.get_rect()
        rule_titleRect.center = ((width / 2), 110)
        screen.blit(rule_title, rule_titleRect)

        rules = [
            "點開始可獲得 20,000 元",
            "一張彩票 2,000 元，一次可選 6 個不重複數字",
            "頭獎（六個全中）： 100,000,000 元",
            "次獎（中五個）： 500,000 元",
            "三獎（中四個）： 40,000 元",
            "特獎（中四個，不看順序）：1,000 元"
        ]
        for i, rule in enumerate(rules):
            line = smallFont2.render(rule, True, BLACK)
            screen.blit(line, (250,165+30*i))
        # your result gua
        # Results

        

        # Start game button
        start_button = pygame.image.load("./images/start2.png")
        start_button = pygame.transform.scale(start_button,(200,100))
        start_buttonRect = start_button.get_rect()
        start_buttonRect.center = ((width / 2 , (3 / 4) * height))
        screen.blit(start_button, start_buttonRect)

        # click, _, _ = pygame.mouse.get_pressed()
        # flag = 1
        # if click == 1:
        #     mouse = pygame.mouse.get_pos()
        #     if buttonRect.collidepoint(mouse):
        #         instructions = False
        #         print("Hello",flag)
        #         flag = flag +1
        #         time.sleep(0.3)
    else:
        
        # Title
        title = pygame.image.load("./images/Quantum_Jackpot.png")
        titleRect = title.get_rect()
        titleRect.center = ((width / 3), 50)
        screen.blit(title, titleRect)

        # Remaining money
        remaining_money_display = mediumFont.render("%d" %remaining_money, True, BLACK)
        remaining_money_displayRect = remaining_money_display.get_rect()
        remaining_money_displayRect.center = ((width * (3 / 4)), 50)
        screen.blit(remaining_money_display, remaining_money_displayRect)
        
        # Play Button
        play_button = pygame.image.load("./images/start.png")
        play_button = pygame.transform.scale(play_button,(100,50))
        play_buttonRect = play_button.get_rect()
        play_buttonRect.center = ((width / 2), ( 3 / 4) * height)
        
        # Again
        again_button = pygame.image.load("./images/RETURN.png")
        again_button = pygame.transform.scale(again_button,(200,100))
        again_buttonRect = again_button.get_rect()
        again_buttonRect.center = ((width / 2), ( 5 / 6 ) * height)
        if Played:
            
            play_buttonRect.center = (width * 2, ( 3 / 4) * height)
            # Prize
            prize = pygame.image.load("./images/%d.png" %earned_money)
            prize = pygame.transform.scale(prize,(400,200))
            prizeRect = prize.get_rect()
            prizeRect.center = ((width / 2), ( 1 / 2) * height)
            screen.blit(prize, prizeRect)
            screen.blit(again_button, again_buttonRect)
            # Result Number
            for i, result in enumerate(results):
                the_number = largeFont.render("%d" %result, True, (0,0,255))
                the_numberRect = the_number.get_rect()
                the_numberRect.center = (width / 2 - 50 * 2.5 + 50 * i, 120)
                screen.blit(the_number,the_numberRect)
            if(earned_money!=0):
                 congrat.play()
            if(earned_money==0):
                fail.play()
        else:
            screen.blit(play_button, play_buttonRect)

            # Input number
            textboxRect = pygame.Rect(width / 3, height / 2 - 100, width / 3, 100)
            pygame.draw.rect(screen, (255,255,255), textboxRect) 
            text_surf = largeFont.render(text, True, (0, 0, 0))
            screen.blit(text_surf, text_surf.get_rect(center = textboxRect.center))
    pygame.display.flip()
    bank = pygame.image.load("./images/bankruptcy.jpg" )
    bankRect = bank.get_rect()
    bankRect.center = (512, 288)
    for event in pygame.event.get():
        #if event.type == pygame.MOUSEBUTTONDOWN
        if remaining_money <= 0:
            screen.blit(bank, bankRect)
            bankrupt.play()
            pygame.display.flip()
            pygame.time.delay(3000)
            pygame.quit()
            sys.exit()
        if event.type == QUIT :
            pygame.quit()
            sys.exit()
        if event.type == pygame.MOUSEBUTTONDOWN:
            print("MouseDown")
            mouse_pos = event.pos
            print("mouse pos: ",mouse_pos)
            if start_buttonRect.collidepoint(mouse_pos):
                instructions = False
                print("Start")
                start_buttonRect.center = (width * 2 , 0)
            elif textboxRect.collidepoint(mouse_pos):
                print("Input")
                input_active = True
                text = ""
            elif play_buttonRect.collidepoint(mouse_pos) and len(text)==6:
                remaining_money -= 2000
                Played = True
                results = get_ball()
                for i in range(0,6):
                    print(results[i])
                earned_money = check(results,text)
                remaining_money += earned_money
            elif again_buttonRect.collidepoint(mouse_pos):
                Played = False
                
        if event.type == pygame.KEYDOWN and input_active and len(text)<length_limit:
            if event.key == pygame.K_RETURN:
                input_active = False
            elif event.key == pygame.K_BACKSPACE:
                text =  text[:-1]
            else:
                if event.unicode >= "0" and event.unicode <= "9":
                    flag = True
                    for i in range(len(text)):
                        if event.unicode == text[i]:
                            flag = False
                    if flag == True:
                        text += event.unicode

                
                
                    
clock.tick(fps)

 
#     break

# pygame.display.update()
print("here")
while True:
    pass
    
            
       