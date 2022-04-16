import pygame, pygame_menu, pygame_widgets
from pygame_widgets.button import Button
import pygame.draw as dr
import math
from math import cos, sin
import locale

locale.setlocale(locale.LC_NUMERIC, "de_DE.utf8")

def fill_arc(center, radius, theta0, theta1, color):
    ndiv = 100
    d_theta = (theta1 - theta0) / ndiv

    for i in range(ndiv):
        x = center[0] + radius * cos(theta0 + i*d_theta)
        y = center[1] + radius * sin(theta0 + i*d_theta)

        pygame.draw.line(screen, color, center, (x, y), 8)

#fill_arc((400, 400), 200, 0, 2*pi/5, red)
#fill_arc((400, 400), 200, 2*pi/5, 4*pi/5, green)

def close_game():
    print("Beendet.")
    pygame.quit()
    run = False
    quit()

def deg2rad(x):
    return x * math.pi / 180

pygame.time.Clock()

pygame.init()

green = (0, 139, 0)            

# initialize font; must be called after 'pygame.init()' to avoid 'Font not Initialized' error
smallfont = pygame.font.SysFont("monospace", 18)
smallAfont = pygame.font.SysFont("Arial", 18)
boldfont = pygame.font.SysFont("Arial Black", 18)
largefont = pygame.font.SysFont("Arial Black", 80)

ScreenX = 800
ScreenY = 600

width = ScreenX - 100
height = ScreenY - 200

Stadionname = "Allianz-Arena"
Heimmannschaft = "SC Rapid Wien"
Kapazitaet = int(28530)
Vermoegen = int(6240000)

#Tribuenen=[("W", "West", 3), ("S", "Süd", 3), ("O", "Ost", 3), ("N", "Nord", 5)]
#Tribuenen=[["W", "West", 3], ["S", "Süd", 3], ["O", "Ost", 3], ["N", "Nord", 5]]
Tribuenen=["W", "West", 1, 125000, 6000, 1200, "S", "Süd", 1, 30000, 8000, 2000, "O", "Ost", 1, 125000, 6000, 1200, "N", "Nord", 1, 450000, 8530, 1600]

screen = pygame.display.set_mode((ScreenX, ScreenY))
#pygame.display.toggle_fullscreen()

#buttonSkip = Button(screen, 100, 500-20, 200-10, 40, text="Überspringen", font=smallfont, onClick=skip_game)

buttonPause = Button(screen, 350, 550, 200-10, 40, text="Ausbauen", font=smallfont, onClick=close_game,
    inactiveColour=(186, 214, 177), hoverColour=(100, 200, 20), pressedColour=(0, 200, 20))
buttonClose = Button(screen, 550, 550, 200-10, 40, text="Schließen", font=smallfont, onClick=close_game,
    inactiveColour=(186, 214, 177), hoverColour=(100, 200, 20), pressedColour=(0, 200, 20))

##s = pygame.display.get_surface()
rect = pygame.Rect(10,10,100,100)
#s.fill(pygame.Color("red"),r)
#screen.blit(s, r)

i = pygame.image.load(r'assets/blue-glossy-button-blank-icon-square-empty-shape-vector-12937816.jpg')
i = pygame.transform.scale(i, (100, 100))

imgSpielfeld = pygame.image.load(r'assets/240_F_195394534_OjXNWoUvzB92C7JAyiN1JcLvUWre7AvM.jpg')

