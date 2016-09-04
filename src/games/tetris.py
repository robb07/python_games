#!/usr/bin/env python
'''
Tetris, the game of falling and stacking blocks that collapse when a full row is created
Created on Jun 9, 2014

@author: Robb
'''
from game_tools import simplegui
from game_tools import sprite
import random
import os

HISTORY_DIR = os.path.join(os.path.expanduser("~"),".python_games")
if not os.path.exists(HISTORY_DIR):
    os.makedirs(HISTORY_DIR)
TETRIS_HISTORY = os.path.join(HISTORY_DIR, "tetris")

SCREEN_SHOT_FILE = None
AUTO_SCREEN_SHOT = False

BLOCK_H = 30
WIDTH = 10*BLOCK_H
HEIGHT = 20*BLOCK_H
IMAGES_ON = False

game_over = False
game_paused = False
cnt = 0
DROP = 20

#blocks = []
block_rows = []

current_tetroid = None
score = 0
lines = 0

if os.path.exists(TETRIS_HISTORY):
    try:
        with open(TETRIS_HISTORY, 'r') as f_in:
            high_score = int(f_in.next().strip())
    except Exception as e:
        high_score = 0
else:
    high_score = 0

control_state = dict([('left',False),('right',False),('down',False)])

TETROID_OFFSET_DICT = dict([('square',  (( 0,0),(0,1),(1,0),(1,1))),
                           ('zig-zag 1',((-1,0),(0,0),(0,1),(1,1))),
                           ('zig-zag 2',((-1,1),(0,0),(0,1),(1,0))),
                           ('tee',      ((-1,0),(0,0),(0,1),(1,0))),
                           ('L1',       ((-1, 1),(-1,0),(0,0),(1,0))),
                           ('L2',       ((-1,-1),(-1,0),(0,0),(1,0))),
                           ('line',     ((-1,0),(0,0),(1,0),(2,0)))])

TETROID_COLOR_DICT = dict([('square','FireBrick'),
                           ('zig-zag 1','SteelBlue'),
                           ('zig-zag 2','Plum'),
                           ('tee',(60,179,71)),
                           ('L1','Gold'),
                           ('L2',(220,94,56)),
                           ('line','SkyBlue')])

image_infos = dict([('dark_blue',simplegui.Image_Info(simplegui.get_image_path('block_dark_blue.png'),(BLOCK_H,BLOCK_H))),
                    ('light_blue',simplegui.Image_Info(simplegui.get_image_path('block_light_blue.png'),(BLOCK_H,BLOCK_H))),
                    ('red',simplegui.Image_Info(simplegui.get_image_path('block_red.png'),(BLOCK_H,BLOCK_H))),
                    ('green',simplegui.Image_Info(simplegui.get_image_path('block_green.png'),(BLOCK_H,BLOCK_H))),
                    ('yellow',simplegui.Image_Info(simplegui.get_image_path('block_yellow.png'),(BLOCK_H,BLOCK_H))),
                    ('purple',simplegui.Image_Info(simplegui.get_image_path('block_purple.png'),(BLOCK_H,BLOCK_H))),
                    ('orange',simplegui.Image_Info(simplegui.get_image_path('block_orange.png'),(BLOCK_H,BLOCK_H)))])
images = dict([])

TETROID_IMAGE_COLOR_DICT = dict([('square','red'),
                                 ('zig-zag 1','dark_blue'),
                                 ('zig-zag 2','purple'),
                                 ('tee','green'),
                                 ('L1','yellow'),
                                 ('L2','orange'),
                                 ('line','light_blue')])

# Shortened clip from http://downloads.khinsider.com/game-soundtracks/album/tetris-gameboy-rip-/tetris-gameboy-02.mp3
# Converted to ogg for portability
SOUNDTRACK_FILE = simplegui.get_sound_path("tetris-gameboy-02_short.ogg")

class Block(sprite.Sprite):
    '''An individual block'''
    
    def __init__(self, pos, color, unit=BLOCK_H, image=None):
        '''Initializes the block'''
        super(Block, self).__init__('block',pos,size=(unit,unit),color=color,line_color='Black',line_width=1,image=image)
        
    def get_left_edge(self):
        '''Gets the left edge of the block'''
        return self.pos[0]-0.5*self.size[0]
    
    def get_right_edge(self):
        '''Gets the right edge of the block'''
        return self.pos[0]+0.5*self.size[0]
    
    def get_top_edge(self):
        '''Gets the top edge of the block'''
        return self.pos[1]-0.5*self.size[1]
    
    def get_bottom_edge(self):
        '''Gets the bottom edge of the block'''
        return self.pos[1]+0.5*self.size[1]
        
