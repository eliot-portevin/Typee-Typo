import install_requirements
import pygame
pygame.init()
import GameScreen
from PIL import ImageFont
import random
import Bubbles as Bub
import Buttons as But
import EventHandling as Events
import PlayerInput as PI
import sys
from subprocess import call


#####################
#     Game Class    #
#####################
class Game():   
    def __init__(self):
        # Window
        self.border_width = 2
        self.bottom_boxH = 50
        self.screenW = 950
        self.screenH = 600
        self.title = "Typee Typo"
        self.top_padding = 100

        # Fonts/Colors
        self.button_color = (44, 150, 199)
        self.button_hover_color = (194,178,128)
        self.button_text_color = (255,255,255)
        self.font_size = 27
        self.master_font = "Media/TravelingTypewriter.ttf"
        self.text_color = (255,255,255)
        self.font = ImageFont.truetype(self.master_font, self.font_size)
        self.word_font = pygame.font.Font(self.master_font, self.font_size)

        # Buttons
        self.button_spacing = 10
        self.buttonW = 150
        self.buttonH = 75
        self.menu_buttonH = 50
        self.menu_buttonW = 100

        # Important Variables
        self.word_delay_score_multiplier = 1.0
        self.up_or_down = 1 # -1 for words up 1 for words down
        self.add_word_seconds = 0
        self.add_words_trigger = 8
        self.max_word_speed = 1
        self.text_blink_delay = .5
        self.player_score = 0
        self.clock = pygame.time.Clock()
        self.is_paused = False

        # Flags
        self.blinking = True
        self.music_playing = True
        self.words_moving = False
        self.pause_screen_drawn = False
        self.pause_bubbles_drawn = False

        # Word Handling
        self.avg_word_length = 0
        self.characters_typed = 0
        self.characters_all = 1
        self.current_words = [""]
        self.gross_words_per_min = 0
        self.wordbank = [""]

        # HUD Variables
        self.left_corner_x_offset = .25
        self.right_corner_x_offset = .75
        self.bubble_y_offset = .5
        self.input_width = 0
        self.button_padding = 10

        # Frames
        self.bubble_frame_count = 0
        self.frame_count = 0
        self.frame_tracker = 0
        self.quick_frame_count = 0
        self.max_FPS = 60
        self.seconds = 1

        # Input Handling
        self.input_left_padding = 20
        self.player_input = None
        self.player_input_obj = None

        # Menu Parameters
        self.x_menu_col_1 = self.screenW / 5.5
        self.x_information = self.screenW * 0.925
        self.y_menu_col_1 = self.screenH / 5 * 1.7
        self.y_menu_col_2 = self.screenH / 5 * 2.7
        self.y_menu_col_3 = self.screenH / 5 * 3.7
        self.y_information = self.screenH * 0.004

        # Prompts/Text
        self.grade_levels = ("1st", "2nd", "3rd", "information", "mute")
        self.pause_text = ('mute', 'quit')
        self.game_buttons = ('pause')
        self.gwpm_prompt = "WPM: "
        self.input_prompt = "Input: "
        self.menu_prompt = "Languages"
        self.score_prompt = "Score: "
        self.start_prompt = "Press Space When Ready!"
        self.title_prompt = "Press Space"

        # Game Media
        self.bg_image = pygame.image.load("Media/background.jpg")
        self.title_text = pygame.image.load("Media/title_image.png")
        self.right_corner = pygame.image.load("Media/meteors/right_meteor.png")
        self.left_corner = pygame.image.load("Media/meteors/left_meteor.png")
        self.game_button_left = pygame.image.load("Media/meteors/game_button_left.png")
        self.game_button_right = pygame.image.load("Media/meteors/game_button_right.png")

        # Sound Media
        self.button_hover_sound = pygame.mixer.Sound("Media/hover_sound.wav")
        self.game_music = "Media/menu_music.wav"
        self.title_music = "Media/menu_music.wav"

        # Button Media
        self.menu_header = pygame.image.load("Media/menu_prompt.png")
        self.english = pygame.image.load("Media/english.png")
        self.french = pygame.image.load("Media/french.png")
        self.german = pygame.image.load("Media/german.png")
        self.information = pygame.image.load("Media/information.png")
        self.mute = pygame.image.load("Media/mute.png")
        self.quit_button = pygame.image.load('Media/quit.png')
        self.all_vocab = (
            self.english, 
            self.french, 
            self.german, 
            self.information, 
            self.mute
        )
        self.pause_buttons = (
            self.mute, 
            self.quit_button
        )
        self.x_mute = 859
        self.y_mute = 450

        # Button Hover Media
        self.grade_1st_hovering = pygame.image.load("Media/english_hovering.png")
        self.grade_2nd_hovering = pygame.image.load("Media/french_hovering.png")
        self.grade_3rd_hovering = pygame.image.load("Media/german_hovering.png")
        self.information_hovering = pygame.image.load('Media/information.png')
        self.mute_hovering = pygame.image.load("Media/mute_hovering.png")
        self.quit_hovering = pygame.image.load('Media/quit_hovering.png')
        try:
            call(["python3", "evolution.py"])
        except:
            print('')

        try:
            call(["python", "evolution.py"])
        except:
            print('')
            
        self.evolution = pygame.image.load('score.png')
        self.restart_variable = False



    #####################
    #      Getters      #
    ##################### 
    def get_menu_buttons(self):
        return But.Button.get_menu_buttons(self)

    def get_num_buttons(self):
        return But.Button.num_buttons

    def get_score_text_size(self, score, return_flag=None):
        convert_text = str(score) + str(self.border_width)
        text = self.score_prompt + convert_text
        width_height = self.font.getsize(text)
        if (return_flag == "width"):
            return width_height[0]
        elif (return_flag == "height"):
            return width_height[1]
        return width_height[0], width_height[1]

    def get_bottom_offset(self, text, score=""):
        text_height = self.get_score_text_size(score, "height")
        input_box_text_offset = (self.bottom_boxH - text_height) // 2
        borders_offset = (self.border_width * 3)
        screenH_offset = self.screenH - text_height
        bottom_offset = screenH_offset - borders_offset - input_box_text_offset
        return bottom_offset

    def get_right_offset(self, score=""):
        text_width = self.get_score_text_size(score, "width")
        right_offset = self.screenW - self.buttonW - text_width
        return right_offset


    #####################
    #      Setters      #
    #####################
    def set_player_input(self):
        self.player_input_obj = PI.PlayerInput(self)
        return

    def set_screen(self):
        pygame.display.set_caption(self.title)
        pygame.display.set_icon(pygame.image.load('Media/Logo.png'))
        return (pygame.display.set_mode((self.screenW, self.screenH)))

    def reset_buttons(self):
        But.Button.buttons.clear()
        return

    #####################
    #      Drawing      #
    #####################
    def draw_buttons(self, screen, game_button=False):
        for button in But.Button.buttons:
            button.draw(screen, self)
            if (game_button):
                Bub.Bubbles.draw_button_bubble(button, screen, self)
        return
    
    def draw_bg_image(self, screen):
        screen.blit(self.bg_image, (0,0))
        return

    def draw_corner_bubbles(self, screen):
        Bub.Bubbles.draw_corner_bubble(screen, self)
        Bub.Bubbles.draw_corner_bubble(screen, self, True)
        return

    def draw_blink_text(self, screen, text, start_screen):
        font_size = self.font.getsize(text)
        x = ((self.screenW / 2) - (font_size[0] / 2))
        if (start_screen):
            y = (self.screenH / 2) - (font_size[1] / 2)
        else:
            y = ((self.screenH / 2) - (font_size[1] / 2) + self.top_padding)
        text = self.word_font.render(text, 1, self.text_color)
        screen.blit(text, (x,y))
        return

    def draw_bubbles(self, screen):
        Bub.Bubbles.draw_bubbles(self, self, screen)
        return


    #####################
    #   Event Handling  #
    #####################
    def quit_game(self, game):
        Events.quit_game(game)

    def play_music(self, music):
        Events.play_music(self, music)
        return

    def add_word_bubble(self, word, screen):
        Bub.Bubbles.add_word_bubble(self, word, screen)
        return

    def pop_word_bubbles(self, screen):
        Bub.Bubbles.pop_word_bubbles(screen)
        return

    def blink_text(self, screen, text, start_screen):
        Events.blink_text(self, screen, text, start_screen)
        return

    def check_frame_count(self):
        Events.check_frame_count(self)
        return

    def check_quick_frame_count(self):
        status = Events.check_quick_frame_count(self)
        return status

    def update_seconds(self, delay):
        status = Events.update_seconds(self, delay)
        return status

    def check_game_events(self, buttons):
        status = Events.check_game_events(self, buttons)
        return status

    def check_menu_events(self, buttons):
        status = Events.check_menu_events(self, buttons)
        return status

    def check_title_events(self):
        status = Events.check_title_events(self)
        return status


