'''

Snake, the game of steering a snake towards food and away from itself.

Created on Jun 11, 2014

@author: Robb
'''

import simplegui
import sprite

WIDTH = 600
HEIGHT = 400
UNIT = 20
MOVE_COUNT = 30
BACKGROUND_COLOR = 'SteelBlue'
FOOD_COLOR = 'White'

game_over = True
move_count = 0
snake = None
food = None

class Snake(object):
    '''
    Snake that moves around the screen growing and eating.
    '''
    
    def __init__(self,start_pos, vel = [UNIT, 0], unit_size = UNIT, color = 'Gold'):
        '''Constructor'''
        self.head = sprite.Sprite(start_pos, vel, 0, (unit_size,unit_size), color)
        self.body = []
        #self.tail = sprite.Sprite(start_pos)
        self.size = (unit_size,unit_size)
        self.color = color
        #self.control_state = dict([('left',False),('right',False)])
        self.controls = dict([('left',-1),('right',1)])
    
    def update(self):
        '''Update the snakes position, try to eat food, and grow'''
#         if self.control_state['left']:
#             self.turn(-1)
#         elif self.control_state['right']:
#             self.turn(1)
#             
        new_seg = sprite.Sprite(self.head.get_pos(),[0,0],0,self.size,self.color)
        
        self.head.update()
        if self.eat_food():
            print 'grow'
            self.body.append(new_seg)
        else:
            self.body.append(new_seg)
            self.body.pop(0)
        
    def draw(self, canvas):
        self.head.draw(canvas)
        for segment in self.body:
            segment.draw(canvas)
            
    def eat_food(self):
        '''Eats the food if the head finds it'''
        global food
        if food and self.head.get_pos() == food.get_pos():
            food = None
            return True
        else:
            return False
    
    def turn(self, direction):
        self.head.rotate(direction)
        vel = self.head.get_vel()
        if direction == 1:
            self.head.set_vel([-1*vel[1], vel[0]])
        else:
            self.head.set_vel([vel[1], -1*vel[0]])
    
    def control(self, key):
        if self.controls.has_key(key):
            self.turn(self.controls[key])
        
    def check_collision(self):
        if self.head.get_pos()[0] < 0 or WIDTH < self.head.get_pos()[0] \
          or self.head.get_pos()[1] < 0 or HEIGHT < self.head.get_pos()[1]:
            return True
        else:
            return False
    
def new_food():
    '''Make new food down'''
    return sprite.Sprite([4*UNIT, 4*UNIT],[0,0],0,[UNIT,UNIT],FOOD_COLOR)

def new_game():
    '''Create a new game'''
    global snake
    snake = Snake([WIDTH/2, HEIGHT/2])

def key_down(key):
    '''Key down Handler'''
    if snake:
        snake.control(key)
#     if snake and snake.control_state.has_key(key):
#         snake.control_state[key] = True

def key_up(key):
    '''Key up handler'''
#     if snake and snake.control_state.has_key(key):
#         snake.control_state[key] = False

def mouse_click(pos):
    '''Mouse click handler'''
    global game_over
    if game_over:
        game_over = False
        new_game()

def draw(canvas):
    '''Draw the board and pieces'''
    global food, move_count, game_over
    if food is None:
        food = new_food()
    
    food.draw(canvas)
    snake.draw(canvas)
    
    
    if not game_over:
        move_count += 1
        if move_count % MOVE_COUNT == 0:
            snake.update()
            if snake.check_collision():
                game_over = True
            
    else:
        canvas.draw_rect([0.1*WIDTH,0.5*HEIGHT-UNIT],[0.8*WIDTH,2*UNIT],0,'Grey','Grey')
        canvas.draw_text('GAME OVER',[WIDTH/2,HEIGHT/2],40,'White',align=('center','middle'))

def setup():
    '''Setup the frame and controls'''
    global frame
    
    frame = simplegui.Frame('Snake',(WIDTH,HEIGHT))
    
    frame.set_background_color(BACKGROUND_COLOR)
    frame.set_draw_handler(draw)
    
    frame.set_key_down_handler(key_down)
    frame.set_key_up_handler(key_up)
    frame.set_mouse_left_click_handler(mouse_click)
    
    

if __name__ == '__main__':
    setup()
    
    new_game()
    frame.start()