import random

class Word(object):
    def __init__(self, word, game):
        self.word = word
        self.text_color = game.text_color

        speed = Word.get_speed(len(word), game.max_word_speed)
        self.speed = speed * game.up_or_down

        # Calculate px size for word width and height
        text_size = game.font.getsize(self.word)
        self.width = text_size[0]
        self.height = text_size[1]

        # Get px offset from right border to keep the word on the game screen
        bubble_size = Word.get_bubble_size_x(game)
        self.x = Word.get_word_start_x(self.word, game)

        if (game.up_or_down == -1):
            input_box_H = game.bottom_boxH - game.border_width * 2
            self.y = game.screenH - input_box_H - self.height
        else:
            self.y = 0 - self.height

        self.y = Word.get_y_padding(self, game, bubble_size)


    #####################
    #      Getters      #
    #####################
    def get_y_padding(self, game, bubble_size):
        left_padding = 0 + bubble_size[0]
        right_padding = game.screenW - bubble_size[0] - self.width
        if (self.x > right_padding or self.x < left_padding):
            y = bubble_size[1] * game.bubble_y_offset - self.height
            return self.y - y
        return self.y

    def get_bubble_size_x(game):
        bubble_size = game.right_corner.get_size()
        x_size = bubble_size[0] * game.right_corner_x_offset
        return (x_size, bubble_size[1])

    def get_word_start_x(word, game):
        word_size = game.font.getsize(word)
        word_x_offset = word_size[0]
        x_max = game.screenW - word_x_offset
        x = random.randint(0, x_max)
        return x

    def get_speed(word_length, max_speed):
        if (word_length == 2): 
            return max_speed * random.uniform(0.7, 1)
        elif (word_length == 3): 
            return max_speed * random.uniform(0.6, 0.9)
        elif (word_length == 4): 
            return max_speed * random.uniform(0.5, 0.75)
        elif (word_length == 5): 
            return max_speed * random.uniform(0.4, 0.7)
        elif (word_length == 6): 
            return max_speed * random.uniform(0.3, 0.65)
        else: 
            return max_speed * random.uniform(0.2, 0.6)

    def word_str_to_obj(game):
        new_words = []
        for word in game.current_words:
            if (type(word) is str):
                new_words.append(Word(word, game))
            else:
                new_words.append(word)
        game.current_words.clear()
        game.current_words = new_words
        return


#####################
#     Movement      #
#####################
def move_word_up(word, screen, game):
    if ((word.y + word.speed) > 0):
        word.y += word.speed
    else:
        missed_word(word, screen, game)
    return

def move_word_down(word, screen, game):
    text_height = game.get_score_text_size(word.word, "height")
    input_box_height = game.bottom_boxH - game.border_width * 2
    height = game.screenH - text_height - input_box_height - game.font_size / 2
    if ((word.y - word.speed) < height):
        word.y += word.speed
    else:
        missed_word(word, screen, game)
    return

def move_words(screen, game):
    for word in game.current_words:
        try:
            if (game.up_or_down == -1):
                move_word_up(word, screen, game)
            else:
                move_word_down(word, screen, game)
        except AttributeError:
            break
    return


#####################
#      Removal      #
#####################
def missed_word(word, screen, game):
    game.current_words.remove(word)
    game.add_word_bubble(word, screen)
    game.button_hover_sound.play()
    return

def remove_words_from_screen(screen, game): # TODO fix error
    if (game.player_input):
        player_input = game.player_input.split(' ')
        for word in reversed(game.current_words):
            for player_word in player_input:
                if (player_word == word.word):
                    game.characters_typed += len(word.word) + 1
                    try:
                        game.current_words.remove(word)   # TODO fix (list.remove(x): x not in list) exception
                    except:
                        continue
                    game.add_word_bubble(word, screen)
                    if game.music_playing == True:
                        game.button_hover_sound.play()
    return