#####################
#    Menu Screen    #
#####################
def draw_menu_header(screen, game):
    image_size = game.menu_header.get_size()
    x = (game.screenW - image_size[0]) / 2
    y = 50
    screen.blit(game.menu_header, (x,y))
    return

def draw_menu(screen, game, buttons):
    index = 0
    for button in buttons:
        screen.blit(game.all_vocab[index], (button.x, button.y))
        index += 1     
    return

def draw_menu_screen(screen, game, buttons):
    game.frame_count += 1
    game.draw_bg_image(screen)
    game.draw_bubbles(screen)
    draw_menu_header(screen, game)
    draw_menu(screen, game, buttons)
    game.draw_buttons(screen)
    pygame.display.update()
    game.check_frame_count()
    return

def menu_screen(screen, game):
    buttons = game.get_menu_buttons()
    while(True):
        game.clock.tick(game.max_FPS)
        if (game.check_menu_events(buttons)):
            break
        draw_menu_screen(screen, game, buttons)
    game.reset_buttons()
    game.frame_count = 0
    return


#####################
#    Title/Start    #
#####################
def draw_title(screen, game):
    text_size = game.title_text.get_size()
    x = (game.screenW - text_size[0]) / 2
    y = game.top_padding - 30
    screen.blit(game.title_text, (x,y))
    return

