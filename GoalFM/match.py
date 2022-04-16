import pygame, pygame_menu, pygame_widgets
from pygame_widgets.progressbar import ProgressBar
from pygame_widgets.button import Button
import time
import random
import math
import os, sys
import espeakng
from num2words import num2words

class Match:

    def skip_game(self):
        print("Skipped")
        pygame.quit()
        run = False
        quit()

    def pause_game(self):
        global run
        print("Pause.")
        #run = False
        #pygame.quit()
        #run = False
        #quit()

    def close_game(self):
        print("Beendet.")
        pygame.quit()
        run = False
        quit()

    def run():

        startTime = time.time()

        pygame.time.Clock()

        #pygame.init()

        pygame.font.init()

        pygame.mixer.init()

        green = (0, 139, 0)  

        # initialize font; must be called after 'pygame.init()' to avoid 'Font not Initialized' error
        myfont = pygame.font.SysFont("monospace", 18)
        largefont = pygame.font.SysFont("Arial Black", 80)

        anpfiff = pygame.mixer.Sound(r'audio/218318__splicesound__referee-whistle-blow-gymnasium.wav')
        torpfiff = pygame.mixer.Sound(r'audio/40754__tommon__one-blast-whistle.wav')
        abpfiff = pygame.mixer.Sound(r'audio/90743__pablo-f__referee-whistle.wav')

        stadion = pygame.mixer.music.load(r'audio/163274__cuauh89__stadium-sound.wav')

        ScreenX = 800
        ScreenY = 800

        width = ScreenX - 200
        height = ScreenY - 200

        Spielminute = int(0)
        Loop = 0
        Verbleibend = 90 - Spielminute

        screen = pygame.display.set_mode((ScreenX, ScreenY))

        #menu = pygame_menu.Menu('title', width, height)

        #pb1 = menu.add.progress_bar('title',50)
        #pb1 = pygame_widgets.progressbar('title',50)

        Spiellaenge = 25 # 10 # in Sekunden

        BallbesitzA = int(50); BallbesitzKumA = int(0)
        BallbesitzB = int(50); BallbesitzKumB = int(0)

        ToreA = 0; HToreA = 0; PunkteA = 0
        ToreB = 0; HToreB = 0; PunkteB = 0

        Sieger = ""

        TorschuetzeA = "Schaub"; TeamA = "Rapid Wien" # Team A is immer Heimmannschaft
        TorschuetzeB = "Lewandowsky"; TeamB = "FC Bayern München"

        # spielzeit
        #progressBar = ProgressBar(screen, 100, 100, width, 40, lambda: 1 - (time.time() - startTime) / Spiellaenge, curved=False)
        progressBar = ProgressBar(screen, 100, 180, width, 40, lambda: Verbleibend / 100 * 1.1, curved=False)

        # ballbesitz
        progressBar = ProgressBar(screen, 100, 250, width-(width / 2)-2, 20, lambda: 1 - (BallbesitzA / 100), curved=False, completedColour=(100, 100, 100), incompletedColour=(0, 200, 0))
        progressBar = ProgressBar(screen, 100+(width / 2)+4, 250, width-(width / 2)-2, 20, lambda: BallbesitzB / 100, curved=False)

        # torschüsse
        progressBar = ProgressBar(screen, 100, 300, width-(width / 2)-2, 20, lambda: 1 - (60 / 100), curved=False, completedColour=(100, 100, 100), incompletedColour=(0, 200, 0))
        progressBar = ProgressBar(screen, 100+(width / 2)+4, 300, width-(width / 2)-2, 20, lambda: 40 / 100, curved=False)

        # gelbe karten
        progressBar = ProgressBar(screen, 100, 350, width-(width / 2)-2, 20, lambda: 1, curved=False, completedColour=pygame.Color('yellow'))
        progressBar = ProgressBar(screen, 100+(width / 2)+4, 350, width-(width / 2)-2, 20, lambda: 0, curved=False, completedColour=pygame.Color('yellow'))

        # rote karten
        progressBar = ProgressBar(screen, 100, 400, width-(width / 2)-2, 20, lambda: 0, curved=False, completedColour=pygame.Color('red'))
        progressBar = ProgressBar(screen, 100+(width / 2)+4, 400, width-(width / 2)-2, 20, lambda: 1, curved=False, completedColour=pygame.Color('red'))

        ##s = pygame.display.get_surface()
        rect = pygame.Rect(10,10,100,100)
        #s.fill(pygame.Color("red"),r)
        #screen.blit(s, r)
        i = pygame.image.load(r'assets/blue-glossy-button-blank-icon-square-empty-shape-vector-12937816.jpg')
        i = pygame.transform.scale(i, (100, 100))

        imgSpielfeld = pygame.image.load(r'assets/240_F_195394534_OjXNWoUvzB92C7JAyiN1JcLvUWre7AvM.jpg')

        LogoA = pygame.image.load(r'logos/fcb.png').convert_alpha()
        LogoA = pygame.transform.scale(LogoA, (100, 100))

        LogoB = pygame.image.load(r'logos/paris.png').convert_alpha()
        LogoB = pygame.transform.scale(LogoB, (100, 100))

        #labelColon = largefont.render(":", True, (0, 0, 0))

        pygame.mixer.music.play()

        pygame.mixer.music.set_volume(0.1)

        speaker = espeakng.ESpeakNG(volume=200,voice="mb-de6",speed=190)

        anpfiff.play()
        print("Anpfiff.")
        speaker.say("Anpfiff.")

        run = True
        while run:

            # render text
            labelSM = myfont.render("Spielminute: " + str(Spielminute), 1, (0,0,0))
            labelVE = myfont.render("Verbleibend: " + str(Verbleibend), 1, (0,0,0))
            labelBB = myfont.render("Ballbesitz: " + str(BallbesitzA) + "% / " + str(BallbesitzB) + "%", 1, (0,0,0))
            labelTS = myfont.render("Torschüsse: 6 / 4", 1, (0,0,0))
            labelGK = myfont.render("Gelbe Karten: 1 / 0", 1, (0,0,0))
            labelRK = myfont.render("Rote Karten: 0 / 1", 1, (0,0,0))
            labelTO = myfont.render("Tore: " + str(ToreA) + " / " + str(ToreB), 1, (0,0,0))

            labelA = largefont.render(str(ToreA), True, (0, 0, 0))
            labelB = largefont.render(str(ToreB), True, (0, 0, 0))
            labelScore = largefont.render(str(ToreA) + " : " + str(ToreB), True, (0, 0, 0))

            events = pygame.event.get()
            for event in events:
                if event.type == pygame.QUIT:
                    abpfiff.play()
                    pygame.quit()
                    run = False
                    quit()
                    
            screen.fill(green)
            #pygame.draw.rect(screen, pygame.Color("white"), (0, 0, 800, 200))

            buttonSkip = Button(screen, 100, 500-20, 200-10, 40, text="Überspringen", font=myfont, onClick=Match.skip_game,
                inactiveColour=(186, 214, 177), hoverColour=(100, 200, 20), pressedColour=(0, 200, 20))
            buttonPause = Button(screen, 300, 500-20, 200-10, 40, text="Pause / Trainer", font=myfont, onClick=Match.pause_game,
                inactiveColour=(186, 214, 177), hoverColour=(100, 200, 20), pressedColour=(0, 200, 20))
            buttonClose = Button(screen, 500, 500-20, 200-10, 40, text="Schließen", font=myfont, onClick=Match.close_game,
                inactiveColour=(186, 214, 177), hoverColour=(100, 200, 20), pressedColour=(0, 200, 20))

            screen.blit(labelSM, (100, 150))
            screen.blit(labelVE, (530, 150))

            screen.blit(labelBB, (280, 230))
            screen.blit(labelTS, (280, 280))
            screen.blit(labelGK, (280, 330))
            screen.blit(labelRK, (280, 380))
            screen.blit(labelTO, (280, 430))

            #pygame.draw.rect(screen, pygame.Color("red"), rect, width=2, border_radius=3)
            #pygame.display.flip()

            screen.blit(i, (100+180, 10))
            screen.blit(i, (width-180, 10))

            screen.blit(imgSpielfeld, (ScreenX / 2 - imgSpielfeld.get_width() / 2, 550))

            if(Loop % 10 == 0):
                #print(Loop)
                for player in range(1, 11):
                    Px = random.randint(55, 355)
                    Py = random.randint(5, 235)
                    pygame.draw.circle(screen, pygame.Color("red"), (220 + Px, 550 + Py), radius=5)
                    #pygame.draw.circle(imgSpielfeld, pygame.Color("red"), (Px, Py), radius=5,)
                #pygame.display.flip() # führt zu flimmern
                #pygame.display.update()
                pygame.time.delay(10)

            screen.blit(labelScore, (ScreenX / 2 - labelScore.get_width() / 2, 0))

            #screen.blit(labelA, (100+180, 10))
            #screen.blit(labelB, (width-180, 10))

            screen.blit(LogoA, (100, 10))
            screen.blit(LogoB, (width, 10))

            #pygame.time.wait(100)
            #Spielminute = round((time.time() - startTime) / (Spiellaenge * 1.1) * 100, 2)

            if(Spielminute == 45+1):
                print("Halbzeitpause - " + str(Spielminute-1) + ". Minute.")
                torpfiff.play()
                speaker.say("Halbzeit")

                HToreA = ToreA
                HToreB = ToreB

                BallbesitzA = 50
                BallbesitzB = 50

                #run = False
                #pygame.time.delay(3000) # milliseconds

                print("10 Minuten Pause.")
                time.sleep(10) # secs
                anpfiff.play()
                #run = True
                Loop += 10
                Spielminute += 2

            if(Loop == 900):
            #if(Verbleibend == 0):
                print("Zeit ist vorbei") 
                run = False
                # pfiff erst ausserhalb der schleife

                if(ToreA > ToreB):
                    PunkteA += 3
                    Sieger = " für " + TeamA
                if(ToreB > ToreA):
                    PunkteB += 3
                    Sieger = " für " + TeamB
                if(ToreA == ToreB):
                    PunkteA = 1
                    PunkteB = 1
                    Sieger = "unentschieden zwischen " + TeamA + " und " + TeamB

                print("Ballbesitz: " + str(math.ceil(BallbesitzKumA / Loop)) + "% : " + str(math.ceil(BallbesitzKumB / Loop)) + "%")
                print("Endstand: " + str(ToreA) + " : " + str(ToreB) + ' (' + str(HToreA) + " : " + str(HToreB) + ')')
                print("Punkte: " + str(PunkteA) + " : " + str(PunkteB))

                print("Script lief " + str(round(time.time() - startTime, 2)) + " Sekunden.")

                txt = "Endstand: " + str(ToreA) + " zu " + str(ToreB) + Sieger
                speaker.say(txt)

            if(random.randint(0, 1) == 0):
                #print(0)
                BallbesitzA += 2 # 1 bei time()
                BallbesitzB -= 2 # 1 bei time()
            else:
                #print(1)
                BallbesitzA -= 2
                BallbesitzB += 2

            BallbesitzKumA += BallbesitzA
            BallbesitzKumB += BallbesitzB

            if(BallbesitzA >= 100):
                ToreA += 1
                BallbesitzA = 50
                BallbesitzB = 50
                torpfiff.play()
                Satz = "Tor (" + TeamA + ") durch " + TorschuetzeA + " in der " + str(num2words(str(int(Spielminute)), to='ordinal', lang='de') + 'n') + " Spielminute."
                SatzA = "Tor (" + TeamA + ") durch " + TorschuetzeA + " in der " + str(Spielminute) + ". Spielminute."
                print(SatzA)
                #pygame.mixer.music.set_volume(0.25)
                #os.system("espeak-ng -vde '" + Satz + "' -s 150")
                speaker.say(Satz)
                time.sleep(3)

            if(BallbesitzB >= 100):
                ToreB += 1
                BallbesitzA = 50
                BallbesitzB = 50
                torpfiff.play()
                Satz = "Tor (" + TeamB + ") durch " + TorschuetzeB + " in der " + str(num2words(str(int(Spielminute)), to='ordinal', lang='de')) + 'n' + " Spielminute."
                SatzA = "Tor (" + TeamB + ") durch " + TorschuetzeB + " in der " + str(Spielminute) + ". Spielminute."
                print(SatzA)
                #pygame.mixer.music.set_volume(0.25)
                #os.system("espeak-ng -vde '" + Satz + "' -s 150")
                speaker.say(Satz)
                time.sleep(3)

            #if(random.randint(1, 100) == 50):
                #anpfiff.play()
                #print("Foul.")

            Loop += 1
            Spielminute = int(Loop / 10)
            Verbleibend = 90 - Spielminute

            pygame_widgets.update(events)
            pygame.display.update()
            pygame.time.delay(10)
            #time.sleep(1)

        abpfiff.play()
        pygame.time.delay(3000)

    #pygame_widgets.update(events)
    #pygame.display.update()
