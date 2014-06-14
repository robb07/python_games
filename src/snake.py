'''

Snake, the game of steering a snake towards food and away from itself.

Created on Jun 11, 2014

@author: Robb
'''

import simplegui
import sprite
import random

#SCREEN_SHOT_FILE = None
SCREEN_SHOT_FILE = "E:/Documents/projects/python_programs/30 days/snake/snake_screen_shot"
AUTO_SCREEN_SHOT = False

WIDTH = 600
HEIGHT = 400
UNIT = 40
MOVE_COUNT = 30
BACKGROUND_COLOR = 'SteelBlue'
FOOD_COLOR = 'White'

game_over = False
game_paused = False
move_count = 0
snake = None
food = None

image_infos = dict([('head',simplegui.Image_Info('../lib/images/snake_head.png',(UNIT,UNIT))),
                    ('neck',simplegui.Image_Info('../lib/images/snake_neck.png',(UNIT,UNIT))),
                    ('straight',simplegui.Image_Info('../lib/images/snake_body_straight.png',(UNIT,UNIT))),
                    ('left',simplegui.Image_Info('../lib/images/snake_body_left.png',(UNIT,UNIT))),
                    ('right',simplegui.Image_Info('../lib/images/snake_body_right.png',(UNIT,UNIT))),
                    ('tail',simplegui.Image_Info('../lib/images/snake_tail.png',(UNIT,UNIT))),
                    ('food',simplegui.Image_Info('../lib/images/snake_food.png',(UNIT,UNIT)))])
images = dict([])


def draw_food(the_food,canvas):
    '''Draws the food as a circle'''
    canvas.draw_circle(the_food.get_pos(),the_food.get_size()[0]/2,the_food.line_width,the_food.line_color,the_food.color)

def draw_head(head, canvas):
    '''Draws the head and eyes'''
    head.draw(canvas,default=True)
    offset = [0.25*s for s in head.get_size()]
    rot_mat = head.get_rot_mat()
    r_offset1 = [rot_mat[0][0]*offset[0]+rot_mat[0][1]*offset[1],rot_mat[1][0]*offset[0]+rot_mat[1][1]*offset[1]]
    r_offset2 = [rot_mat[0][0]*offset[0]+rot_mat[0][1]*-1*offset[1],rot_mat[1][0]*offset[0]+rot_mat[1][1]*-1*offset[1]]
    eye1_pos = [head.get_pos()[0]+r_offset1[0], head.get_pos()[1]+r_offset1[1]]
    eye2_pos = [head.get_pos()[0]+r_offset2[0], head.get_pos()[1]+r_offset2[1]]
    canvas.draw_circle(eye1_pos,2,1,'Black','Black')
    canvas.draw_circle(eye2_pos,2,1,'Black','Black')
    
def draw_tail(tail, canvas):
    '''Draws the tail'''
    #tail.draw(canvas,default=True)
    offset = [0.5*t for t in tail.get_size()]
    rot_mat = tail.get_rot_mat()
    r_offset1 = [rot_mat[0][0]*offset[0]+rot_mat[0][1]*offset[1],rot_mat[1][0]*offset[0]+rot_mat[1][1]*offset[1]]
    r_offset2 = [rot_mat[0][0]*offset[0]+rot_mat[0][1]*-1*offset[1],rot_mat[1][0]*offset[0]+rot_mat[1][1]*-1*offset[1]]
    r_offset3 = [rot_mat[0][0]*-1*offset[0]+rot_mat[0][1]*0*offset[1],rot_mat[1][0]*-1*offset[0]+rot_mat[1][1]*0*offset[1]]
    tri_pts = [[tail.get_pos()[0]+r_offset1[0], tail.get_pos()[1]+r_offset1[1]],
               [tail.get_pos()[0]+r_offset2[0], tail.get_pos()[1]+r_offset2[1]],
               [tail.get_pos()[0]+r_offset3[0], tail.get_pos()[1]+r_offset3[1]]]
    canvas.draw_polygon(tri_pts, tail.line_width, tail.line_color, tail.color)
    
    
