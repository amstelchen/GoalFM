import pygame, pygame_menu, pygame_widgets
from pygame_widgets.button import Button
import pygame.draw as dr

# from .farben import *
#import farben

from .colors import *

class Intro:

    def close_game():
        print("Beendet.")
        pygame.quit()
        run = False
        quit()

    def run():

        #pygame.init()

        pygame.font.init()
        clock = pygame.time.Clock()

        boldfont = pygame.font.SysFont("Arial Black", 14)
        largefont = pygame.font.SysFont("Arial Black", 80)
        mediumfont = pygame.font.SysFont("Arial Black", 40)

        ScreenX = 1920
        ScreenY = 1080

        alpha = 0
        alpha_change = 1

        ProgramName = " Fussball-Manager "

        modes = pygame.display.list_modes()
        #print(modes)
        #screen = pygame.display.set_mode((ScreenX, ScreenY))
        screen = pygame.display.set_mode(modes[0])
        #print(pygame.display.get_window_size())
        pygame.display.toggle_fullscreen()

        screen.fill(Colors.black)
        #imgStudio = pygame.image.load("flags/" + "at.png").convert_alpha()

        text = "Studio 4"
        imgStudio = largefont.render(text, True, Colors.white)
        text = _("presents")
        imgPresents = mediumfont.render(text, True, Colors.white)

        font_riesig = pygame.font.Font(pygame_menu.font.FONT_OPEN_SANS_BOLD, 120)
        text_riesig = font_riesig.render(" GOAL ", True, Colors.white, Colors.green)

        box1 = pygame.Surface((text_riesig.get_width() + 100, text_riesig.get_height()))
        box1.blit(text_riesig, (0, 0))

        font_gross = pygame.font.Font(pygame_menu.font.FONT_OPEN_SANS_BOLD, 32)
        text_gross = font_gross.render(ProgramName.upper(), True, Colors.white, Colors.green)

        box2 = pygame.Surface((text_riesig.get_width(), text_gross.get_height()))
        box2.fill(Colors.green)
        box2.blit(text_gross, ((text_riesig.get_width() - text_gross.get_width()) / 2, 0))

        filename = "music/The-Games_Looping.mp3"
        pygame.mixer_music.load(filename,"mp3") # "ogg")
        #if audiostate == 1:
        pygame.mixer_music.play(-1)

        run = True
        while run:

            clock.tick(60)

            events = pygame.event.get()
            for event in events:
                if event.type == pygame.QUIT:
                    #close_game()
                    quit()

                if event.type == pygame.KEYDOWN:
        
                        if event.key == pygame.K_x and event.mod == pygame.KMOD_CTRL:
                            pygame.quit()
                            sys.exit()
                    
                        if event.key == pygame.K_ESCAPE:
                            run = False

                        if event.key == pygame.K_f:
                            pygame.display.toggle_fullscreen()

            alpha += alpha_change
            if not 0 <= alpha <= 255:
                alpha_change *= -1
            #else:
            #    run = False
            alpha = max(0, min(alpha, 255))
            #print(alpha)

            if alpha == 0:
                #pygame.quit()
                run = False

            screen.fill(0)

            alphaimgStudio = imgStudio.copy()
            alphaimgStudio.set_alpha(alpha)    
            alphaimgPresents = imgPresents.copy()
            alphaimgPresents.set_alpha(alpha)    

            screen.blit(alphaimgStudio, (ScreenX / 2 - imgStudio.get_width() / 2, ScreenY / 2 - imgStudio.get_height() / 2))
            screen.blit(alphaimgPresents, (ScreenX / 2 - imgPresents.get_width() / 2, ScreenY / 2 - imgPresents.get_height() / 2 + 100))
            
            pygame.display.flip()

        alpha_change = 1
        alpha = 0

        pygame.event.clear(pygame.KEYDOWN, True)
        events = None
        #pygame.time.delay(500)

        #pygame.mixer_music.play(-1)

        run = True
        while run:

            clock.tick(60)

            events = pygame.event.get()
            for event in events:
                if event.type == pygame.QUIT:
                    close_game()

                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                                alpha = 255
                                #final = True
                                run = False

            alpha += alpha_change
            #if not 0 <= alpha <= 255:
            #    alpha_change *= -1
            #else:
            #    run = False
            alpha = max(0, min(alpha, 255))
            #print(alpha)

            if alpha == 255:
                #pygame.quit()
                run = False

            screen.fill(0)

            alpha_image = box1.copy()
            alpha_image.set_alpha(alpha)    
            #screen.blit(alpha_image, (0, 0))
            screen.blit(alpha_image, (ScreenX / 2 - text_riesig.get_width() / 2, ScreenY / 2 - text_riesig.get_height() / 2))
            
            pygame.display.flip()

        alpha = 0
        alpha_change = 1

        pygame.event.clear()

        run = True
        while run:

            #if final == True:
            #    alpha = 255

            clock.tick(60)

            events = pygame.event.get()
            for event in events:
                if event.type == pygame.QUIT:
                    close_game()

                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                                alpha = 255
                                run = False

            alpha += alpha_change
            #if not 0 <= alpha <= 255:
            #    alpha_change *= -1
            #else:
            #    run = False
            alpha = max(0, min(alpha, 255))
            #print(alpha)

            if alpha == 255:
                #pygame.time.delay(3000)
                run = False

            alpha_image2 = box2.copy()
            alpha_image2.set_alpha(alpha)    
            screen.blit(alpha_image2, (ScreenX / 2 - text_riesig.get_width() / 2, ScreenY / 2 + text_riesig.get_height() / 2))
            pygame.display.flip()

#pygame.quit()