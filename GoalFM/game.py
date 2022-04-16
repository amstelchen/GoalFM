#!/bin/python
# -*- coding: utf-8 -*-

import sys, os
import datetime
import gettext
import configparser
import argparse
from gi.repository import GLib
from pathlib import Path

from pygame.locals import *

os.environ['PYGAME_HIDE_SUPPORT_PROMPT']='1'

import pygame, pygame_menu, pygame_widgets
from pygame_widgets.button import Button
from pygame_widgets.button import ButtonArray

from .sqlite3db import *
from .colors import *
from .sqlite3db import *

#global playername, playercash, season, quarter
#global xdg_config_file

audiostate = 1

#_ = gettext.gettext
#gettext1 = gettext.translation('base', localedir='locales', languages=['de'])
#gettext1.install()
#_ = gettext.gettext # Deutsch

main_theme = pygame_menu.themes.THEME_GREEN.copy()
main_theme.title_background_color=(0, 139, 0)
main_theme.widget_font_color = Colors.black

def AssetPath(path):
    return os.path.join(os.path.dirname(__file__).replace('GoalFM/GoalFM/', 'GoalFM/', 1), r'assets/football-200x200.png')

class Config:

    def __init__(self, playername):

        self.Module = "GoalFM"
        self.xdg_config_dir = ""
        self.xdg_config_file = ""

        # konfigurationsdatei verwalten ###############################################

        #xdg_config_dir = os.path.join(GLib.get_user_config_dir(), Path(__file__).stem)
        #xdg_config_file = os.path.join(xdg_config_dir, Path(__file__).stem) + ".conf"

        self.xdg_config_dir = os.path.join(GLib.get_user_config_dir(), self.Module)
        self.xdg_config_file = os.path.join(self.xdg_config_dir, self.Module + ".conf")

        if os.path.exists(self.xdg_config_file):
            print(_("Using") + " " + self.xdg_config_file + ".")
            #Config.load_config(self.xdg_config_file)
        else:
            print(_("Config file") + " " + self.xdg_config_dir + " " + "not found." + " " + _("Loading sane defaults."))

        #self.config_file = config_file
        #self.audiostate = audiostate
        #self.playername = playername
        #self.playercash = playercash
        #self.season = season
        #self.quarter = quarter
    
    def save_config(self, audiostate, playername, playercash, season, quarter):

        config = configparser.ConfigParser()
        config['Settings'] = {}
        config['Settings']['Resolution'] = str(pygame.display.get_window_size())
        config['Settings']['Audio'] = str(audiostate)
        config['Settings']['playername'] = str(playername)
        config['Settings']['playercash'] = str(playercash)
        config['Settings']['season'] = str(season) + "Q" + str(quarter)
        with open(self.xdg_config_file, 'w') as configfile:
            config.write(configfile)
            print("Game saved.")

    def load_config(self):
        #global playername, playercash, season, quarter
        #global xdg_config_file, audiostate

        config = configparser.ConfigParser()
        config.read(str(self.xdg_config_file))
        audiostate = config['Settings']['Audio']
        playername = config['Settings']['playername']
        playercash = int(config['Settings']['playercash'])
        season = int(config['Settings']['season'].split('Q')[0])
        quarter = int(config['Settings']['season'].split('Q')[1])
        print("Game loaded.")
        return Config()

class Box:

    def __init__(self, screen, text, x, y, width=260, height=315):
        self.text = text
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.screen = screen

    def draw(self):
        pygame.draw.rect(self.screen, Colors.black, [self.x, self.y, self.width, self.height], 2, 5)
        font_klein = pygame.font.Font(pygame_menu.font.FONT_OPEN_SANS_BOLD, 16)
        text_box = font_klein.render(self.text, True, Colors.black) # black)
        #text_boxRect = text_box.get_rect()
        #text_boxRect.left = boxRect.left + 10 # (20, 20)
        #text_boxRect.top = boxRect.top + 10 # (20, 20)
        self.screen.blit(text_box, (self.x + 10, self.y + 10)) #, text_boxRect)

