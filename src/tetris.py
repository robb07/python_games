'''
Tetris, the game of falling and stacking blocks that collapse when a full row is created
Created on Jun 9, 2014

@author: Robb
'''
import simplegui
import random

BLOCK_H = 30
WIDTH = 12*BLOCK_H
HEIGHT = 20*BLOCK_H

game_over = False
game_paused = False
cnt = 0
DROP = 30

blocks = []
current_tetroid = None
next_tetroid = None
score = 0

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
                           ('line','Ivory')])

class Block(object):
    '''An individual block'''
    
    def __init__(self,pos,color,unit = BLOCK_H):
        '''Initializes the block'''
        self.pos = pos
        self.color = color
        self.unit = unit
        self.size = (unit,unit)
        
    def draw(self,canvas):
        '''Draws the block on the canvas'''
        canvas.draw_rect(self.pos,self.size,1,'Grey',self.color)
    
    def set_pos(self, pos):
        '''Set the position'''
        self.pos = pos
        
    def get_pos(self):
        '''Get the position'''
        return self.pos
    
class Tetroid(object):
    '''A piece of four blocks that falls'''
    
    def __init__(self,name,pos,offsets,color,unit = BLOCK_H):
        '''Initializes the tetroid'''
        self.name = name
        self.pos = pos
        self.rot = 0
        self.color = color
        self.offsets = offsets
        self.unit = unit
        self.blocks = [Block([pos[0]+offset[0]*unit,pos[1]+offset[1]*unit],color,unit) for offset in offsets]
        
    
    def draw(self, canvas):
        '''Draws the tetroid'''
        for block in self.blocks:
            block.draw(canvas)
    
    def get_name(self):
        '''Gets the name of the tetroid'''
        return self.name
    
    def set_pos(self, pos):
        '''Sets the position of the tetroid'''
        self.pos = pos
        self.update_blocks()
        
    def get_pos(self):
        '''Gets the position of the tetroid'''
        return self.pos
    
    def get_blocks(self):
        '''Gets the blocks that make up the tetroid'''
        return self.blocks
    
    def update_blocks(self):
        '''Updates the position of the blocks'''
        if self.rot == 0:
            rot_mat = [[1,0],[0,1]]
        elif self.rot == 1:
            rot_mat = [[0,1],[-1,0]]
        elif self.rot == 2:
            rot_mat = [[-1,0],[0,-1]]
        elif self.rot == 3:
            rot_mat = [[0,-1],[1,0]]
        
        for block, offset in zip(self.blocks, self.offsets):
            r_offset = [rot_mat[0][0]*offset[0]+rot_mat[0][1]*offset[1],rot_mat[1][0]*offset[0]+rot_mat[1][1]*offset[1]]
            block.set_pos([self.pos[0]+r_offset[0]*self.unit, self.pos[1]+r_offset[1]*self.unit])
            #needs the rotation 
            
    def rotate(self, direction):
        '''Rotates the tetroid +1 for clockwise, -1 for counterclockwise'''
        if not game_paused:
            self.rot = (self.rot + direction) % 4
            self.update_blocks()
            
            if any([block.get_pos()[0] < 0 or block.get_pos()[0] >= WIDTH or \
                    block.get_pos()[1] >= HEIGHT for block in self.blocks]) or \
               not no_overlaps_w_blocks(self.blocks,[0,0]):
                self.rot = (self.rot - direction) % 4
                self.update_blocks()
        
    def move_left(self):
        '''Moves the tetroid one unit to the left'''
        if all([block.get_pos()[0]-self.unit >= 0 for block in self.blocks]) and \
            no_overlaps_w_blocks(self.blocks,[-self.unit,0]) and \
            not game_paused:
            self.pos[0] -= self.unit
            self.update_blocks()
        
        
    def move_right(self):
        '''Moves the tetroid one unit to the right'''
        if all([block.get_pos()[0]+self.unit < WIDTH for block in self.blocks]) and \
            no_overlaps_w_blocks(self.blocks,[self.unit,0]) and \
            not game_paused:
            self.pos[0] += self.unit
            self.update_blocks()
        
        
    def move_down(self):
        '''Moves the tetroid one unit down'''
        if all([block.get_pos()[1]+self.unit < HEIGHT for block in self.blocks]) and \
            no_overlaps_w_blocks(self.blocks,[0,self.unit]) and \
            not game_paused:
            self.pos[1] += self.unit
            self.update_blocks()
        
