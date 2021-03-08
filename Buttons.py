import pygame
import csv
import numpy as np
pygame.init()


class Button:
    buttons = []
    pause_buttons = []
    num_buttons = 0
    num_pause_buttons = 0
    def __init__(self, x, y, text, game, is_menu_button, image_size=None):
        self.x = x
        self.y = y
        self.text = text
        self.text_color = game.text_color
        self.color = game.button_color
        self.hovering = False
        self.play_sound = True
        self.visible = True
        self.font = pygame.font.SysFont('Monospace', 15, bold=True)
        self.high_score_font = pygame.font.SysFont('Monospace', 20, bold=True)
        self.time_font = pygame.font.SysFont('Monospace', 17, bold = False)
        self.evolution = pygame.image.load("score.png")
        self.evolution = pygame.transform.scale(self.evolution, (630, 420))
        
        # Menu/Game Button Parameters
        if (is_menu_button):
            self.width = image_size[0]
        else:
            self.width = game.buttonW
        self.height = image_size[1]
        self.border = (self.x-2, self.y-2, self.width+4, self.height+4)


    #####################
    #      Getters      #
    #####################
    def get_menu_buttons(game):
        col = 1
        row = 1
        for index in range(len(game.grade_levels)):
            value = game.grade_levels[index]
            if (col == 1):
                if (row == 1):
                    image = game.english
                    image_size = image.get_size()
                    x = game.x_menu_col_1 - image_size[0] / 2
                    y = game.y_menu_col_1
                elif (row == 2):
                    image = game.french
                    image_size = image.get_size()
                    x = game.x_menu_col_1 - image_size[0] / 2
                    y = game.y_menu_col_2
                elif (row == 3):
                    image = game.german
                    image_size = image.get_size()
                    x = game.x_menu_col_1 - image_size[0] / 2
                    y = game.y_menu_col_3
                elif (row == 4):
                    image = game.information
                    image_size = image.get_size()
                    x = game.x_information
                    y = game.y_information
                elif (row == 5):
                    image = game.mute
                    image_size = image.get_size()
                    x = game.x_information - 20
                    y = 0.75 * game.screenH
                row += 1
            Button.add_button(x, y, value, True, image_size, game)

        return Button.buttons

    def get_pause_buttons(game):
        num = 1
        for index in range(len(game.pause_buttons)):
            value = game.pause_buttons[index]
            if (num == 1):
                image = game.quit_button
                image_size = image.get_size()
                x = 200
                y = 300
            elif (num == 2):
                image = game.mute
                image_size = image.get_size()
                x = game.x_information -20
                y = 0.75 * game.screenH
            num += 1
        Button.add_pause_button(x, y, value, True, image_size, game)


    #####################
    #   Event Handling  #
    #####################
    def is_over(self, mouse_position):
        mouseX = mouse_position[0]
        mouseY = mouse_position[1]
        if (mouseX > self.x and mouseX < self.x + self.width):
            if (mouseY > self.y and mouseY < self.y + self.height):
                return True         
        return False

    def add_button(x, y, value, is_menu_button, image_size, game):
        Button.num_buttons += 1
        Button.buttons.append(Button(
            x, 
            y, 
            value,
            game,
            is_menu_button,
            image_size)
        )
        return
    
    def add_pause_button(x, y, value, is_pause_button, image_size, game):
        Button.num_pause_buttons += 1
        Button.pause_buttons.append(Button(
            x, 
            y, 
            value,
            game,
            is_pause_button,
            image_size)
        )
        return


    #####################
    #      Drawing      #
    #####################
    def draw_button(self, screen, image, height, game):
        size = image.get_size()
        x = game.screenW - game.buttonW + (game.buttonW - size[0]) / 2
        y = game.screenH - height - game.bottom_boxH + (game.buttonH - size[1]) / 2
        screen.blit(image, (x, y))
        return

    def draw(self, screen, game, hover=None):
        if (self.visible):
            if (self.hovering):
                if (self.text == "1st"):
                    screen.blit(game.grade_1st_hovering, (self.x, self.y))
                elif (self.text == "2nd"):
                    screen.blit(game.grade_2nd_hovering, (self.x, self.y))
                elif (self.text == "3rd"):
                    screen.blit(game.grade_3rd_hovering, (self.x, self.y))
                elif (self.text == 'information'):
                    screen.blit(game.information_hovering, (self.x, self.y))
                    draw_rect_alpha(screen, (0, 0, 0, 100), (0, 0, 1080, 800))
                    draw_rect_alpha(screen, (57, 42, 97, 200), (50, 40, 850, 530))
                    draw_score(screen, score, (300, 535), self.high_score_font)
                    draw_score(screen, times, (270, 513), self.time_font)
                    screen.blit(self.evolution, (160, 70))
                elif (self.text == 'mute'):
                    screen.blit(game.mute_hovering, (self.x, self.y))
                elif (self.text == 'quit'):
                    screen.blit(game.quit_hovering, (self.x, self.y))
        return

DataFiles = ['Media/score.csv']
scores = []
high_score = []

for i in range(len(DataFiles)):

    scores, time = np.loadtxt(DataFiles[i], skiprows=1, usecols=(1, 2), unpack=True, delimiter=';')
    high_score = str(max(scores))
    sum_time = np.sum(time)
    if (sum_time>3600):
        total_time = round(sum_time/3600, 2)
        times = "You have spent " + str(total_time) + " hours on the game."
    elif (sum_time>60):
        total_time = round(sum_time/60, 2)
        times = "You have spent " + str(total_time) + " minutes on the game."
    else:
        times = "You have spent " + str(total_time) + " seconds on the game."


    score = "Your High Score:   " + high_score + " WPM"

def draw_evolution(surface, rect):
    surface.blit(evolution, evolution_rect)

def draw_rect_alpha(surface, color, rect):
    shape_surf = pygame.Surface(pygame.Rect(rect).size, pygame.SRCALPHA)
    pygame.draw.rect(shape_surf, color, shape_surf.get_rect())
    surface.blit(shape_surf, rect)

def draw_score(surface, text, pos, font, color=(255, 255, 255, 200)):
    x, y = pos
    word_surface = font.render(str(text), 0, color)
    surface.blit(word_surface, (x, y))