def draw_screen(screen, game, start_screen=False):
    game.clock.tick(game.max_FPS)
    game.frame_count += 1
    game.draw_bg_image(screen)
    if (start_screen):
        game.blink_text(screen, game.start_prompt, start_screen)
    else:
        draw_title(screen, game)
        game.blink_text(screen, game.title_prompt, start_screen)
    game.draw_bubbles(screen)
    pygame.display.update()
    game.check_frame_count()
    return

def title_screen(screen, game):
    game.play_music(game.title_music)
    while (True):
        if (game.check_title_events()):
            break
        draw_screen(screen, game)
    return

def start_screen(screen, game):
    while (True):
        if (game.check_title_events()):
            game.words_moving = True
            break
        draw_screen(screen, game, True)
    return


#####################
#        Main       #
#####################
def restart2():
    game = Game()
    screen = game.set_screen()
    game.set_player_input()

    menu_screen(screen, game)
    start_screen(screen, game)
    GameScreen.play(screen, game)
    if game.restart_variable:
        restart()

def restart():
    game = Game()
    screen = game.set_screen()
    game.set_player_input()

    menu_screen(screen, game)
    start_screen(screen, game)
    GameScreen.play(screen, game)
    if game.restart_variable:
        restart2()

def main():
    game = Game()
    screen = game.set_screen()
    game.set_player_input()

    title_screen(screen, game)
    menu_screen(screen, game)
    start_screen(screen, game)
    GameScreen.play(screen, game)
    if game.restart_variable:
        restart()


if __name__ == "__main__":
    main()