run = True
while run:

    # render text
    #labelSM = myfont.render("Spielminute: " + str(Spielminute), 1, (0,0,0))
    #labelVE = myfont.render("Verbleibend: " + str(Verbleibend), 1, (0,0,0))
    #labelBB = myfont.render("Ballbesitz: " + str(BallbesitzA) + "% / " + str(BallbesitzB) + "%", 1, (0,0,0))
    #labelTS = myfont.render("Torschüsse: 6 / 4", 1, (0,0,0))
    #labelGK = myfont.render("Gelbe Karten: 1 / 0", 1, (0,0,0))
    #labelRK = myfont.render("Rote Karten: 0 / 1", 1, (0,0,0))
    #labelTO = myfont.render("Tore: " + str(ToreA) + " / " + str(ToreB), 1, (0,0,0))

    #labelA = largefont.render(str(ToreA), True, (0, 0, 0))
    #labelB = largefont.render(str(ToreB), True, (0, 0, 0))
    labelStadion = largefont.render(Stadionname, True, (0, 0, 0))
    labelKapazitaet = smallfont.render("Kapazität " + locale.format_string('  %.0f', Kapazitaet, grouping = True) + ' P', True, (0, 0, 0)) # \U0001F61B
    labelVermoegen = smallfont.render("Vermögen " + locale.format_string('%.0f', Vermoegen, grouping = True, monetary=False) + ' €', True, (0, 0, 0))
    labelHeimmannschaft = smallfont.render("Heimmannschaft " + str(Heimmannschaft), True, (0, 0, 0))

    events = pygame.event.get()
    for event in events:
        if event.type == pygame.QUIT:
            pygame.quit()
            run = False
            quit()
        if event.type == pygame.KEYDOWN:
            #if event.key == pygame.K_s:
                #print(Tribuenen[1][2])
            try:
                Tr = Tribuenen[Tribuenen.index(pygame.key.name(event.key).upper())+1]
                St = Tribuenen[Tribuenen.index(pygame.key.name(event.key).upper())+2]
                Ko = Tribuenen[Tribuenen.index(pygame.key.name(event.key).upper())+3]
                Ka = Tribuenen[Tribuenen.index(pygame.key.name(event.key).upper())+4]
                Er = Tribuenen[Tribuenen.index(pygame.key.name(event.key).upper())+5]
                if St <= 3 and Kapazitaet < 120000:
                    print(f"Kosten für Tribüne {Tr:4s} von {Ka} um {Er} auf Kapazität {Ka+Er} / Ausbaustufe {St}: {Ko} ")
                    Kapazitaet += Ka
                    Vermoegen -= Ko
                    Ka = Ka+Er
                    St += 1
                    Tribuenen[Tribuenen.index(pygame.key.name(event.key).upper())+2] = St
                    Tribuenen[Tribuenen.index(pygame.key.name(event.key).upper())+4] = Ka
                #print(pygame.key.name(event.key))
            except:
                pass

    screen.fill(green)
    #screen.blit(labelSM, (100, 150))
    #screen.blit(labelVE, (530, 150))

    #screen.blit(labelBB, (280, 230))
    #screen.blit(labelTS, (280, 280))
    #screen.blit(labelGK, (280, 330))
    #screen.blit(labelRK, (280, 380))
    #screen.blit(labelTO, (280, 430))

    #pygame.draw.rect(screen, pygame.Color("red"), rect, width=2, border_radius=3)
    #pygame.display.flip()

    #screen.blit(i, (100+180, 10))
    #screen.blit(i, (width-180, 10))

    #screen.blit(imgSpielfeld, (ScreenX / 2 - imgSpielfeld.get_width() / 2, 180))
    screen.blit(imgSpielfeld, (220, 180))

    screen.blit(labelStadion, (ScreenX / 2 - labelStadion.get_width() / 2, 0))
    screen.blit(labelKapazitaet, (100, 510))
    screen.blit(labelVermoegen, (100, 530))
    screen.blit(labelHeimmannschaft, (ScreenX - labelHeimmannschaft.get_width() - 100, 510))

    #points = [(100, 100), (700, 100), (700,500), (100,500)]
    #rect_filled = pygame.Surface((600, 400))
    #l1 = pygame.draw.lines(screen, (0,0,0), True, points, width=2)
    #screen.blit(rect_filled, screen, area=(0, 0, 100, 100))

    pygame.draw.line(screen, (0,0,0), (200, 100), (600, 100), width=1)
    pygame.draw.line(screen, (0,0,0), (100, 200), (100, 400), width=1)
    pygame.draw.line(screen, (0,0,0), (200, 500), (600, 500), width=1)
    pygame.draw.line(screen, (0,0,0), (700, 200), (700, 400), width=1)

    # aussenkreise
    r = pygame.Rect(500, 100, 200, 200)
    a1 = dr.arc(screen, (0,0,0), r, 0, deg2rad(90),width=1)
    r = pygame.Rect(500, 300, 200, 200)
    a1 = dr.arc(screen, (0,0,0), r, deg2rad(270), deg2rad(0),width=1)
    r = pygame.Rect(100, 300, 200, 200)
    a1 = dr.arc(screen, (0,0,0), r, deg2rad(180), deg2rad(270),width=1)
    r = pygame.Rect(100, 100, 200, 200)
    a1 = dr.arc(screen, (0,0,0), r, deg2rad(90), deg2rad(180),width=1)

    # sektoren

    rO = pygame.draw.rect(screen, pygame.Color('orange'), [220+360+2, 423-242, 40, 240])
    labelO = boldfont.render("  O", 1, pygame.Color('black')).convert_alpha(screen)
    screen.blit(labelO, rO)
    rW = pygame.draw.rect(screen, pygame.Color('green'), [220-40-2, 423-242, 40, 240])
    labelN = boldfont.render("  W", 1, pygame.Color('black')).convert_alpha(screen)
    screen.blit(labelN, rW)
    rS = pygame.draw.rect(screen, pygame.Color('red'), [220, 423, 359, 40])
    labelN = boldfont.render("  S", 1, pygame.Color('black')).convert_alpha(screen)
    screen.blit(labelN, rS)
    for anz in range(4):
        rx = pygame.draw.rect(screen, pygame.Color('blue'), [220+(anz*90), 138, 87, 40])
        # render text
        labelN = boldfont.render("     N" + str(anz+1), True, pygame.Color('white')).convert_alpha(screen)
        screen.blit(labelN, rx)
        #screen.blit(labelSM, (220+(anz*90) + rx.width / 2, 138))

    #pygame.draw.rect(screen, pygame.Color('blue'), [220+100+100, 140, 100, 40])
    #pygame.draw.rect(screen, pygame.Color('blue'), [220+100+100, 140, 100, 40])
    #pygame.display.flip()

    #r1 = pygame.Rect(left, top, width, height)
    #s1 = pygame.Surface((200, 200))
    #pygame.draw.rect(s1, (0,0,0), r1)
    #r1.bottom = 200
    #screen.blit(s1,r1)

    # innenkreise
    r = pygame.Rect(220+360+2-40, 423-242-40, 80, 80)
    #a1 = dr.arc(screen, pygame.Color('darkorchid'), r, 0, deg2rad(90),width=100)

    fill_arc(center=(220+360+2, 423-242-3), radius=40, theta0=deg2rad(270), theta1=deg2rad(360), color=pygame.Color('turquoise3'))
    fill_arc(center=(220+360+2, 423), radius=40, theta0=deg2rad(0), theta1=deg2rad(90), color=pygame.Color('turquoise3'))
    fill_arc(center=(220-2, 423-242-3), radius=40, theta0=deg2rad(180), theta1=deg2rad(270), color=pygame.Color('turquoise3'))
    fill_arc(center=(220-2, 423-2), radius=40, theta0=deg2rad(90), theta1=deg2rad(180), color=pygame.Color('turquoise3'))

    #rOb = pygame.draw.rect(screen, pygame.Color('darkorchid'), [220+360+2, 423-242-40, 0, 0])
    #labelO = boldfont.render("O", 1, pygame.Color('black')).convert_alpha(screen)
    #screen.blit(labelO, rOb)

    pygame_widgets.update(events)
    pygame.display.update()
    pygame.time.delay(10)
    #time.sleep(1)

pygame.time.delay(3000)
