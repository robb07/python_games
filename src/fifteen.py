'''
The fifteen tile puzzle game.

Created on Jun 7, 2014

@author: Robb
'''

import simplegui
import random

# globals
NUM = 4
NUM_COLS = NUM
NUM_ROWS = NUM
NUM_TOTAL = NUM_COLS*NUM_ROWS

BUTTON_W = 200
CANVAS_W = 600
CANVAS_H = 600

TILE_W = CANVAS_W / (2 + NUM_COLS)
TILE_H = CANVAS_H / (2 + NUM_ROWS)
FONT_H = TILE_H // 2
BUTTON_FONT_H = 20

ROWS = [str(num) for num in range(NUM_ROWS)]
COLS = [chr(ord('A') + let) for let in range(NUM_COLS)]

SPACES = [c + r for r in ROWS for c in COLS]

TILE_COLOR = dict({0:'FireBrick', 1:'Ivory'})
LETTER_COLOR = dict({0:'Ivory', 1:'FireBrick'})

swapping_space = None
swapping_count = 0.
SWAP_STOP = 10.

# helper functions
def new_board():
    '''Creates a new board'''
    global tiles, board
    
    tiles = [num for num in range(1, NUM_TOTAL)]
    tiles.append(0)
        
    board = {}
    for space,tile in zip(SPACES,tiles):
        board[space] = tile
    
    #print board

def get_space_pos(space):
    '''Finds the position for a space'''
    col = COLS.index(space[0])
    row = ROWS.index(space[1])
    
    x_offset = TILE_W + col * TILE_W
    y_offset = TILE_H + row * TILE_H
    
    return (x_offset, y_offset)

def get_space(pos):
    '''Finds the space for a position'''
    col = (pos[0] - TILE_W) // TILE_W
    row = (pos[1] - TILE_H) // TILE_H
    
    if col in range(NUM_COLS) and row in range(NUM_ROWS):
        return COLS[col] + ROWS[row]
    else:
        return None

def get_blank_space():
    '''Finds the blank space'''
    blank = [key for key, val in board.items() if val == 0]
    return blank[0]

def move_tile(space):
    '''Moves a tile be swapping it with the blank space'''
    global swapping_space
    if space in SPACES:
        blank = get_blank_space()
        if blank != space:
            r = abs(ord(blank[0]) - ord(space[0]))
            c = abs(ord(blank[1]) - ord(space[1]))
            if r + c <= 1:
                swapping_space = blank
                board[space], board[blank] = board[blank], board[space]
            

# event handlers
def draw(canvas):
    '''Draws the canvas'''
    global swapping_space, swapping_count
    
    for space in SPACES:
        if board[space] != 0 and swapping_space != space:
            pos = get_space_pos(space)
            
            canvas.draw_rect(pos, (TILE_W, TILE_H), 4, 'Black', TILE_COLOR[board[space] % 2])
            
            #canvas.draw_text(str(board[space]), pos, FONT_H, LETTER_COLOR[board[space] % 2], 'sans-serif', ('left', 'top'))
            canvas.draw_text(str(board[space]), (pos[0] + TILE_W/2, pos[1] + TILE_H/2), FONT_H, LETTER_COLOR[board[space] % 2], 'sans-serif', ('center', 'middle'))
            #canvas.draw_text(str(board[space]), [pos[0] + TILE_W, pos[1] + TILE_H], FONT_H, LETTER_COLOR[board[space] % 2], 'sans-serif', ('right', 'bottom'))
        elif swapping_space == space:
            blank_pos = get_space_pos(get_blank_space())
            dest_pos = get_space_pos(space)
            delta_x = dest_pos[0] - blank_pos[0]
            delta_y = dest_pos[1] - blank_pos[1]
            pos = (blank_pos[0] + delta_x*swapping_count/SWAP_STOP,
                   blank_pos[1] + delta_y*swapping_count/SWAP_STOP)
            swapping_count += 1.
            if swapping_count == SWAP_STOP:
                swapping_count = 0.
                swapping_space = None
                
            canvas.draw_rect(pos, (TILE_W, TILE_H), 4, 'Black', TILE_COLOR[board[space] % 2])
            
            canvas.draw_text(str(board[space]), (pos[0] + TILE_W/2, pos[1] + TILE_H/2), FONT_H, LETTER_COLOR[board[space] % 2], 'sans-serif', ('center', 'middle'))
    
        
def shuffle_button():
    '''Shuffles the board'''
    shuffles = 1000
    while shuffles > 0:
        direction = random.randrange(4)
        blank = get_blank_space()
        if direction == 0:
            space = chr(ord(blank[0]) - 1) + blank[1]
        elif direction == 1:
            space = chr(ord(blank[0]) + 1) + blank[1]
        elif direction == 2:
            space = blank[0] + chr(ord(blank[1]) - 1)
        else:
            space = blank[0] + chr(ord(blank[1]) + 1)
        
        if space in SPACES:
            move_tile(space)
            shuffles -= 1

def reset_button():
    '''Resets the board'''
    new_board()

def click(pos):
    '''Finds the tile to move'''
    space = get_space(pos)
    
    if space:
        move_tile(space)

def key_up(key):
    '''Presses the buttons using the keyboard'''
    if key == 'r':
        reset_button()
    elif key == 's':
        shuffle_button()

if __name__ == '__main__':
    # create frame

    frame = simplegui.Frame('Fifteen',(CANVAS_W, CANVAS_H),BUTTON_W)
    
    # register event handlers
    frame.set_draw_handler(draw)
    frame.add_button("Reset tiles", reset_button, BUTTON_W, BUTTON_FONT_H)
    frame.add_button("Shuffle tiles", shuffle_button, BUTTON_W, BUTTON_FONT_H)
    frame.set_key_up_handler(key_up)
    frame.set_mouse_left_click_handler(click)
    
    new_board()
    frame.start()
    