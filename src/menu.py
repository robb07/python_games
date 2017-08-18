#!/usr/bin/env python
'''
Menu for picking the game to play.

Created on Jul 12, 2014

@author: Robb
'''

from game_tools import simplegui
from games import fifteen
from games import breakout
from games import pong
from games import snake
from games import tetris
from games import cryptoquip
from games import setgame

HEIGHT = 400
CONTROL_WIDTH = 200
BUTTON_WIDTH = 0.9*CONTROL_WIDTH
BUTTON_FONT_SIZE = 20

selected_button = None

def game_starter(the_game):
    '''Start a game'''
    the_frame = the_game.setup()
    the_game.new_game()
    the_frame.start()
    
    frame.start()


def fifteen_starter():
    '''Starts the fifteen game'''
    game_starter(fifteen)

def pong_starter():
    '''Starts the pong game'''
    game_starter(pong)

def tetris_starter():
    '''Starts the tetris game'''
    game_starter(tetris)

def snake_starter():
    '''Starts the snake game'''
    game_starter(snake)

def breakout_starter():
    '''Starts the breakout game'''
    game_starter(breakout)

def cryptoquip_starter():
    '''Starts the cryptoquip game'''
    game_starter(cryptoquip)
    
def setgame_starter():
    '''Starts the set game'''
    game_starter(setgame)
    
def key_up(key):
    '''Handles the key up events'''
    if key == 'down' or key =='right':
        change_selected_button(1)
    elif key == 'up' or key == 'left':
        change_selected_button(-1)
    elif key == 'return':
        buttons[selected_button].call_handler()
    
    
def change_selected_button(direction):
    '''Changes which button is selected'''
    global selected_button
    if selected_button is None:
        selected_button = 0
    else:
        buttons[selected_button].color = 'grey'
        selected_button = (selected_button + direction) % len(buttons)
    buttons[selected_button].color = 'white'
    
    
def setup():
    '''Setup the menu for the games.'''
    global frame, buttons
    
    frame = simplegui.Frame('Menu',(0,HEIGHT),CONTROL_WIDTH)
    frame.set_key_up_handler(key_up)
    
    frame.add_label('Menu')
    
    buttons = []
    buttons.append(frame.add_button('Fifteen', fifteen_starter, BUTTON_WIDTH, BUTTON_FONT_SIZE))
    buttons.append(frame.add_button('Pong', pong_starter, BUTTON_WIDTH, BUTTON_FONT_SIZE))
    buttons.append(frame.add_button('Tetris', tetris_starter, BUTTON_WIDTH, BUTTON_FONT_SIZE))
    buttons.append(frame.add_button('Snake', snake_starter, BUTTON_WIDTH, BUTTON_FONT_SIZE))
    buttons.append(frame.add_button('Breakout', breakout_starter, BUTTON_WIDTH, BUTTON_FONT_SIZE))
    buttons.append(frame.add_button('Cryptoquip', cryptoquip_starter, BUTTON_WIDTH, BUTTON_FONT_SIZE))
    buttons.append(frame.add_button('Set', setgame_starter, BUTTON_WIDTH, BUTTON_FONT_SIZE))
    
    return frame

if __name__ == '__main__':
    setup()
    
    frame.start()
    frame.quit()