class Tetroid(sprite.Sprite):
    '''A piece of four blocks that falls'''
    
    def __init__(self,name,pos,offsets,color,unit = BLOCK_H, image=None):
        '''Initializes the tetroid'''
        self.blocks = []
        self.offsets = offsets
        self.unit = unit
        self.block_image = image
        
        super(Tetroid, self).__init__(name,pos,color=color)

        self.blocks = [Block([pos[0]+offset[0]*unit,pos[1]+offset[1]*unit],color,unit,image=image) for offset in offsets]
        
    def set_pos(self, pos):
        '''Sets the position of the tetroid'''
        self._pos = pos
        self.update_blocks()
         
    def get_pos(self):
        '''Gets the position of the tetroid'''
        return self._pos
    
    pos = property(get_pos, set_pos)
    
    def set_rot(self, rot):
        '''Sets the rotation of the tetroid'''
        self._rot = rot
        self.update_blocks()
        
    def get_rot(self):
        '''Gets the rotation of the tetroid'''
        return self._rot
    
    rot = property(get_rot, set_rot)
    
    def get_size(self):
        '''Gets the size of the tetroid'''
        return (max(b.pos[0] for b in self.blocks) - min(b.pos[0] for b in self.blocks) + self.unit,
                max(b.pos[1] for b in self.blocks) - min(b.pos[1] for b in self.blocks) + self.unit)
        
    def draw(self, canvas):
        '''Draws the tetroid'''
        for block in self.blocks:
            block.draw(canvas)
    
    def update_blocks(self):
        '''Updates the position of the blocks'''
        for block, offset in zip(self.blocks, self.offsets):
            block.pos = self.rotate_offset([offset[0]*self.unit, offset[1]*self.unit])
            
    def rotate(self, direction):
        '''Rotates the tetroid +1 for clockwise, -1 for counterclockwise'''
        super(Tetroid, self).rotate(direction)
        
        if any([block.pos[0] < 0 or block.pos[0] >= WIDTH or \
                block.pos[1] >= HEIGHT for block in self.blocks]) or \
           not no_overlaps_w_blocks(self.blocks,[0,0]):
            super(Tetroid, self).rotate(-direction)
        
    def move_left(self):
        '''Moves the tetroid one unit to the left'''
        if all([block.get_left_edge() > 0 for block in self.blocks]) and \
            no_overlaps_w_blocks(self.blocks,[-self.unit,0]):
            self.move([-self.unit, 0])
            
    def move_right(self):
        '''Moves the tetroid one unit to the right'''
        if all([block.get_right_edge() < WIDTH for block in self.blocks]) and \
            no_overlaps_w_blocks(self.blocks,[self.unit,0]):
            self.move([self.unit, 0])
            
    def move_down(self):
        '''Moves the tetroid one unit down'''
        if all([block.get_bottom_edge() < HEIGHT for block in self.blocks]) and \
            no_overlaps_w_blocks(self.blocks,[0,self.unit]):
            self.move([0, self.unit])
            
        
def no_overlaps_w_blocks(tetroid_blocks, move):
    '''Checks to see if the blocks movement will overlap a laid down block'''
    for block in tetroid_blocks:
        new_pos = (block.pos[0] + move[0], block.pos[1] + move[1])
        for check_block in block_rows[int(new_pos[1]/block.size[1])]:
            if check_block.pos == new_pos:
                return False
    return True

def drop_blocks(tetroid):
    '''Drops the blocks from the tetroid onto the board'''
    for block in tetroid.blocks:
        block_rows[int(block.pos[1]/block.size[1])].append(block)

def completed_rows():
    '''Return the completed row numbers'''
    return [i for i, row in enumerate(block_rows) if len(row) == WIDTH/BLOCK_H]

def remove_completed_rows(rows_to_remove):
    '''Removes any rows that are completed'''
    for i in rows_to_remove:
        for row in block_rows[:i]:
            for block in row:
                block.pos = [block.pos[0], block.pos[1]+BLOCK_H]
        block_rows.pop(i)
        block_rows.insert(0,[])

def increase_score(num_rows):
    '''Increase the score'''
    global score, lines, high_score
    lines += num_rows
    lines_label.text = 'Lines: '+str(lines)
    
    if num_rows == 4:
        num_rows *= 2
    score += num_rows*100
    score_label.text = 'Score: '+str(score)
    if score > high_score:
        high_score = score
        with open(TETRIS_HISTORY, 'w') as f_out:
            f_out.write(str(high_score))
    high_score_label.text = 'High Score: '+str(high_score)
    
        