class Snake(object):
    '''
    Snake that moves around the screen growing and eating.
    '''
    
    def __init__(self,start_pos, vel = [UNIT, 0], unit_size = UNIT, color = 'Gold'):
        '''Constructor'''
        self.head = sprite.Sprite(start_pos, vel, 0, (unit_size,unit_size), color, draw_method=draw_head, image=images['head'])
        self.neck = sprite.Sprite(start_pos, vel, self.head.get_rot(), (unit_size,unit_size), color, image=images['neck'])
        self.body = []
        self.tail = None
        self.size = (unit_size,unit_size)
        self.color = color
        self.controls = dict([('left',1),('right',-1)])
        
    
    def update(self):
        '''Update the snakes position, try to eat food, and grow'''
        new_seg = sprite.Sprite(self.head.get_pos(),[0,0],self.head.get_rot(),self.size,self.color,image=images['straight'])
        
        self.head.update((WIDTH,HEIGHT))
        if self.neck.rot != self.head.get_rot():
            if (self.head.get_rot() - self.neck.rot) % 4 == 1:
                new_seg.image = images['left']
            else:
                new_seg.image = images['right']
            self.neck.set_rot(self.head.get_rot())
        self.neck.set_pos(self.head.get_pos())
        if self.eat_food():
            self.body.append(new_seg)
        else:
            self.body.append(new_seg)
            old_seg = self.body.pop(0)
            if self.tail:
                self.tail.set_pos(old_seg.get_pos())
                self.tail.set_rot(old_seg.get_rot())
        
        if self.tail is None and len(self.body) > 0:
            self.tail = self.body.pop(0)
            self.tail.draw_method = draw_tail
            #self.tail.image = None
            self.tail.image = images['tail']
        
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
        if food and self.head.get_pos() == food.get_pos():
            food = None
            return True
        else:
            return False
    
    def turn(self, direction):
        '''Turn the snake's head'''
        self.head.rotate(direction)
        vel = self.head.get_vel()
        if direction == -1:
            self.head.set_vel([-1*vel[1], vel[0]])
        else:
            self.head.set_vel([vel[1], -1*vel[0]])
    
    def control(self, key):
        '''Accept a control input'''
        if self.controls.has_key(key):
            self.turn(self.controls[key])
        
    def check_collision(self):
        '''Check for collisions with the snake body'''
        #if self.head.get_pos()[0] < 0 or  WIDTH < self.head.get_pos()[0] or \
        #   self.head.get_pos()[1] < 0 or HEIGHT < self.head.get_pos()[1] or \
        if any([seg.get_pos() == self.head.get_pos() for seg in self.body]):          
            return True
        else:
            return False
    
    def is_on(self, pos):
        '''Checks to see if the any part of the snake is on the position'''
        if self.head.get_pos() == pos:
            return True
        return any([seg.get_pos()==pos for seg in self.body])
    
def new_food():
    '''Put new food down'''
    food_pos = rand_pos()
    while snake.is_on(food_pos):
        food_pos = rand_pos()
    return sprite.Sprite(food_pos,[0,0],0,[UNIT,UNIT],FOOD_COLOR,line_color=FOOD_COLOR,draw_method=draw_food,image=images['food'])

def new_game():
    '''Create a new game'''
    global snake, food
    food = None
    snake = Snake(rand_pos())

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
    if key == 'p' or key == 'space':
        game_paused = not game_paused

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
    
    images = dict([(key, simplegui.Image(image_info)) for key, image_info in image_infos.iteritems()])
    
    if SCREEN_SHOT_FILE:
        frame.set_screen_shot_file(SCREEN_SHOT_FILE)

if __name__ == '__main__':
    setup()
    
    new_game()
    frame.start()