class Flags:

    def __init__(self, screen, text, pos_x, pos_y, width=3, height=5):
        self.text = text
        self.pos_x = pos_x
        self.pos_y = pos_y
        self.width = width
        self.height = height
        self.screen = screen

    def draw(self):
        printflags = 0
        countries = ['AT', 'DE', 'CH', 'HU', 'DK', 'BE', 'GB', 'IT', 'ES', 'PT', 'UA', 'GR', 'FR', 'LU', 'LT']; i = 0
        scaleX = 80; scaleY = 50

        for x in range(self.width):
            for y in range(self.height):
                image1 = pygame.image.load("flags/" + countries[i].lower() + ".png")
                image1 = pygame.transform.scale(image1,(scaleX, scaleY))
                self.screen.blit(image1, (self.pos_x + x * scaleX + x * 3, self.pos_y + y * scaleY + y * 3))
                i+=1
        
        #if printflags == 1:
        #   print(str(i) + " " + _("Flags loaded."))
        #printflags = 0

class GameLoop:

    # bilder laden ################################################################

    #image = pygame.image.load(r'C:\Users\user\Pictures\geek.jpg')
    image_ball = pygame.image.load(AssetPath(r'assets/football-200x200.png'))
    image_salary = pygame.image.load(r'assets/salary-32x32.png')

    image_v1 = pygame.image.load(r'images/1-footballer-silhouette-10.png',"png")
    image_v5 = pygame.image.load(r'images/5-football-player-silhouett.jpg')

    image_v1 = pygame.transform.scale(image_v1,(200, 200))
    image_v5 = pygame.transform.scale(image_v5,(200, 200))

    programIcon = pygame.image.load('assets/footballmanager.png')
    pygame.display.set_icon(programIcon)

    #SpielerIcon = pygame.image.load(r'images/avatar1.png')
    #SpielerIcon = pygame.transform.scale(SpielerIcon,(100,113))

    SpielerIcon = pygame_menu.BaseImage(r'images/avatar1.png')
    SpielerIcon.resize(100, 113)

    def __init__(self):
        self.audiostate = 1
        self.playername = "Michael"

    def about_the_game(self):
        global ProgramName

        #pmenu = pygame_menu.Menu(_("About") + " " + ProgramName, width=300, height=300)
        #pmenu = pygame_menu.widgets.Frame(width=300, height=300, orientation=pygame_menu.locals.ORIENTATION_VERTICAL)
        #pmenu.show()

    def open_menu():
        menu.mainloop(self.screen)

    def open_team():
        #pmenu = pygame_menu.widgets.Frame(width=300, height=300, orientation=pygame_menu.locals.ORIENTATION_VERTICAL)
        #pmenu_menu.widgets.Widget
        #pmenu.draw(self.screen)
        #pygame_widgets.widget.
        #srf = pygame.surface.Surface((600,400))
        #srf.blit(srf,self.screen,area=(300,300))
        #rect = pygame.draw.rect(self.screen,(0, 139, 0),(self.screen.get_width() / 2 - 300, self.screen.get_height() / 2 - 200,600,400),2,5) # (0,0,0)
        #self.screen.fill((0, 139, 0),rect=rect)
        #pygame_widgets.label=""

        theme_team = pygame_menu.themes.THEME_GREEN.copy()
        theme_team.title_background_color=(0, 139, 0)
        theme_team.widget_font_color = Colors.black
        theme_team.widget_alignment = pygame_menu.locals.ALIGN_LEFT
        #theme_team.widget_font = pygame.font.Font(pygame_menu.font.FONT_OPEN_SANS, 20)
        theme_team.widget_font = pygame.font.SysFont("Noto Sans Mono", 22)
        #theme_team.widget_font = pygame.font.SysFont("/usr/share/fonts/noto/NotoSansMono-Thin.ttf", 28)

        spielerkarte = pygame_menu.Menu(title=_('Spieler'), width=800, height=600, theme=theme_team)

        #print(spielerkarte.get_value())
        #for i in spielerkarte.get_input_data():
        #    print(str(i))

        spielerkarte.add.label('Bernhard Unger',
            align=pygame_menu.locals.ALIGN_LEFT, font_size=20)
        #spielerkarte.add.label(spielerkarte.get_input_data())

        #spielerkarte.add.image(r'images/avatar1.png',scale=(100,113))
        spielerkarte.add.image(GameLoop.SpielerIcon, align=pygame_menu.locals.ALIGN_LEFT, widget=600)

        #t = spielerkarte.add.table("hallo")
        #t = pygame_menu.widgets.Table("aaa")
        #t.set_border(3, Colors.red)
        #t.adcells = ["a", "b"]
        #r = t.add_row(cells)
        #p1 = pygame_widgets.progressbar("aaa")
        #p1 = pygame_menu.widgets.ProgressBar("...")
        #c = [pygame_widgets.progressbar("wi",default=100), "b", "c"]
        #c = [p1, "a"]

        conn = connect_goal_db()
        rows = select_stats(conn)
        for row in rows:
            spielerkarte.add.progress_bar(str(row[1]).rjust(30),default=row[2],width=200) #,default=str(row[2]))

        #spielerkarte.add.progress_bar("Einsatzfreude".rjust(20),default=72,width=200,height=30,inactiveColour=Colors.green,progress_text_enabled=False)
        #spielerkarte.add.progress_bar("Grundfitness".ljust(20),default=96,width=200,height=30,inactiveColour=Colors.green,progress_text_enabled=False)
        #spielerkarte.add.progress_bar("Flanken".ljust(20),default=69-30,width=200,height=30,inactiveColour=Colors.red,progress_text_enabled=False)
        #spielerkarte.add.progress_bar("Kopfballtechnik".ljust(20),default=97,width=200,height=30,inactiveColour=Colors.black,progress_text_enabled=False)
        #spielerkarte.add.progress_bar("Moral".ljust(20),default=84,width=200,height=30,inactiveColour=Colors.green,progress_text_enabled=False)

        spielerkarte.add.vertical_margin(30)
        spielerkarte.add.button(_('Close'), pygame_menu.events.BACK)

        #spielerkarte.mainloop(pygame.display.get_surface(), clear_surface=False,widget_alignment=pygame_menu.locals.ALIGN_LEFT)

        pmenu_team = pygame_menu.Menu(_("Team"), width=800, height=600, theme=theme_team)
        pmenu_team.add.vertical_margin(30)
        conn = connect_goal_db()
        rows = select_all_team(conn)
        #pmenu_team.add.label('bla')
        for row in rows:
            #print(str(row))
            #zeile = row.str().format("{[0]} {:<30[1]}")
            spielername = str(row[2]) + ' ' + str(row[3])
            spieler = '  ' + str(row[1]).rjust(2,' ') + '  ' + spielername.ljust(28,' ') + row[5].ljust(10,' ') + \
                ' ' + str(row[7]).rjust(3+1) + ' ' + str(row[8]).rjust(2+1) + ' ' + str(row[9]).rjust(3)
            pmenu_team.add.button(title=spieler, button_id=str(row[1]), action=spielerkarte)

        pmenu_team.add.button(_('Close'), action=pygame_menu.events.CLOSE) # TODO
        pmenu_team.add.button(_('Close'), pygame_menu.events.RESET)

        pmenu_team.enable()
        pmenu_team.mainloop(pygame.display.get_surface(), clear_surface=False,widget_alignment=pygame_menu.locals.ALIGN_LEFT)

    def set_difficulty(self, value, difficulty):
        # Do the job here !
        pass

    def set_audiomode(self, value, audiomode):
        global audiostate

        # Do the job here !
        if audiomode == 2:
            pygame.mixer_music.stop()
        else:
            pygame.mixer_music.play(-1)
        audiostate = audiomode
        pass

    def set_videomode(self, value, videomode):
        print(_("Videomode") + " " + str(videomode) + " " + _("chosen") + ".")
        pygame.display.set_mode((videomode))
        pass

    def set_text_value(self, name):
        global playername

        #on input change your value is returned here
        print('Player name is', name)
        playername = name
        #text_klein = font_klein.render(_("Spieler") + ": " + name, True, white, green)

    def do_next_turn(self):
        global playercash, quarter, season

        if quarter == 4:
            quarter = 1
            season += 1
        else:
            quarter+=1

        playercash += 125000
        print("Loop. " + _("Season") + " " + str(season) + " " + _("Quarter") + " " + str(quarter))

    def run():

        global xdg_config_file
        global playername

        #conf = Config().load_config()
        #conf = Config()
        #conf.load_config()
        #print(conf.playername)
        #self.playername = conf.playername

        #config = Config.load_config()
        #config.load_config()
        #playername = config(playername)

        print("xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx")

        ###############################################################################

        pygame.init()

        #parser = argparse.ArgumentParser(description='A managerial sports game written in Python.')
        #args = parser.parse_args()
        #print(args.accumulate(args.integers))
        #print(ProgramName + " - " + parser.description)

        conn = None

        # globale variablen ###########################################################

        ProgramName = _("Fussball-Manager")

        season = int(1)
        quarter = int(1)
        audiostate = 1
        playername = str('')
        playercash = int(3560200) # '3.56M'

        # musik laden #################################################################

        filename = "music/The-Games_Looping.mp3"
        pygame.mixer_music.load(filename,"mp3") # "ogg")
        if audiostate == 1:
            pygame.mixer_music.play(-1)

        # standardfarben RGB ##########################################################

        #white = (255, 255, 255)
        #green = (0, 139, 0)
        #blue = (0, 0, 128)
        #black = (0, 0, 0)
        
        # spielfläche initialisieren ##################################################

        screenX = 1920 #800
        screenY = 1080 #600

        screen = pygame.display.set_mode((screenX, screenY))
        pygame.display.set_caption(ProgramName)
        pygame.display.toggle_fullscreen()
        #self.screen.fill(green)

        conf = Config("Michael")
        conf.save_config(audiostate=1, playername="Michael", playercash=100, season=1, quarter=1)
        #self.playername = "Michael"

        # interne spieluhr starten ####################################################

        clock = pygame.time.Clock()

        # bildschirm-auflösungen auflisten ############################################

        resolutions = pygame.display.list_modes()
        list_resolutions =  []
        for res in resolutions:
            list_resolutions.append((str(res).replace(', ', 'x'),res))

        # schriften laden #############################################################

        #font_riesig = pygame.font.Font('freesansbold.ttf', 120)
        font_riesig = pygame.font.Font(pygame_menu.font.FONT_OPEN_SANS_BOLD, 120)
        text_riesig = font_riesig.render("GOAL", True, Colors.white, Colors.green)
        text_riesigRect = text_riesig.get_rect()
        text_riesigRect.center = (screenX // 2 + 100, screenY // 2 - text_riesigRect.height / 2 + 100)

        #font_gross = pygame.font.Font('freesansbold.ttf', 32)
        font_gross = pygame.font.Font(pygame_menu.font.FONT_OPEN_SANS_BOLD, 32)
        text_gross = font_gross.render(ProgramName.upper(), True, Colors.white, Colors.green)
        text_grossRect = text_gross.get_rect()
        text_grossRect.center = (screenX // 2 + 100, screenY // 2 + 100)

        #font_klein = pygame.font.Font('freesansbold.ttf', 16)
        font_klein = pygame.font.Font(pygame_menu.font.FONT_OPEN_SANS_BOLD, 16)

        # themen für pygame_menu adaptieren ###########################################

        # menüs definieren ############################################################

        ABOUT = [f'GoalFM {ProgramName} {GoalFM.__version__}',
                f'Author: {GoalFM.__author__}',
                f'Email: {GoalFM.__email__}']
                
        about_menu = pygame_menu.Menu(height=300, theme=main_theme, title=_('About'), width=400)

        for m in ABOUT:
            about_menu.add.label(m, align=pygame_menu.locals.ALIGN_LEFT, font_size=20)
        about_menu.add.vertical_margin(30)
        about_menu.add.button(_('Close'), pygame_menu.events.BACK)

        # hauptmenü definieren ########################################################

        menu = pygame_menu.Menu(_('Welcome'), 500, 450, theme=main_theme, center_content=True)
                            #theme=pygame_menu.themes.THEME_GREEN)

        menu.add.button(_('Play'), GameLoop.run)
        #menu.add.button(_('About'), about_the_game)
        menu.add.button(_('About'), about_menu)
        menu.add.button(_('Quit'), pygame_menu.events.EXIT)
        f = menu.add.frame_h(300, 10)
        #f.set_padding((1,1))
        #f.set_border(1, (125, 121, 114))
        menu.add.text_input('Name: ', default=playername, onchange=GameLoop.set_text_value)
        menu.add.selector(_('Difficulty') + ': ', [(_('Hard'), 1), (_('Easy'), 2)], onchange=GameLoop.set_difficulty)
        menu.add.selector(_('Resolution') + ': ', list_resolutions, onchange=GameLoop.set_videomode)
        menu.add.selector(_('Audio') + ': ', items=[(_('On'), 1), (_('Off'), 2)], onchange=GameLoop.set_audiomode) # default=int(audiostate)

        #menu._auto_centering = True
        #menu.mainloop(screen)

        ###############################################################################

        #global playername, quarter, season
        #global conn

        #print(_("Game starting..."))

        conn = connect_goal_db()

        while True:
            screen.fill(Colors.green)

            screen.blit(text_riesig, text_riesigRect)
            screen.blit(text_gross, text_grossRect)

            now = datetime.datetime.now()
            #print (now.strftime("%Y-%m-%d %H:%M:%S"))

            text_datum = font_klein.render(now.strftime("%Y-%m-%d %H:%M:%S"), True, Colors.white, Colors.green)
            text_datumRect = text_datum.get_rect()
            text_datumRect.center = (screen.get_width() - text_datumRect.width + 50, text_datumRect.height)
            screen.blit(text_datum, text_datumRect)

            text_klein = font_klein.render(_("Player") + ": " + str(playername) + "        " + _("Season") + " " + str(season) + " " + _("Quarter") + " " + str(quarter), True, Colors.white, Colors.green)
            text_kleinRect = text_klein.get_rect()
            #text_kleinRect.center = (text_kleinRect.width + 50, text_kleinRect.height)
            text_kleinRect.midleft = (12, text_kleinRect.height)
            screen.blit(text_klein, text_kleinRect)

            text_cash = font_klein.render(_("Cash") + ": " + str(playercash), True, Colors.white, Colors.green)
            text_cashRect = text_cash.get_rect()
            #text_kleinRect.center = (text_kleinRect.width + 50, text_kleinRect.height)
            text_cashRect.midleft = (12 + GameLoop.image_salary.get_width() + 10, 30 + GameLoop.image_salary.get_height() / 2)
            screen.blit(text_cash, text_cashRect)

            #self.screen.blit(image, (0, 0))
            screen.blit(GameLoop.image_ball, (screenX - GameLoop.image_ball.get_width(), screenY - GameLoop.image_ball.get_height()))
            #self.screen.blit(image_salary, (text_kleinRect.right + 30, text_kleinRect.height - 10))
            screen.blit(GameLoop.image_salary, (12, 30))

            screen.blit(GameLoop.image_v1, (520+280+10, 100))
            #self.screen.blit(image_v5, (520, 440))

            button = Button(screen, 10, screen.get_height() - 60, 200, 50, False, text="Weiter - nächstes Quartal", fontsize=32, margin=20,
                inactiveColour=(186, 214, 177), hoverColour=(186, 214, 177), pressedColour=(0, 200, 20), radius=10, onClick=GameLoop.do_next_turn) # onClick=lambda: print('Click'))

            button = Button(screen, 10, screen.get_height() - 120, 200, 50, False, text="Options", fontsize=32, margin=20,
                inactiveColour=(186, 214, 177), hoverColour=(186, 214, 177), pressedColour=(0, 200, 20), radius=10, onClick=GameLoop.open_menu) # onClick=lambda: print('Click'))

            button = Button(screen, 230+10, 760+10, 260-10-10, 50, False, text="Liste", fontsize=32, margin=20,
                inactiveColour=(186, 214, 177), hoverColour=(186, 214, 177), pressedColour=(0, 200, 20), radius=10, onClick=GameLoop.open_team) # onClick=lambda: print('Click'))

            # linkes menue
            rows = select_all_menu(conn)
            menues = []
            #for i in range(100,600,50):
            i = 100

            f3 = pygame_menu.font.FONT_COMIC_NEUE

            for row in rows:
                #f1 = pygame.font.Font(FONT_OPEN_SANS, 16)
                #f2 = pygame.freetype.SysFont(FONT_OPEN_SANS, 16)
                #font1 = pygame_menu.font.FONT_OPEN_SANS

                button = Button(screen, 10, i, 200, 40, isSubWidget=True, text=str(row[1]), fontSize=32, margin=20, radius=10, widget_font=f3 , # font=f3,
                    inactiveColour=(186, 214, 177), hoverColour=(186, 214, 177), pressedColour=(0, 200, 20))
                #ba = ButtonArray(self.screen, 10, 100, 200, 1000, (1, 4), border=50, texts=('1', '2', '3', '4'),
                #    onClicks=(lambda: print('1'), lambda: print('2'), lambda: print('3'), lambda: print('4')))

                #self.screen.blit(button, self.screen)
                button.draw(); # button.enable(); button.show(); button.isSubWidget()
                
                #, font= , font pygame_menu.font.FONT_OPEN_SANS)
                #self.screen.blit(source, dest)

                #r = pygame.draw.rect(self.screen,(0,0,0),(10,i,200,40),2,5)
                #text_menu = font_klein.render(str(row[1]), True, black)
                #text_menuRect = text_menu.get_rect()
                #text_menuRect.midleft = (20, i + 20)
                #self.screen.blit(text_menu, text_menuRect)

                #text_menuRect.clamp(r)
                #r.clamp(text_menuRect)
                i += 50

            # dashboard kaesten
            abstand = 280

            rows = select_dashboard(conn)
            zeile = 0
            for row in rows:
                #draw_box(row [0], _(row[1]),230+zeile*abstand,100)
                #Box.draw()
                #Box.draw_box(row[0], _(row[1]),230+zeile*abstand,100,screen)
                Box(screen, _(row[1]), 230+zeile*abstand, 100, 260, 315).draw()

                #myObject.move(10, 10) # move to new place
                #myObject.draw() # draw in new place

                zeile += 1
                #print(row[1])

            """draw_box(0, _("Team"),510,100)
            draw_box(1, _("Training"),510+abstand,100)
            draw_box(2, _("Stadium"),510+2*abstand,100)
            draw_box(3, _("Sponsor"),510+3*abstand,100)
            draw_box(4, _("Finance"),510+4*abstand,100)

            draw_box(4, _("Youth"),510-abstand+10,430)"""

            Box(screen, _("Placeholder"), 230, 430).draw()
            Box(screen, _("Placeholder"),510, 430).draw()

            Box(screen, _("Placeholder"), 510+3*abstand, 430).draw()
            Box(screen, _("Placeholder"),510+4*abstand,430).draw()

            Box(screen, _("Placeholder"),230,760).draw()

            Box(screen, _("Placeholder"),510,760).draw()
            Box(screen, _("Placeholder"),510+abstand,760).draw()
            Box(screen, _("Placeholder"),510+2*abstand,760,530+10).draw()

            Flags(screen, "", 237, 140).draw()
            #show_flags()

            #if mymenu.is_enabled():
                #menu.update(events)
                #menu.draw(self.screen)

            #if spielerkarte.is_enabled():
                #spielerkarte.update(events)
                #spielerkarte.draw(self.screen)

            events = pygame.event.get()
            for event in events:
                #print(event)

                if event.type == pygame.QUIT:
                    print(_("Game stopping..."))
                    conf.save_config(audiostate, playername, playercash, season, quarter)
                    #Config(xdg_config_file, audiostate, playername, playercash, season, quarter).save_config()
                    #save_config()
                    pygame.quit()
                    sys.exit()

                if event.type == pygame.KEYDOWN:
    
                    if event.key == pygame.K_x and event.mod == pygame.KMOD_CTRL:
                        Config(xdg_config_file, audiostate, playername, playercash, season, quarter).save_config()
                        #Config.save_config()
                        #save_config()
                        pygame.quit()
                        sys.exit()
                
                    if event.key == pygame.K_ESCAPE:
                        #Config(audiostate, playername, playercash, season, quarter).save_config()
                        c = Config()
                        c.save_config(audiostate, playername, playercash, season, quarter)
                        #Config.load_config()
                        #save_config
                        menu.mainloop(screen)

                    if event.key == pygame.K_f:
                        pygame.display.toggle_fullself.screen()
                
            pygame_widgets.update(events)
            pygame.display.update()
            #pygame.display.flip()
            clock.tick(30)
            #print(pygame.time.get_ticks())

            pass

