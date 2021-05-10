import pygame
import random
import Words
from subprocess import call
import Bubbles as Bub
import csv
import numpy as np
pygame.init()

#####################
#      Getters      #
##################### 
def get_words_per_min(game):
    one_min = 60
    gwpm = str(game.gross_words_per_min)
    if game.characters_typed == 0:
        gwpm = 0
    else:
        average_chars = game.characters_typed / game.avg_word_length
        average_time = game.seconds / one_min
        gwpm = round(average_chars / average_time)
    return gwpm

def get_gwpm_text_size(game):
    gwpm = str(game.gross_words_per_min)
    text_string = game.gwpm_prompt + str(gwpm)
    text_size = game.font.getsize(text_string)
    text = game.word_font.render(text_string, 1, game.text_color)
    return text, text_size[0]

def get_stopwatch_string(game):
    game_seconds = game.seconds
    seconds = game_seconds % 60
    mins = game_seconds // 60
    hours = game_seconds // 60 // 60
    if (hours > 0):
        stopwatch = (f"{hours:02}:{mins:02}:{seconds:02}")
    elif (mins > 0):
        stopwatch = (f"{mins:02}:{seconds:02}")
    else:
        stopwatch = (f"{seconds:02}")
    return stopwatch

def get_time_location(text_size, game):
    char_size = game.font.getsize("0")
    image_size = game.right_corner.get_size()
    x = game.screenW - (image_size[0] * game.right_corner_x_offset) / 2
    x -= text_size[0] / 2 - char_size[0]
    y = game.screenH - game.bottom_boxH
    return x, y

def add_word(game):
    new_word = random.choice(game.wordbank)
    game.current_words.append(new_word)
    return


#####################
#   Event Handling  #
#####################

def continue_game(screen, game):
    if (len(game.current_words) < game.add_words_trigger):
        game.current_words.append(random.choice(game.wordbank))
    Words.Word.word_str_to_obj(game)
    Words.remove_words_from_screen(screen, game)
    Words.move_words(screen, game)
    game.pop_word_bubbles(screen)
    pygame.display.update()
    return


#####################
#      Drawing      #
#####################
def draw_input_text(screen, game):
    player_input = game.player_input_obj.get_surface()
    size = game.player_input_obj.input_size
    x = game.screenW / 2 - size[0] / 2
    y = game.get_bottom_offset(game.score_prompt) + game.border_width
    screen.blit(player_input, (x,y))
    return

def draw_elapsed_time(screen, game):
    text_string = get_stopwatch_string(game)
    text_size = game.font.getsize(text_string)
    text = game.word_font.render(text_string, 1, game.text_color)
    x, y = get_time_location(text_size, game)
    screen.blit(text, (x,y))
    return

def draw_words_per_min(screen, game):
    if (game.characters_typed != 0 and game.seconds != 0):
        gwpm = get_words_per_min(game)
        game.gross_words_per_min = gwpm
    text, text_width = get_gwpm_text_size(game)
    x = 0 + game.input_left_padding / 1.5
    y = game.screenH - game.bottom_boxH
    screen.blit(text, (x,y))
    draw_elapsed_time(screen, game)
    return

def draw_input_top(screen, game):
    image_size = game.right_corner.get_size()
    x_start = 0 + image_size[0] * .75
    x_end = game.screenW - image_size[0] * .75
    game.input_width = x_end - x_start
    y = game.screenH - game.bottom_boxH
    pygame.draw.line(screen, game.text_color, (x_start,y), (x_end,y), game.border_width)
    return

def draw_words(screen, game):
    for word in game.current_words:
        text = game.word_font.render(word.word, 1, word.text_color)
        screen.blit(text, (word.x, word.y))
    return

def draw_buttons(self, screen, game_button=False):
    for button in But.Button.buttons:
        button.draw(screen, self)
        if (game_button):
            Bub.Bubbles.draw_button_bubble(button, screen, self)
    return

def get_high_score():
    DataFiles = ['Media/score.csv']

    for i in range(len(DataFiles)):
        scores, time = np.loadtxt(DataFiles[i], skiprows=1, usecols=(1, 2), unpack=True, delimiter=';')
        high_score = str(max(scores))

    return high_score

def draw_pause(screen, game):
    high_score = get_high_score()
    pause_surface = pygame.Surface((1000,800), pygame.SRCALPHA)
    pause_surface.fill((0,0,0,100))
    screen.blit(pause_surface, (0,0))

    resume_font = pygame.font.SysFont('Monospace', 25, bold=True)
    quit_font = pygame.font.SysFont('Monospace', 15, bold=True)
    resume_text = resume_font.render('To resume your game, press [ESC] again.', 0, (255, 255, 255))
    restart_text = resume_font.render('Press R to restart.', 0, (255, 255, 255))
    resume_surface = pygame.Surface((740, 400), pygame.SRCALPHA)
    resume_surface.fill((0, 0, 0, 100))
    screen.blit(resume_surface, (100, 100))
    screen.blit(resume_text, (475 - resume_text.get_width() / 2, 120))
    screen.blit(restart_text, (475 - restart_text.get_width() / 2, 150))

    quit_text1 = quit_font.render('If you wish to quit this game, you can simply close the', 0, (255, 255, 255))
    quit_text2 = quit_font.render('window. Your score will be saved automatically ._.', 0, (255, 255, 255))
    score = resume_font.render("Your High Score:   " + high_score + " WPM", 0, (255, 255, 255))

    screen.blit(quit_text1, (200, 220))
    screen.blit(quit_text2, (225, 250))
    screen.blit(score, (245, 450))

    return

def draw_game_screen(screen, game, buttons):
    game.draw_bg_image(screen)
    draw_words(screen, game)
    game.draw_corner_bubbles(screen)
    game.draw_buttons(screen)
    draw_input_top(screen, game)
    draw_words_per_min(screen, game)
    draw_input_text(screen, game)
    if (game.is_paused):
        draw_pause(screen, True)
    pygame.display.update()
    return

#####################
#    Game Screen    #
#####################
def play(screen, game):
    if game.music_playing is True:
        game.play_music(game.game_music)
    buttons = None
    game.seconds = 0
    while(not game.restart_variable):
        game.clock.tick(game.max_FPS)
        game.frame_count += 1
        if not (game.check_game_events(buttons)):
            break
        if (game.words_moving):
            continue_game(screen, game)
            game.check_frame_count()
        draw_game_screen(screen, game, buttons)
    game.reset_buttons()
    return