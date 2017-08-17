#!/usr/bin/env python
'''
Set, the game of matching cards by similarity and differences
Created August 16, 2017

@author: Robb
'''

import random
from game_tools import simplegui

PAD_W = 10
PAD_H = 10
CARD_W = 120
CARD_H = 180
WIDTH = 6*CARD_W
HEIGHT = 4*CARD_H

CARDS_IMAGE_INFO = simplegui.Image_Info(simplegui.get_image_path('set_shapes.png'), (6*(CARD_W + PAD_W), 6*(CARD_H + PAD_H)))

cards_dict = dict([])
keys = []

def draw(canvas):
    '''Draw the board'''
    global keys, ticker
    if ticker == 0:
        keys = random.sample(cards_dict.keys(), 12)
        ticker = 20

    for i, k in enumerate(keys):
        row = i // 4
        col = i % 4
        canvas.draw_image(cards_dict[k], ((0.5+col)*(CARD_W+PAD_W), (0.5+row)*(CARD_H+PAD_H)))

    ticker -= 1

def setup():
    '''Setup the frame and event handlers'''
    global frame, all_cards_image, cards_dict, ticker

    frame = simplegui.Frame('Set', (WIDTH, HEIGHT))
    frame.set_draw_handler(draw)
    frame.set_background_color("white")

    ticker = 0
    all_cards_image = simplegui.Image(CARDS_IMAGE_INFO)
    
    # cards are organized in x direction by number (larger distance) then pattern
    # and in the y direction by color then shape
    for n in xrange(3):
        for p in xrange(3):
            for c in xrange(3):
                for s in xrange(3):
                    pos_offset = ((3*n + p)*(CARD_W + PAD_W), (3*c + s)*(CARD_H + PAD_H))
                    cards_dict[(n, p, c, s)] = simplegui.SubImage(all_cards_image, pos_offset, (CARD_W, CARD_H))

if __name__ == '__main__':
    setup()
    
    frame.start()
    frame.quit()