def no_overlaps_w_blocks(tetroid_blocks, move):
    '''Checks to see if the blocks movement will overlap a laid down block'''
    for block in tetroid_blocks:
        new_pos = [p + m for p, m in zip(block.get_pos(), move)]
        for check_block in blocks:
            if check_block.get_pos() == new_pos:
                return False
    return True

def remove_completed_rows():
    '''Removes any rows that are completed'''
    global score
    if len(blocks)>0:
        highest_row = min([block.get_pos()[1] for block in blocks])
        rows_to_remove = []
        
        for i in range((HEIGHT - highest_row) / BLOCK_H + 1):
            row = [block for block in blocks if (HEIGHT-block.get_pos()[1])/BLOCK_H==i]
            
            if len(row) == WIDTH/BLOCK_H:
                rows_to_remove.append(i)
                
                for block in row:
                    blocks.remove(block)
        
        for block in blocks:
            x, y = block.get_pos()
            del_y = BLOCK_H * len([i for i in rows_to_remove if (HEIGHT-y)/BLOCK_H>i])
            block.set_pos([x,y+del_y])
        
        score += len(rows_to_remove)
        score_label.set_text('Score: '+str(score))
        
def draw(canvas):
    '''Draw the board'''
    global cnt, game_over, current_tetroid, next_tetroid
    
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
            old_pos = list(current_tetroid.get_pos())
            current_tetroid.move_down()
            if old_pos == current_tetroid.get_pos():
                [blocks.append(block) for block in current_tetroid.get_blocks()]
                current_tetroid, next_tetroid = next_tetroid, new_tetroid()
                next_label.set_text('Next: ' + next_tetroid.get_name())
                if not no_overlaps_w_blocks(current_tetroid.get_blocks(),[0,0]):
                    game_over = True
                    
        current_tetroid.draw(canvas)
    
    remove_completed_rows()
    
    for block in blocks:
        block.draw(canvas)
        
    if game_over:
        canvas.draw_rect([0.1*WIDTH,0.5*HEIGHT-BLOCK_H],[0.8*WIDTH,2*BLOCK_H],0,'Grey','Grey')
        canvas.draw_text('GAME OVER',[WIDTH/2,HEIGHT/2],40,'White',align=('center','middle'))
    
def new_tetroid():
    '''Creates a new random Tetroid'''
    key = random.choice(TETROID_OFFSET_DICT.keys())
    return Tetroid(key,[WIDTH/2,0*BLOCK_H],TETROID_OFFSET_DICT[key],TETROID_COLOR_DICT[key])

def new_game():
    '''Clears the board and starts a new game'''
    global blocks, game_over, game_paused, current_tetroid, next_tetroid
    
    blocks = []
    
    game_over = False
    game_paused = False
    
    current_tetroid = new_tetroid()
    next_tetroid = new_tetroid()
    next_label.set_text('Next: ' + next_tetroid.get_name())

def key_down(key):
    '''Handles the key down events'''
    if control_state.has_key(key):
        control_state[key] = True
    

def key_up(key):
    '''Handles the key up events'''
    if control_state.has_key(key):
        control_state[key] = False
    elif key == 'a':
        current_tetroid.rotate(-1)
    elif key == 's':
        current_tetroid.rotate(+1)
    elif key == 'p':
        pause()
    elif key == 'n':
        new_game()
    

def pause():
    '''Pauses the game'''
    global game_paused
    game_paused = not game_paused
    
def setup():
    '''Setup the frame and event handlers'''
    global frame, next_label, score_label
    frame = simplegui.Frame('Tetris',(WIDTH,HEIGHT),100)
    frame.set_draw_handler(draw)
    frame.set_key_down_handler(key_down)
    frame.set_key_up_handler(key_up)
    
    frame.add_label('')
    next_label = frame.add_label('Next: ?')
    score_label = frame.add_label('Score: 0')
    frame.add_label('')
    frame.add_label('Pause: p')
    frame.add_label('New Game: n')
    frame.add_label('Rotate: a,s')
    frame.add_label('Move: arrows')
    

if __name__ == '__main__':
    setup()
    
    new_game()
    frame.start()