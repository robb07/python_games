#!/usr/bin/env python
'''
Created on Jul 16, 2014

@author: Robb
'''

from game_tools import simplegui
import string
import random
import os

PACKAGE_DIRECTORY = os.path.dirname(os.path.abspath(__file__))
MESSAGES_FILE = os.path.abspath(os.path.join(PACKAGE_DIRECTORY, '..', '..', 'lib', 'quips.txt'))

WIDTH = 800
HEIGHT = 850

BORDER = (40, 40)
FONT_DIM = (20, 20)
FONT_COLOR = 'Black' 
BACKGROUND_COLOR = 'Ivory'

MESSAGE_ROW_DIM = (WIDTH - 7*FONT_DIM[0],4*FONT_DIM[1])
plaintext = ''
ciphertext = ''
working_key = dict([])

controls = dict([('up',['up','left']),('down',['down','right'])])
control_states = dict([(control,False) for control in controls.iterkeys()]) 

cnt = 0
CONTROL_TICK = 10

selected_panel = 'message'
selected_index = 0
selection_len = 1

def encrypt_substitute(message, key):
    '''Encrypts the message with a substitution cipher'''
    return ''.join([key[m] if m in key else m for m in message])

def clean_text(message):
    '''Removes all symbols and spaces from a message'''
    return ''.join([m for m in message if m in string.ascii_letters])

def draw(canvas):
    '''Draws the cryptoquip'''
    global selected_index, cnt
    cnt += 1
    if cnt % CONTROL_TICK == 0:
        if control_states['up']:
            selected_index = (selected_index - 1) % selection_len
        elif control_states['down']:
            selected_index = (selected_index + 1) % selection_len
    
    working_text = encrypt_substitute(ciphertext, working_key)
    draw_message(canvas, ciphertext, BORDER, FONT_DIM, MESSAGE_ROW_DIM)
    draw_message(canvas, working_text, (BORDER[0], BORDER[1] + 1.5*FONT_DIM[1]), FONT_DIM, MESSAGE_ROW_DIM, selected_index=(selected_index if selected_panel == 'message' else None))
    if working_text == plaintext:
        canvas.draw_text('You win!',(BORDER[0],HEIGHT - BORDER[1] - 2*FONT_DIM[1]), 2*FONT_DIM[1], FONT_COLOR)
        
    canvas.draw_line((WIDTH - 4*FONT_DIM[0], BORDER[1]), (WIDTH - 4*FONT_DIM[0], HEIGHT - BORDER[1]), 1, FONT_COLOR)
    draw_key(canvas, working_key, (WIDTH - 4*FONT_DIM[0], BORDER[1]), FONT_DIM, selected_index=(selected_index if selected_panel == 'key' else None))

def draw_message(canvas, message, pos, font_dim, message_dim, selected_index=None):
    '''Draws the message on the canvas'''
    cols = int(message_dim[0] / font_dim[0])
    
    words = message.split(' ')
    curr_col = 0
    curr_row = 0
    w_index = 0
    for word in words:
        if len(word) + curr_col > cols:
            curr_row += 1
            curr_col = 0
        word_space = word + ' '
        for w in word_space:
            if selected_index == w_index and w in string.ascii_lowercase+'_':
                canvas.draw_rect((pos[0]+(curr_col-0.5)*font_dim[0], pos[1]+curr_row*message_dim[1]), (font_dim[0],1.3*font_dim[1]), 1, FONT_COLOR)
            canvas.draw_text(w, (pos[0]+curr_col*font_dim[0], pos[1]+curr_row*message_dim[1]),
                             font_dim[0], FONT_COLOR, font_face='serif', align=('center','top'))
            curr_col += 1
            if w in string.ascii_lowercase+'_':
                w_index += 1
        
    
def draw_key(canvas, key, pos, font_dim, selected_index=None):
    '''Draws the key on the canvas'''
    cipher_alphabet = string.ascii_uppercase
    for i, c in enumerate(cipher_alphabet):
        
        canvas.draw_text(c, (pos[0] + 1.0*font_dim[0], pos[1] + 1.5*i*font_dim[1]), font_dim[1], FONT_COLOR, font_face='serif', align=('center','top'))
        if selected_index == i:
            canvas.draw_rect((pos[0] + 2.0*font_dim[0], pos[1] + 1.5*i*font_dim[1]), (font_dim[0],1.3*font_dim[1]), 1, FONT_COLOR)
        canvas.draw_text(key[c], (pos[0] + 2.5*font_dim[0], pos[1] + 1.5*i*font_dim[1]), font_dim[1], FONT_COLOR, font_face='serif', align=('center','top'))
        
def new_key():
    '''Creates a new key'''
    cipher_alphabet = list(string.ascii_uppercase)
    random.shuffle(cipher_alphabet)
    return dict([(p,c) for p, c in zip(string.ascii_lowercase, cipher_alphabet)])
    
def new_game():
    '''Creates a new game'''
    global plaintext, ciphertext, working_key
    
    with open(MESSAGES_FILE,'r') as f_in:
        lines = [line.strip() for line in f_in if len(line) > 20 and line[0] != '#']
        
    plaintext = random.choice(lines).lower()
    key = new_key()
    ciphertext = encrypt_substitute(plaintext, key)
    working_key = dict([(c,'_') for c in string.ascii_uppercase])
    select_panel('message')
    
def select_panel(panel):
    '''Sets the selected panel'''
    global selected_panel, selection_len, selected_index
    if panel == 'message':
        selected_panel = 'message'
        selection_len = len(clean_text(ciphertext))
        selected_index = 0
    else:
        selected_panel = 'key'
        selection_len = len(working_key)
        selected_index = 0
        
def selected_letter(selected_index):
    '''Return the selected letter'''
    if selected_panel == 'message':
        return clean_text(ciphertext)[selected_index]
    else:
        return string.ascii_uppercase[selected_index]

def key_down(key):
    '''Key down handler'''
    global selected_index
    if key in controls['up']:
        control_states['up'] = True
        selected_index = (selected_index - 1) % selection_len
    elif key in controls['down']:
        control_states['down'] = True
        selected_index = (selected_index + 1) % selection_len
    
def key_up(key):
    '''Key up handler'''
    if key in controls['up']:
        control_states['up'] = False
    elif key in controls['down']:
        control_states['down'] = False
    elif key in string.ascii_letters:
        working_key[selected_letter(selected_index)] = key.lower()
    elif key == '_' or key == '-' or key =='delete' or key == 'backspace':
        working_key[selected_letter(selected_index)] = '_'
    elif key == 'return':
        new_game()

def mouse_click(pos):
    '''Mouse click handler'''
    if pos[0] < MESSAGE_ROW_DIM[0]:
        select_panel('message')        
    else:
        select_panel('key')
    
def setup():
    '''Sets up a new cryptoquip game'''
    global frame
    frame = simplegui.Frame('Cryptoquip', (WIDTH,HEIGHT),canvas_color=BACKGROUND_COLOR)
    
    frame.set_draw_handler(draw)
    frame.set_key_down_handler(key_down)
    frame.set_key_up_handler(key_up)
    frame.set_mouse_left_click_handler(mouse_click)
    
    return frame

if __name__ == '__main__':
    
    setup()
    
    new_game()
    frame.start()
    frame.quit()
    
