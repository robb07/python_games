#!/usr/bin/env python
'''

Snake, the game of steering a snake towards food and away from itself.

Created on Jun 11, 2014

@author: Robb
'''

from game_tools import simplegui
from game_tools import sprite
import random

SCREEN_SHOT_FILE = None
AUTO_SCREEN_SHOT = False

WIDTH = 600
HEIGHT = 400
UNIT = 40
MOVE_COUNT = 30
BACKGROUND_COLOR = 'SteelBlue'
FOOD_COLOR = 'White'
IMAGES_ON = True

game_over = False
game_paused = False
move_count = 0
snake = None
food = None

image_infos = dict([('head',simplegui.Image_Info(simplegui.get_image_path('snake_head.png'),(UNIT,UNIT))),
                    ('neck',simplegui.Image_Info(simplegui.get_image_path('snake_neck.png'),(UNIT,UNIT))),
                    ('straight',simplegui.Image_Info(simplegui.get_image_path('snake_body_straight.png'),(UNIT,UNIT))),
                    ('left',simplegui.Image_Info(simplegui.get_image_path('snake_body_left.png'),(UNIT,UNIT))),
                    ('right',simplegui.Image_Info(simplegui.get_image_path('snake_body_right.png'),(UNIT,UNIT))),
                    ('tail',simplegui.Image_Info(simplegui.get_image_path('snake_tail.png'),(UNIT,UNIT))),
                    ('food',simplegui.Image_Info(simplegui.get_image_path('snake_food.png'),(UNIT,UNIT)))])
images = dict([])


def draw_head(head, canvas):
    '''Draws the head and eyes'''
    head.draw(canvas,default=True)
    eye1_pos = head.rotate_offset([0.25*head.size[0], 0.25*head.size[1]])
    eye2_pos = head.rotate_offset([0.25*head.size[0], -0.25*head.size[1]])
    canvas.draw_circle(eye1_pos,2,1,'Black','Black')
    canvas.draw_circle(eye2_pos,2,1,'Black','Black')
    
def draw_tail(tail, canvas):
    '''Draws the tail'''
    #tail.draw(canvas,default=True)
    tri_pts = [tail.rotate_offset([ 0.5*tail.size[0],  0.5*tail.size[1]]),
               tail.rotate_offset([ 0.5*tail.size[0], -0.5*tail.size[1]]),
               tail.rotate_offset([-0.5*tail.size[0],                0.])]
    canvas.draw_polygon(tri_pts, tail.line_width, tail.line_color, tail.color)
    
    
class Snake(object):
    '''
    Snake that moves around the screen growing and eating.
    '''
    
    def __init__(self,start_pos, vel = [UNIT, 0], unit_size = UNIT, color = 'Gold', images=None):
        '''Constructor'''
        if images is None:
            self.images = dict([(key,None) for key in ['head','neck','tail','straight','left','right']])
        else:
            self.images = images
        self.head = sprite.Sprite('head', start_pos, vel, 0, (unit_size,unit_size), color, draw_method=draw_head, image=self.images['head'], update_method=sprite.update_toroid)
        self.neck = sprite.Sprite('neck', start_pos, vel, self.head.rot, (unit_size,unit_size), color, image=self.images['neck'])
        self.body = []
        self.tail = None
        self.size = (unit_size,unit_size)
        self.color = color
        self.controls = dict([('left',1),('right',-1)])
        
    
    def update(self):
        '''Update the snakes position, try to eat food, and grow'''
        new_seg = sprite.Sprite('seg',self.head.pos,[0,0],self.head.rot,self.size,self.color,image=self.images['straight'])
        
        self.head.update((WIDTH,HEIGHT))
        if self.neck.rot != self.head.rot:
            if (self.head.rot - self.neck.rot) % 4 == 1:
                new_seg.image = self.images['left']
            else:
                new_seg.image = self.images['right']
            self.neck.rot = self.head.rot
        self.neck.pos = self.head.pos
        if self.eat_food():
            self.body.append(new_seg)
        else:
            self.body.append(new_seg)
            old_seg = self.body.pop(0)
            if self.tail:
                self.tail.pos = old_seg.pos
                self.tail.rot = old_seg.rot
        
        if self.tail is None and len(self.body) > 0:
            self.tail = self.body.pop(0)
            self.tail.name = 'tail'
            self.tail.draw_method = draw_tail
            #self.tail.image = None
            self.tail.image = self.images['tail']
        
    def draw(self, canvas):
        '''Draws the snake on the canvas'''
        if self.tail:
            self.tail.draw(canvas)
            self.neck.draw(canvas)
        for segment in self.body:
            segment.draw(canvas)
        
        self.head.draw(canvas)
            
    def eat_food(self):
        '''Eats the food if the head finds it'''
        global food
        if food and self.head.pos == food.pos:
            food = None
            return True
        else:
            return False
    
    def turn(self, direction):
        '''Turn the snake's head'''
        self.head.rotate(direction)
        vel = self.head.vel
        if direction == -1:
            self.head.vel = [-1*vel[1], vel[0]]
        else:
            self.head.vel = [vel[1], -1*vel[0]]
    
    def control(self, key):
        '''Accept a control input'''
        if self.controls.has_key(key):
            self.turn(self.controls[key])
        
    def check_collision(self):
        '''Check for collisions with the snake body'''
        if any([seg.pos == self.head.pos for seg in self.body]):          
            return True
        elif self.tail and self.tail.pos == self.head.pos:
            return True
        else:
            return False
    
    def is_on(self, other_sprite):
        '''Checks to see if the any part of the snake is on the position'''
