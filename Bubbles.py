import pygame
import random

class Bubbles:
    bubble = pygame.image.load("Media/meteors/m1.png")
    bubble_pop = [
    pygame.image.load("Media/meteors/m%s.png" % img) for img in range(2,5)
    ]
    bubble_array = []
    def __init__(self, game, word_bubble=False, word_x=0, word_y=0):
        self.img = Bubbles.bubble
        size = self.img.get_size()
        self.width = size[0]
        self.height = size[1]
        screenW, screenH = pygame.display.get_surface().get_size()
        if (word_bubble):
            self.x = word_x
            self.y = word_y
            self.popping = True
        else:
            self.x = random.randint(0, 2000)
            self.y = game.screenH + self.height
            self.popping = False
            self.startX = self.x
            self.speed = random.uniform(.5, 2)
            self.direction = random.choice(["right", "left"])
        self.pop_count = 1
        self.pop_FPS = 3
        self.bubbling = True


    #####################
    #   Event Handling  #
    #####################
    def pop_bubble(self, screen):
        if (self.popping):
            img = self.bubble_pop[self.pop_count // self.pop_FPS]
            screen.blit(img, (self.x, self.y))
            self.pop_count += 1
            if (self.pop_count > len(self.bubble_pop) + 1):
                return True
        return False

    def update_bubbles(self, game):
        x = random.randint(1, 100)
        if x == 1:
            Bubbles.bubble_array.append(Bubbles(game))
        return

    def add_word_bubble(game, word, screen):
        image_size = game.menu_header.get_size()
        y_offset = word.y - image_size[1] / 2
        Bubbles.bubble_array.append(Bubbles(
            game, 
            True, 
            word.x, 
            y_offset)
        )
        return

    def pop_word_bubbles(screen):
        for bubble in Bubbles.bubble_array:
            if (bubble.pop_bubble(screen)):
                Bubbles.bubble_array.remove(bubble)
        return


    #####################
    #      Drawing      #
    #####################
    def draw(self, screen, game):
        if not (self.popping):
            screen.blit(self.img, (self.x, self.y))
            self.y -= self.speed
            self.x -=self.speed
            if (self.x <= (0 - game.font_size - game.border_width)):
                self.popping = True
            elif (self.y <= (0 - game.font_size - game.border_width)):
                self.popping = True
        return

    def draw_bubbles(self, game, screen):
        for bubble in Bubbles.bubble_array:
            if not (bubble.draw(screen, game)):
                if (bubble.pop_bubble(screen)):
                    Bubbles.bubble_array.remove(bubble)
        Bubbles.update_bubbles(self, game)
        return

    def draw_button_bubble(button, screen, game):
        text_size = game.font.getsize(button.text)

        if (button.text == "Mute"):
            image_size = game.game_button_left.get_size()
            x = button.x - text_size[0] / 2
            y = button.y - image_size[1] / 2 + text_size[1]
            screen.blit(game.game_button_left, (x,y))
        elif (button.text == "Speed"):
            image_size = game.game_button_right.get_size()
            x = button.x - text_size[0] / 2
            y =  button.y - image_size[1] / 2 + text_size[1]
            screen.blit(game.game_button_right, (x,y))
        elif (button.text == "+"):
            pixel_y_offset = 12
            image_size = game.speed_up.get_size()
            speed_bubble_size = game.speed_image.get_size()
            x = button.x - image_size[0] + text_size[0]
            text_size = game.font.getsize("Speed")
            y =  button.y - speed_bubble_size[1] + text_size[1] / 2 + pixel_y_offset
            screen.blit(game.speed_change, (x,y))
        elif (button.text == "-"):
            pixel_x_offset = 2
            pixel_y_offset = 5
            image_size = game.speed_down.get_size()
            speed_bubble_size = game.speed_image.get_size()
            x = button.x - image_size[0] / 2 - text_size[0] * 2 + pixel_x_offset
            text_size = game.font.getsize("Speed")
            y = button.y - speed_bubble_size[1] + text_size[1] / 2 + pixel_y_offset
            screen.blit(game.speed_change, (x,y))
        return

    def draw_corner_bubble(screen, game, left_bubble=False):
        image_size = game.right_corner.get_size()
        y = game.screenH - image_size[1] * game.bubble_y_offset
        if (left_bubble):
            x = 0 - image_size[0] * game.left_corner_x_offset
            screen.blit(game.left_corner, (x,y))
        else:
            x = game.screenW - image_size[0] * game.right_corner_x_offset
            screen.blit(game.right_corner, (x,y))
        return