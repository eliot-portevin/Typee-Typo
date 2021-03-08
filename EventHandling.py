import pygame
import pygame.locals as pl
import sys
import GameScreen
import TypeeTypo
import csv
from datetime import date
pygame.init()

class Wordbanks:
    my_file_english = open('Media/words.txt', 'r')
    my_file_french = open('Media/mots.txt', 'r')
    my_file_german = open('Media/Wörtern.txt', 'r')
    content_english = my_file_english.read()
    content_french = my_file_french.read()
    content_german = my_file_german.read()
    words_english = content_english.split('\n')
    words_french = content_french.split('\n')
    words_german = content_german.split('\n')
#####################
#   Game Specifics  #
#####################
def quit_game(game):
    gwpm = int(GameScreen.get_words_per_min(game))
    today = str(date.today())
    time = game.seconds
    with open('Media/score.csv', mode='a') as scores:
        scores = csv.writer(scores, delimiter=';', quotechar='"', quoting=csv.QUOTE_MINIMAL)

        scores.writerow([str(today), int(gwpm), int(time)])

    pygame.quit()
    sys.exit(0)

def play_music(game, music):
    music = pygame.mixer.music.load(music)
    pygame.mixer.music.play(-1)
    game.music_playing = True
    return

def update_seconds(game, delay):
    game.frame_tracker += 1
    if (game.frame_tracker == (game.max_FPS * delay)):
        game.frame_tracker = 0
        game.seconds += 1
        return True
    return False

def blink_text(game, screen, text, start_screen):
    if (game.update_seconds(game.text_blink_delay)):
        if (game.blinking):
            game.blinking = False
        else:
            game.blinking = True
    if (game.blinking):
        game.draw_blink_text(screen, text, start_screen)
    return

def update_player_input(game, events):
    if (game.words_moving):
        if (game.player_input_obj.update(events, game)):
            game.player_input = game.player_input_obj.get_text()
            game.player_input_obj.reset_input_text()
    return


#####################
#       Frames      #
#####################
def check_frame_count(game):
    if (game.frame_count >= game.max_FPS):
        game.frame_count = 0
        game.seconds += 1
        game.add_word_seconds += 1
    return

def check_quick_frame_count(game):
    max_FPS_fraction = game.max_FPS * game.add_word_delay
    if (game.quick_frame_count == max_FPS_fraction):
        game.quick_frame_count = 0
        return True
    game.quick_frame_count += 1
    return False


#####################
#    Title Events   #
#####################
def check_title_events(game):
    events = pygame.event.get()
    for event in events:
        if (event.type == pygame.QUIT):
                    quit_game(game)
        elif (event.type == pygame.KEYDOWN):
            if (event.key == pygame.K_SPACE):
                return True
    return False


#####################
#    Menu Events    #
#####################
def get_avg_word_length(wordbank):
    num_words = len(wordbank)
    total = 0
    for word in wordbank:
        total += len(word)
    avg_length = 4.5
    return avg_length

def check_menu_mouse_position(game, mouse_position, button):
    if (button.is_over(mouse_position)):
        button.color = game.button_hover_color
        button.textColor = game.button_text_color
        button.hovering = True
        if (button.play_sound):
            if game.music_playing is True:
                game.button_hover_sound.play()
                button.play_sound = False
    else:
        button.color = game.button_color
        button.textColor = game.button_text_color
        button.hovering = False
        button.play_sound = True
    return

click_rect  = pygame.Rect(50, 220, 300, 500)
mute_rect = pygame.Rect(800, 0, 500, 1000)

def check_button(game, button):
    if (button.text == "1st"):
        game.wordbank = Wordbanks.words_english
    elif (button.text == "2nd"):
        game.wordbank = Wordbanks.words_french
    elif (button.text == "3rd"):
        game.wordbank = Wordbanks.words_german
    elif (button.text == 'information'):
        return False
    elif (button.text == 'mute'):
        if game.music_playing is False:
            pygame.mixer.music.unpause()
            game.music_playing = True
            return False
        else:
            pygame.mixer.music.pause()
            game.music_playing = False
            return False
    if (game.wordbank != None):
        avg_word_length = get_avg_word_length(game.wordbank)
        game.avg_word_length = avg_word_length
        return True
    return False

def check_menu_events(game, buttons):
    mouse_position = pygame.mouse.get_pos()
    events = pygame.event.get()
    for event in events:
        if (event.type == pygame.QUIT):
                    quit_game(game)
        elif (event.type == pygame.MOUSEMOTION):
            for button in buttons:
                check_menu_mouse_position(game, mouse_position, button)
        elif (event.type == pygame.MOUSEBUTTONDOWN):
            for button in buttons:
                if (button.is_over(mouse_position)):
                    if (check_button(game, button)):
                        return True
    return False

def click_button(mouse_position, buttons, game):
    for button in buttons:
        if (button.is_over(mouse_position)):
            if (button.text == "Start"):
                game.words_moving = True
                button.visible = True
            elif (button.text == "Pause"):
                if (game.words_moving):
                    game.words_moving = False
                else:
                    game.words_moving = True
            elif (button.text == "Mute"):
                if (game.music_playing):
                    pygame.mixer.music.pause()
                    game.music_playing = False
                else:
                    pygame.mixer.music.unpause()
                    game.music_playing = True
    return

def check_game_events(game, buttons):
    mouse_position = pygame.mouse.get_pos()
    events = pygame.event.get()
    for event in events:
        if (event.type == pygame.QUIT):
            quit_game(game)
        elif (event.type == pygame.KEYDOWN):
            if event.key == pl.K_ESCAPE:
                if (game.words_moving):
                    game.words_moving = False
                    game.is_paused = True
                else:
                    game.words_moving = True
                    game.is_paused = False
    update_player_input(game, events)
    return True