#         if self.head.pos == pos:
#             return True
#         if self.tail and self.tail.pos == pos:
#             return True
#         return any([seg.pos==pos for seg in self.body])
        if self.head.overlaps(other_sprite):
            return True
        if self.tail and self.tail.overlaps(other_sprite):
            return True
        return any(seg.overlaps(other_sprite) for seg in self.body)
    
def new_food():
    '''Put new food down'''
    food_pos = rand_pos()
    while snake.is_on(sprite.Sprite(pos=food_pos,size=[UNIT,UNIT])):
        food_pos = rand_pos()
    return sprite.Sprite('food',food_pos,[0,0],0,[UNIT,UNIT],FOOD_COLOR,line_color=FOOD_COLOR,draw_method=sprite.draw_circle,image=images['food'])

def new_game():
    '''Create a new game'''
    global snake, food
    food = None
    snake = Snake(rand_pos(),images=images)

def rand_pos():
    '''Creates a random position on the board'''
    return [random.randrange(WIDTH/UNIT)*UNIT + 0.5*UNIT,random.randrange(HEIGHT/UNIT)*UNIT + 0.5*UNIT]

def key_down(key):
    '''Key down Handler'''
    if snake:
        snake.control(key)

def key_up(key):
    '''Key up handler'''
    global game_paused
    if key == 'space':
        game_paused = not game_paused
    elif key == 'return':
        new_game()

def mouse_click(pos):
    '''Mouse click handler'''
    global game_over, game_paused
    if game_over:
        game_over = False
        new_game()
    if game_paused:
        game_paused = False

def draw(canvas):
    '''Draw the board and pieces'''
    global food, move_count, game_over
    if food is None:
        food = new_food()
    
    food.draw(canvas)
    snake.draw(canvas)
        
    if not game_over:
        move_count = (move_count + 1) % MOVE_COUNT
        if not game_paused and move_count == 0:
            snake.update()
            if snake.check_collision():
                game_over = True
                
    else:
        canvas.draw_rect([0.2*WIDTH,0.5*HEIGHT-UNIT],[0.6*WIDTH,2*UNIT],0,(128,128,128),(128,128,128))
        canvas.draw_text('GAME OVER',[WIDTH/2,HEIGHT/2],40,'White',align=('center','middle'))
        
    if AUTO_SCREEN_SHOT and move_count == 0 and not game_paused and not game_over:
        frame.screen_shot()

def setup():
    '''Setup the frame and controls'''
    global frame, images
    
    frame = simplegui.Frame('Snake',(WIDTH,HEIGHT))
    
    frame.set_background_color(BACKGROUND_COLOR)
    frame.set_draw_handler(draw)
    
    frame.set_key_down_handler(key_down)
    frame.set_key_up_handler(key_up)
    frame.set_mouse_left_click_handler(mouse_click)
    
    #configure images
    if IMAGES_ON:
        images = dict([(key, simplegui.Image(image_info)) for key, image_info in image_infos.iteritems()])
    else:
        images = dict([(key, None) for key, image_info in image_infos.iteritems()])
        
    if SCREEN_SHOT_FILE:
        frame.set_screen_shot_file(SCREEN_SHOT_FILE)
        
    return frame

if __name__ == '__main__':
    setup()
    
    new_game()
    frame.start()
    frame.quit()