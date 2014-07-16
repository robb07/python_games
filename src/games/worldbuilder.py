'''
Opens up a world as a canvas to place objects

Created on Jun 23, 2014

@author: Robb
'''

from game_tools import simplegui
from games import world
from game_tools import sprite

WIDTH = 600
HEIGHT = 600

BACKGROUND_COLORS = simplegui.BACKGROUND_COLORS

BLOCK_H = 30
image_infos = dict([('dark_blue',simplegui.Image_Info('../lib/images/block_dark_blue.png',(BLOCK_H,BLOCK_H))),
                    ('light_blue',simplegui.Image_Info('../lib/images/block_light_blue.png',(BLOCK_H,BLOCK_H))),
                    ('red',simplegui.Image_Info('../lib/images/block_red.png',(BLOCK_H,BLOCK_H))),
                    ('green',simplegui.Image_Info('../lib/images/block_green.png',(BLOCK_H,BLOCK_H))),
                    ('yellow',simplegui.Image_Info('../lib/images/block_yellow.png',(BLOCK_H,BLOCK_H))),
                    ('purple',simplegui.Image_Info('../lib/images/block_purple.png',(BLOCK_H,BLOCK_H))),
                    ('orange',simplegui.Image_Info('../lib/images/block_orange.png',(BLOCK_H,BLOCK_H)))])
images = dict([])

cursor = None
cursor_colors = image_infos.keys()
cursor_color = cursor_colors[0]

def draw(canvas):
    '''Draw the world and builder'''
    if the_world:
        the_world.draw(canvas)
        
    if type(cursor) is sprite.Sprite:
        cursor.draw(canvas)

def mouse_click(pos):
    '''Handles the mouse click'''
    global cursor
    if type(cursor) is sprite.Sprite:
        selected_blocks = [block for block in the_world.blocks if block.contains(pos)]
        for block in selected_blocks:
            the_world.blocks.remove(block)
        the_world.blocks.append(cursor)
        cursor = new_cursor(pos)
    elif cursor == 'del':
        selected_blocks = [block for block in the_world.blocks if block.contains(pos)]
        for block in selected_blocks:
            the_world.blocks.remove(block)
        
def mouse_move(pos):
    '''Handles the mouse movement'''
    global cursor
    
#     if not cursor:
#         cursor = new_cursor(pos)
    if type(cursor) is sprite.Sprite:
        snap_pos = [(int(pos[0]/BLOCK_H)+0.5)*BLOCK_H,(int(pos[1]/BLOCK_H)+0.5)*BLOCK_H]
        cursor.set_pos(snap_pos)

def key_down(key):
    '''Handles the key down event'''
    pass

def key_up(key):
    '''Handle the key up event'''
    global cursor_color, cursor
    if key == 'c':
        cursor_color = cursor_colors[(cursor_colors.index(cursor_color)+1) % len(cursor_colors)]
        if type(cursor) is sprite.Sprite:
            cursor.image = images[cursor_color]
        else:
            cursor = new_cursor([0,0])
    elif key == 'p':
        print the_world
    elif key == 'b':
        the_world.background_color = BACKGROUND_COLORS[(BACKGROUND_COLORS.index(the_world.background_color)+1) % len(BACKGROUND_COLORS)]
    elif key == 'd':
        cursor = 'del'
        
def setup():
    '''Setup the frame and event handlers'''
    global frame, images
    frame = simplegui.Frame('World',(WIDTH,HEIGHT))
    frame.set_draw_handler(draw)
    frame.set_key_down_handler(key_down)
    frame.set_key_up_handler(key_up)
    frame.set_mouse_left_click_handler(mouse_click)
    frame.set_mouse_move_handler(mouse_move)
    
    
    images = dict([(key, simplegui.Image(image_info)) for key, image_info in image_infos.iteritems()])
    return frame

def new_world():
    '''Makes a new world'''
    global the_world
    the_world = games.world.World((WIDTH,HEIGHT),'Black')
    
def new_cursor(pos):
    '''Makes a new cursor'''
    return sprite.Sprite('block',pos,size=(BLOCK_H,BLOCK_H),image=images[cursor_color])
    
if __name__ == '__main__':
    setup()
    
    new_world()
    frame.start()
    frame.quit()