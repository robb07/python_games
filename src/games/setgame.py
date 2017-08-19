#!/usr/bin/env python
'''
Set, the game of matching cards by similarity and differences
Created August 16, 2017

@author: Robb
'''

import random
from game_tools import simplegui
from game_tools import sprite

PAD_W = 10
PAD_H = 10
CARD_W = 120
CARD_H = 180
WIDTH = 9*CARD_W
HEIGHT = 4*CARD_H
BUTTON_W = 0.9*CARD_W       
BUTTON_FONT_H = 16

CARDS_IMAGE_INFO = simplegui.Image_Info(simplegui.get_image_path('set_shapes.png'), (6*(CARD_W + PAD_W), 6*(CARD_H + PAD_H)))

DEFAULT_CARDS_ON_BOARD = 12
ABS_MAX_CARDS_ON_BOARD = 21
max_cards_on_board = 12
deck = []
board = dict([])
num_sets = 0
score = 0

class Card(sprite.Sprite):
    '''A Card'''

    def __init__(self, number, pattern, color, shape):
        '''Constructor'''
        global all_cards_image
        self.props = (number, pattern, color, shape)
        self.selected = False
        self.coords = None
        # cards are organized in x direction by number (larger distance) then pattern
        # and in the y direction by color then shape
        pos_offset = ((3*number + pattern)*(CARD_W + PAD_W), (3*color + shape)*(CARD_H + PAD_H))
        size = (CARD_W, CARD_H)
        image = simplegui.SubImage(all_cards_image, pos_offset, size)
        super(Card, self).__init__(name='Card' + "".join(map(str, self.props)), size=size, image=image)

    def set_coords(self, (row, col)):
        self.coords = (row, col)
        self.set_pos(((1+col)*(CARD_W+PAD_W), (1+row)*(CARD_H+PAD_H)))

    def get_coords(self):
        return self.coords

    def set_selected(self, selected):
        self.selected = selected

    def get_selected(self):
        return self.selected

    def draw(self, canvas):
        if self.selected:
            x, y = self.get_pos()
            w, h = self.get_size()
            canvas.draw_rect((x-5-w/2, y-5-h/2), (w+10, h+10), 2, "SteelBlue")
        super(Card, self).draw(canvas)


def valid_set(cards):
    '''Checks if the set of cards is a valid set'''
    if len(cards) != 3:
        return False

    card1, card2, card3 = cards
    return all(sum(dimension) % 3 == 0 for dimension in zip(card1.props, card2.props, card3.props))


def mouse_left_click(pos):
    '''Hndles left mouse clicks'''
    for card in board.itervalues():
        if card.contains(pos):
            card.set_selected(not card.get_selected())


def key_up(key):
    '''Handles key up events'''
    if key == "d":
        deal_more()


def deal_more():
    '''Attempts to deal more cards'''
    global max_cards_on_board, score
    if max_cards_on_board + 3 <= ABS_MAX_CARDS_ON_BOARD and len(deck) > 0:
        max_cards_on_board += 3
        # TODO: only decrease score if there are viable sets left
        score -= 2
        deal_cards()


def draw(canvas):
    '''Draw the board'''
    global deck, board, max_cards_on_board
    global num_sets, score
    for card in board.itervalues():
        card.draw(canvas)

    selected = [card for card in board.itervalues() if card.get_selected()]
    if len(selected) == 3:
        if valid_set(selected):
            for card in selected:
                del board[card.get_coords()]
            if max_cards_on_board > DEFAULT_CARDS_ON_BOARD:
                max_cards_on_board -= 3
            deal_cards()
            num_sets += 1
            score += 10
        else:
            for card in selected:
                card.set_selected(False)

    # Update the labels
    remaining_cards_label.text = "Cards: {0}".format(len(deck))
    sets_label.text = "Sets: {0}".format(num_sets)
    score_label.text = "Score: {0}".format(score)


def new_game():
    '''Build a new deck, shuffle, and deal out the cards'''
    global deck, board, max_cards_on_board
    global num_sets, score
    deck = [Card(n, p, c, s) for n in xrange(3)
                             for p in xrange(3)
                             for c in xrange(3)
                             for s in xrange(3)]
    random.shuffle(deck)
    board = dict([])
    max_cards_on_board = DEFAULT_CARDS_ON_BOARD
    deal_cards()
    num_sets = 0
    score = 0


def deal_cards():
    global deck, board, max_cards_on_board
    
    for i in xrange(max_cards_on_board):
        row = i % 3
        col = i // 3
        if len(deck) > 0 and len(board) < max_cards_on_board and (row, col) not in board:
            card = deck.pop()
            card.set_coords((row, col))
            board[(row, col)] = card



def setup():
    '''Setup the frame and event handlers'''
    global frame, all_cards_image
    global remaining_cards_label, sets_label, score_label

    frame = simplegui.Frame('Set', (WIDTH, HEIGHT), CARD_W)
    frame.set_draw_handler(draw)
    frame.set_mouse_left_click_handler(mouse_left_click)
    frame.set_key_up_handler(key_up)
    frame.set_background_color("white")

    all_cards_image = simplegui.Image(CARDS_IMAGE_INFO)

    remaining_cards_label = frame.add_label("")
    sets_label = frame.add_label("")
    score_label = frame.add_label("")
    # ENHANCEMENT: add high score label
    frame.add_label("")

    frame.add_button("Deal More", deal_more, BUTTON_W, BUTTON_FONT_H)
    frame.add_button("New Game", new_game, BUTTON_W, BUTTON_FONT_H)
    
    return frame
    

if __name__ == '__main__':
    setup()
    
    new_game()
    frame.start()
    frame.quit()
