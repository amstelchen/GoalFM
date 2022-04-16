import pygame, pygame_menu, pygame_widgets
from pygame_widgets.progressbar import ProgressBar
from pygame_widgets.button import Button
import GoalFM, GoalFM.sqlite3db
from sqlite3db import *
import time
import random
import math
import os, sys

imgSpielfeld = pygame.image.load(r'assets/240_F_195394534_OjXNWoUvzB92C7JAyiN1JcLvUWre7AvM.jpg')
imgSpielfeld = pygame.transform.scale2x(imgSpielfeld)
imgSpielfeld = pygame.transform.rotate(imgSpielfeld, 90)

def reversed_string(a_string):
    return a_string[::-1]

def taktik_aendern(strTaktik):
    buttonWeiter.enable()
    print()
    print("Taktik: " + strTaktik)

    #screen.fill(green)
    imgSpielfeldCopy = imgSpielfeld.copy()
    #screen.blit(imgSpielfeld, (250, 50))

    Px = 100; Py = 70
    Ex = imgSpielfeldCopy.get_width()
    Ey = imgSpielfeldCopy.get_height()

    Abstand = 50
    SpielerNummer = int(0)
    row = int(1)
    AnzSpieler = int(0)
    Linien = str.split(reversed_string(strTaktik),'-')
    for i in Linien:
        AnzSpieler += int(i[0])
    SpielerNummer = AnzSpieler + 1
    AnzLinien = len(str.replace(strTaktik,'-',''))
    for i in Linien:
        print("Linie " + str(row) + ": " + i + " Mann.")
        MaennerProLinie = int(i[0])
        if MaennerProLinie == 1:
            x = Ex // 2
        if MaennerProLinie >= 2:
            x = Ex // 2 - Abstand // 2 * MaennerProLinie + Abstand // 2

        for j in range(1, MaennerProLinie + 1):
            Farbe = pygame.Color("orange")
            if row == 1:
                Farbe = pygame.Color("red")
            if row == 2:
                Farbe = pygame.Color("orange")
            if row == 3 and AnzLinien == 3:
                Farbe = pygame.Color("blue")
            if row == 4:
                Farbe = pygame.Color("blue")

            y = Py + row * 120 # 145
            ci = pygame.draw.circle(imgSpielfeldCopy, Farbe, (x, y), radius=15)
            #pygame.display.update()

            #rx = pygame.draw.rect(imgSpielfeldCopy, pygame.Color('blue'), [x, y, 1, 1])
            labelN = boldfont.render(str(SpielerNummer), True, pygame.Color('white')).convert_alpha(screen)
            rx = pygame.Rect(x - labelN.get_width()/2, y - labelN.get_height()/2, 20, 20)
            imgSpielfeldCopy.blit(labelN, rx) #, [x + 100, y, x + 30, y + 30])

            print('{:>5}'.format(SpielerNummer) + ": " + str((x, y)))
            x += Abstand
            SpielerNummer -= 1
        row += 1
        pygame.draw.circle(imgSpielfeldCopy, pygame.Color("black"), (Ex / 2, Ey - 50), radius=15)
        labelN = boldfont.render("1", True, pygame.Color('white')).convert_alpha(screen)
        rx = pygame.Rect(Ex / 2 - labelN.get_width()/2, Ey - 50 - labelN.get_height()/2, 20, 20)
        imgSpielfeldCopy.blit(labelN, rx) #, [x + 100, y, x + 30, y + 30])

    screen.blit(imgSpielfeldCopy, (250, 50))

def close_game():
    print("Beendet.")
    pygame.quit()
    run = False
    quit()

pygame.time.Clock()

pygame.init()

conn = connect_goal_db()

green = (0, 139, 0)  

# initialize font; must be called after 'pygame.init()' to avoid 'Font not Initialized' error
smallfont = pygame.font.SysFont("monospace", 18)
smallAfont = pygame.font.SysFont("Arial", 18)
boldfont = pygame.font.SysFont("Arial Black", 18)
largefont = pygame.font.SysFont("Arial Black", 80)

ScreenX = 800
ScreenY = 800

width = ScreenX - 200
height = ScreenY - 200

screen = pygame.display.set_mode((ScreenX, ScreenY))

screen.fill(green)

screen.blit(imgSpielfeld, (250, 50))

rows = select_taktiken(conn)

labelHead = smallAfont.render("Taktik wählen", True, pygame.Color('white')).convert_alpha(screen)
rx = pygame.Rect(70, 50, 20, 20)
screen.blit(labelHead, rx) #, [x + 100, y, x + 30, y + 30])

zeile=0
for row in rows:
    print(row)
    strTaktik = [row[0]]
    buttonConf = Button(screen, 70, 100+zeile*35, 100, 40, text=row[0], font=smallfont, onClick=taktik_aendern, onClickParams=strTaktik,
        inactiveColour=(186, 214, 177), hoverColour=(100, 200, 20), pressedColour=(0, 200, 20))
    zeile += 1

buttonWeiter = Button(screen, 50, 700-20, 150-10, 40, text="Fortsetzen", font=smallfont, onClick=close_game,
        inactiveColour=(186, 214, 177), hoverColour=(100, 200, 20), pressedColour=(0, 200, 20))
buttonClose = Button(screen, 50, 750-20, 150-10, 40, text="Schließen", font=smallfont, onClick=close_game,
        inactiveColour=(186, 214, 177), hoverColour=(100, 200, 20), pressedColour=(0, 200, 20))

buttonWeiter.disable()

run = True
while run:

    # render text
    #labelScore = largefont.render(str(ToreA) + " : " + str(ToreB), True, (0, 0, 0))

    events = pygame.event.get()
    for event in events:
        if event.type == pygame.QUIT:
            pygame.quit()
            run = False
            quit()
            
    #screen.blit(imgSpielfeld, (250, 50))

    #pygame.draw.rect(screen, pygame.Color("white"), (0, 0, 800, 200))

    #screen.blit(labelSM, (100, 150))

    #screen.blit(i, (100+180, 10))
    #screen.blit(i, (width-180, 10))

    pygame_widgets.update(events)
    pygame.display.update()
    pygame.time.delay(10)
    #time.sleep(1)

pygame.time.delay(3000)
#pygame_widgets.update(events)
#pygame.display.update()