def draw(canvas):
    '''Draw the board'''
    global cnt, game_over, current_tetroid, flashing_rows, flashes
    
    if not game_paused and not game_over:
        speed = DROP - (lines / 10)
        if speed < 1:
            speed = 1
        cnt = (cnt + 1) % speed
        
        if cnt % 2 == 0:
            for control, state in control_state.iteritems():
                if state:
                    if control == 'left':
                        current_tetroid.move_left()
                    elif control == 'right':
                        current_tetroid.move_right()
                    elif control == 'down':
                        current_tetroid.move_down()
                

    if current_tetroid:
        if cnt == 0 and not game_paused and not game_over:
            old_pos = list(current_tetroid.pos)
            current_tetroid.move_down()
            if old_pos == current_tetroid.pos:
                
                drop_blocks(current_tetroid)
                current_tetroid = next_tetroid()
                 
                if not no_overlaps_w_blocks(current_tetroid.blocks,[0,0]):
                    game_over = True
                    
        current_tetroid.draw(canvas)
    
    if flashes == 0:
        remove_completed_rows(flashing_rows)
        increase_score(len(flashing_rows))
        flashing_rows = []
    
    rows = completed_rows()
    if any(r not in flashing_rows for r in rows):
        flashing_rows = rows
        flashes = 4*len(flashing_rows)
    
    
    for row in block_rows:
        for block in row:
            block.draw(canvas)
    
    if (flashes / 2) % 2 == 0:
        for i in flashing_rows:
            canvas.draw_rect([0,i*BLOCK_H],[WIDTH,BLOCK_H],0,'White','White')
    flashes -= 1
    if game_over:
        canvas.draw_rect([0.1*WIDTH,0.5*HEIGHT-BLOCK_H],[0.8*WIDTH,2*BLOCK_H],0,'Grey','Grey')
        canvas.draw_text('GAME OVER',[WIDTH/2,HEIGHT/2],40,'White',align=('center','middle'))
        frame.stop_soundtrack()
        
    if AUTO_SCREEN_SHOT and cnt == 0 and not game_paused and not game_over:
        frame.screen_shot()
    
def new_tetroid():
    '''Creates a new random Tetroid'''
    key = random.choice(TETROID_OFFSET_DICT.keys())
    image = images[TETROID_IMAGE_COLOR_DICT[key]]
    tetroid = Tetroid(key,[0,0],TETROID_OFFSET_DICT[key],TETROID_COLOR_DICT[key],image=image)
    
    return tetroid

def next_tetroid():
    '''Sets the preview pane to the new tetroid and puts the previewed tetroid on the board'''
    tetroid = next_container.sprite
    tetroid.pos = [0.5*BLOCK_H+WIDTH/2,1.5*BLOCK_H]
    next_container.sprite = new_tetroid()
    return tetroid
    
def new_game():
    '''Clears the board and starts a new game'''
    global block_rows, game_over, game_paused, current_tetroid, flashing_rows, flashes, score, lines
    
    block_rows = [[] for _ in range(int(HEIGHT/BLOCK_H))]
    flashing_rows = []
    flashes = 0
    
    game_over = False
    game_paused = False
    
    frame.play_soundtrack()
    current_tetroid = next_tetroid()
    
    score = 0
    lines = 0
    

def key_down(key):
    '''Handles the key down events'''
    if control_state.has_key(key):
        control_state[key] = True
    

def key_up(key):
    '''Handles the key up events'''
    if control_state.has_key(key):
        control_state[key] = False
    elif key == 'a' or key == 'up':
        if not game_paused:
            current_tetroid.rotate(-1)
    elif key == 's':
        if not game_paused:
            current_tetroid.rotate(+1)
    elif key == 'space':
        pause()
    elif key == 'return':
        new_game()
    elif key == 'm':
        frame.toggle_mute()
    

def pause():
    '''Pauses the game'''
    global game_paused
    game_paused = not game_paused
    if game_paused:
        frame.pause_soundtrack()
    else:
        frame.unpause_soundtrack()

    
def setup():
    '''Setup the frame and event handlers'''
    global frame, next_container, score_label, lines_label, high_score_label, images

    frame = simplegui.Frame('Tetris',(WIDTH,HEIGHT),160, soundtrack=SOUNDTRACK_FILE)
    frame.set_draw_handler(draw)
    frame.set_key_down_handler(key_down)
    frame.set_key_up_handler(key_up)
    
    if IMAGES_ON:
        images = dict([(key, simplegui.Image(image_info)) for key, image_info in image_infos.iteritems()])
    else:
        images = dict([(key, None) for key, image_info in image_infos.iteritems()])
    
    #Build the control panel
    frame.add_label('')
    frame.add_label('')
    next_container = frame.control_panel.add_sprite_container(new_tetroid(),size=(3*BLOCK_H,3*BLOCK_H))
    score_label = frame.add_label('Score: 0')
    lines_label = frame.add_label('Lines: 0')
    frame.add_label('')
    high_score_label = frame.add_label('High Score: ' + str(high_score))
    
    if SCREEN_SHOT_FILE:
        frame.set_screen_shot_file(SCREEN_SHOT_FILE)
        
    return frame

if __name__ == '__main__':
    setup()
    
    new_game()
    frame.start()
    frame.quit()
