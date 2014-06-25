#!/usr/bin/env python
'''
Tetris, the game of falling and stacking blocks that collapse when a full row is created
Created on Jun 9, 2014

@author: Robb
'''
import simplegui
import sprite
import random

#SCREEN_SHOT_FILE = None
SCREEN_SHOT_FILE = "E:/Documents/projects/python_programs/30 days/tetris/tetris_screen_shot"
AUTO_SCREEN_SHOT = False

BLOCK_H = 30
WIDTH = 10*BLOCK_H
HEIGHT = 20*BLOCK_H

game_over = False
game_paused = False
cnt = 0
DROP = 20

blocks = []
current_tetroid = None
score = 0
lines = 0

control_state = dict([('left',False),('right',False),('down',False)])

TETROID_OFFSET_DICT = dict([('square',  (( 0,0),(0,1),(1,0),(1,1))),
                           ('zig-zag 1',((-1,0),(0,0),(0,1),(1,1))),
                           ('zig-zag 2',((-1,1),(0,0),(0,1),(1,0))),
                           ('tee',      ((-1,0),(0,0),(0,1),(1,0))),
                           ('L1',       ((-1,0),(0,0),(0,1),(0,2))),
                           ('L2',       (( 1,0),(0,0),(0,1),(0,2))),
                           ('line',     ((-1,0),(0,0),(1,0),(2,0)))])

TETROID_COLOR_DICT = dict([('square','FireBrick'),
                           ('zig-zag 1','SteelBlue'),
                           ('zig-zag 2','Plum'),
                           ('tee',(60,179,71)),
                           ('L1','Gold'),
                           ('L2',(220,94,56)),
                           ('line','SkyBlue')])

image_infos = dict([('dark_blue',simplegui.Image_Info('../lib/images/block_dark_blue.png',(BLOCK_H,BLOCK_H))),
                    ('light_blue',simplegui.Image_Info('../lib/images/block_light_blue.png',(BLOCK_H,BLOCK_H))),
                    ('red',simplegui.Image_Info('../lib/images/block_red.png',(BLOCK_H,BLOCK_H))),
                    ('green',simplegui.Image_Info('../lib/images/block_green.png',(BLOCK_H,BLOCK_H))),
                    ('yellow',simplegui.Image_Info('../lib/images/block_yellow.png',(BLOCK_H,BLOCK_H))),
                    ('purple',simplegui.Image_Info('../lib/images/block_purple.png',(BLOCK_H,BLOCK_H))),
                    ('orange',simplegui.Image_Info('../lib/images/block_orange.png',(BLOCK_H,BLOCK_H)))])
images = dict([])

TETROID_IMAGE_COLOR_DICT = dict([('square','red'),
                                 ('zig-zag 1','dark_blue'),
                                 ('zig-zag 2','purple'),
                                 ('tee','green'),
                                 ('L1','yellow'),
                                 ('L2','orange'),
                                 ('line','light_blue')])

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
        
        super(Tetroid, self).__init__(name,pos,size=(3*self.unit,3*self.unit),color=color)

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
        new_pos = [p + m for p, m in zip(block.pos, move)]
        for check_block in blocks:
            if check_block.pos == new_pos:
                return False
    return True

def remove_completed_rows():
    '''Removes any rows that are completed'''
    rows_to_remove = []
    if len(blocks)>0:
        highest_row = min([block.get_top_edge() for block in blocks])
        
        
        for i in range(int((HEIGHT - highest_row) / BLOCK_H + 1)):
            row = [block for block in blocks if (HEIGHT-block.get_top_edge())/BLOCK_H==i]
            
            if len(row) == WIDTH/BLOCK_H:
                rows_to_remove.append(i)
                
                for block in row:
                    blocks.remove(block)
    
    
        for block in blocks:
            x, y = block.pos
            del_y = BLOCK_H * len([i for i in rows_to_remove if (HEIGHT-block.get_top_edge())/BLOCK_H>i])
            block.pos = [x,y+del_y]
    return rows_to_remove

def increase_score(num_rows):
    '''Increase the score'''
    global score, lines
    lines += num_rows
    lines_label.text = 'Lines: '+str(lines)
    
    if num_rows == 4:
        num_rows *= 2
    score += num_rows*100
    score_label.text = 'Score: '+str(score)
        
def draw(canvas):
    '''Draw the board'''
    global cnt, game_over, current_tetroid
    
    if not game_paused and not game_over:
        cnt = (cnt + 1) % DROP
        
        if cnt % 2 == 0:
            for control,state in control_state.iteritems():
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
                [blocks.append(block) for block in current_tetroid.blocks]
                current_tetroid = next_tetroid()
                
                if not no_overlaps_w_blocks(current_tetroid.blocks,[0,0]):
                    game_over = True
                    
        current_tetroid.draw(canvas)
    
    removed_rows = remove_completed_rows()
    increase_score(len(removed_rows))
    
    for block in blocks:
        block.draw(canvas)
        
    if game_over:
        canvas.draw_rect([0.1*WIDTH,0.5*HEIGHT-BLOCK_H],[0.8*WIDTH,2*BLOCK_H],0,'Grey','Grey')
        canvas.draw_text('GAME OVER',[WIDTH/2,HEIGHT/2],40,'White',align=('center','middle'))
        
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
    tetroid.pos = [0.5*BLOCK_H+WIDTH/2,0.5*BLOCK_H]
    next_container.sprite = new_tetroid()
    return tetroid
    
def new_game():
    '''Clears the board and starts a new game'''
    global blocks, game_over, game_paused, current_tetroid
    
    blocks = []
    
    game_over = False
    game_paused = False
    
    current_tetroid = next_tetroid()
    

def key_down(key):
    '''Handles the key down events'''
    if control_state.has_key(key):
        control_state[key] = True
    

def key_up(key):
    '''Handles the key up events'''
    if control_state.has_key(key):
        control_state[key] = False
    elif key == 'a':
        if not game_paused:
            current_tetroid.rotate(-1)
    elif key == 's':
        if not game_paused:
            current_tetroid.rotate(+1)
    elif key == 'space':
        pause()
    elif key == 'return':
        new_game()
    

def pause():
    '''Pauses the game'''
    global game_paused
    game_paused = not game_paused
    
def setup():
    '''Setup the frame and event handlers'''
    global frame, next_container, score_label, lines_label, images
    frame = simplegui.Frame('Tetris',(WIDTH,HEIGHT),200)
    frame.set_draw_handler(draw)
    frame.set_key_down_handler(key_down)
    frame.set_key_up_handler(key_up)
    
    images = dict([(key, simplegui.Image(image_info)) for key, image_info in image_infos.iteritems()])
    #images = dict([(key, None) for key, image_info in image_infos.iteritems()])
    
    #Build the control panel
    frame.add_label('')
    next_container = frame.control_panel.add_sprite_container(new_tetroid())
    score_label = frame.add_label('Score: 0')
    lines_label = frame.add_label('Lines: 0')
    frame.add_label('')
    frame.add_label('Pause: space')
    frame.add_label('New Game: return')
    frame.add_label('Rotate: a,s')
    frame.add_label('Move: arrows')
    
    
    if SCREEN_SHOT_FILE:
        frame.set_screen_shot_file(SCREEN_SHOT_FILE)

if __name__ == '__main__':
    setup()
    
    new_game()
    frame.start()