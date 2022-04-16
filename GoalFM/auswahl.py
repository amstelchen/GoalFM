import pygame, pygame_menu, pygame_widgets
from pygame_widgets.button import Button
import GoalFM, GoalFM.sqlite3db
from sqlite3db import * # confederations
import pygame.draw as dr
import textwrap, os

def close_game():
    print("Beendet.")
    pygame.quit()
    run = False
    quit()

def select_conf(short_name, long_name):
    screen.fill(green)
    buttonWeiter.enable()

    imgConf = pygame.image.load(os.path.join('images/federations/',short_name + '.png'))
    screen.blit(imgConf, (350, 160))
    tw = textwrap.wrap(long_name, width=30)
    #tw = str.split(value,maxsplit=50)
    #str.replace(value, "in", "\nin")
    x = int(0)
    for line in tw:
        Desc = smallfont.render(str(line), True, (0, 0, 0))
        screen.blit(Desc, (350, 100+x))
        x += 20

pygame.time.Clock()

pygame.init()

conn = connect_goal_db()

# initialize font; must be called after 'pygame.init()' to avoid 'Font not Initialized' error
smallfont = pygame.font.SysFont("monospace", 18)
boldfont = pygame.font.SysFont("Arial Black", 14)
largefont = pygame.font.SysFont("Arial Black", 80)

ScreenX = 800
ScreenY = 600

width = ScreenX - 100
height = ScreenY - 200

screen = pygame.display.set_mode((ScreenX, ScreenY))

green = (0, 139, 0)
screen.fill(green)

rows = confederations(conn)

lineDesc = "Bitte wählen sie einen Fussballverband"
Desc = smallfont.render(lineDesc, True, (0, 0, 0))
screen.blit(Desc, (350, 230))

buttonWeiter = Button(screen, 350, 500, 200-10, 40, text="Auswählen", font=smallfont, onClick=close_game,
    inactiveColour=(186, 214, 177), hoverColour=(100, 200, 20), pressedColour=(0, 200, 20),enabled=False)
buttonClose = Button(screen, 550, 500, 200-10, 40, text="Schließen", font=smallfont, onClick=close_game,
    inactiveColour=(186, 214, 177), hoverColour=(100, 200, 20), pressedColour=(0, 200, 20))

buttonWeiter.disable()
zeile=0
for row in rows:
    print(row)
    myl = []
    myl.append(str(row[0]))
    myl.append(str(row[1]))
    buttonConf = Button(screen, 100, 100+zeile*40, 200, 40, text=row[0], font=smallfont, onClick=select_conf, onClickParams=myl,
        inactiveColour=(186, 214, 177), hoverColour=(100, 200, 20), pressedColour=(0, 200, 20))
    zeile += 1

#imgKontinent = pygame.image.load(r'assets/blue-glossy-button-blank-icon-square-empty-shape-vector-12937816.jpg')
#imgKontinent = pygame.transform.scale(imgKontinent, (100, 100))

run = True
while run:

    #labelStadion = largefont.render(Stadionname, True, (0, 0, 0))
    #labelKapazitaet = boldfont.render("Kapazität " + str(Kapazitaet), True, (0, 0, 0))
    #labelHeimmannschaft = boldfont.render("Heimmannschaft " + str(Heimmannschaft), True, (0, 0, 0))

    events = pygame.event.get()
    for event in events:
        if event.type == pygame.QUIT:
            pygame.quit()
            run = False
            quit()
            
    pygame_widgets.update(events)
    pygame.display.update()
    pygame.time.delay(10)
    #time.sleep(1)

pygame.time.delay(3000)
