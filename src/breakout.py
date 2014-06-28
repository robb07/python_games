#!/usr/bin/env python
'''
Created on Jun 28, 2014

@author: Robb
'''

import simplegui
import sprite
import random
import math

#SCREEN_SHOT_FILE = None
SCREEN_SHOT_FILE = "E:/Documents/projects/python_programs/30 days/tetris/tetris_screen_shot"
AUTO_SCREEN_SHOT = False

BRICK_SIZE = (50,20)
GRID_WIDTH = 20
GRID_HEIGHT = 30
TOP_GAP = 3
NUM_ROWS = 15

WIDTH = GRID_WIDTH*BRICK_SIZE[0]
HEIGHT = GRID_HEIGHT*BRICK_SIZE[1]
BACKGROUND_COLOR = 'Black'
IMAGES_ON = False

BALL_SIZE = (0.5*BRICK_SIZE[0], 0.5*BRICK_SIZE[0])
BALL_RADIUS = 0.5*BALL_SIZE[0]
PADDLE_SIZE = (BRICK_SIZE[0]*3, 0.75*BRICK_SIZE[1])
PADDLE_SPEED = 8
ball_speed = 5

SPARE_BALLS = 5

game_over = False
game_paused = False

brick_rows = []
ball = None
paddle = None
die = None

score = 0
multiplier = 1
cnt = 0
COUNT_FULL = 20

image_infos = dict([(color,None) for color in simplegui.COLOR_PALETTE.keys() if color != BACKGROUND_COLOR])
images = dict([])

control_state = dict([('left',False),('right',False)])

def draw(canvas):
    '''Draws the board, bricks, paddle, and ball'''
    global ball, game_over, cnt
    if not game_paused and not game_over:
        cnt = (cnt + 1) % COUNT_FULL
        
        if die and ball and ball.overlaps(die):
            if len(spare_balls) > 0:
                spare_balls.pop()
                ball = new_ball()
            else:
                game_over = True
                ball = None
                
        if ball:
            keep_score(paddle_bounce(paddle, ball), bricks_bounce(brick_rows, ball))
            
            ball.update((WIDTH,HEIGHT))
        if paddle:
            if control_state['left']:
                paddle.vel = (-PADDLE_SPEED,0)
            elif control_state['right']:
                paddle.vel = (PADDLE_SPEED,0)
            else:
                paddle.vel = (0,0)
            
            paddle.update((WIDTH,HEIGHT))
    
    for brick_row in brick_rows:
        for brick in brick_row:
            brick.draw(canvas)
    
    if paddle:
        paddle.draw(canvas)
        
    if ball:
        ball.draw(canvas)
    
    canvas.draw_text(str(score),continuous_pos((GRID_WIDTH-1,TOP_GAP/2.)),20,'White',align=('right','middle'))
    
    for spare in spare_balls:
        spare.draw(canvas)
        
    if game_over:
        canvas.draw_rect([0.25*WIDTH,0.5*HEIGHT-40],[0.5*WIDTH,2*40],2,'Black','Gray')
        canvas.draw_text('GAME OVER',[WIDTH/2,HEIGHT/2],40,'White',align=('center','middle'))
        
    if AUTO_SCREEN_SHOT and cnt == 0 and not game_paused and not game_over:
        frame.screen_shot()
    

def new_game():
    '''Resets the board'''
    global brick_rows, paddle, ball, spare_balls, die, game_over
    game_over = False
    
    brick_rows = [[make_brick([col + (0.5 if row % 2 == 1 else 0),row],random_color()) for col in range(GRID_WIDTH+1)] for row in range(TOP_GAP,TOP_GAP+NUM_ROWS)]
    ball = new_ball()
    spare_balls = make_spare_balls((0,TOP_GAP/2.))
    paddle = new_paddle()
    die = sprite.Sprite(pos=(WIDTH/2,HEIGHT),size=(WIDTH,2))
    
    
def new_ball():
    '''Returns a new ball'''
    return sprite.Sprite(name='Ball',
                         pos=continuous_pos([GRID_WIDTH/2, GRID_HEIGHT - (GRID_HEIGHT - NUM_ROWS - TOP_GAP)/2]),
                         vel=random_vel(ball_speed,[-45,-135]),
                         size=BALL_SIZE,
                         color=simplegui.COLOR_PALETTE['White'],
                         image=None,
                         draw_method=sprite.draw_circle,
                         update_method=sprite.update_bounce)

def new_paddle():
    '''Makes a paddle'''
    return sprite.Sprite(name='Paddle',
                         pos=continuous_pos([GRID_WIDTH/2, GRID_HEIGHT - 2]),
                         size=PADDLE_SIZE,
                         color=simplegui.COLOR_PALETTE['White'],
                         image=None,
                         update_method=sprite.update_stay_in_world)

def make_spare_balls(grid_pos):
    '''Makes the spare balls'''
    cont_pos = continuous_pos(grid_pos)
    return [sprite.Sprite(name='SpareBall',
                         pos=(cont_pos[0]+(i+1)*BALL_SIZE[0],cont_pos[1]),
                         size=BALL_SIZE,
                         color=simplegui.COLOR_PALETTE['White'],
                         image=None,
                         draw_method=sprite.draw_circle) for i in range(SPARE_BALLS)]
    
def make_brick(grid_pos, color):
    '''Makes a brick'''
    return sprite.Sprite(name=color,
                         pos=continuous_pos(grid_pos),
                         size=BRICK_SIZE,
                         color=simplegui.COLOR_PALETTE[color],
                         image=images[color])

def continuous_pos(grid_pos):
    '''Translates grid coordinates to continuous position'''
    return [BRICK_SIZE[0]*grid_pos[0],BRICK_SIZE[1]*grid_pos[1]]

def random_color():
    '''Returns a random color'''
    return random.choice(image_infos.keys())
    
def random_vel(speed,angle_range=[0,360]):
    '''Returns a random velocity with a magnitude of speed'''
    ang = random.uniform(angle_range[0]*math.pi/180.,angle_range[1]*math.pi/180.)
    return [speed*math.cos(ang), speed*math.sin(ang)]

def paddle_bounce(paddle, ball):
    '''Bounces the ball off the paddle'''
    if paddle and ball.overlaps(paddle):
        ball.vel = (ball.vel[0]+0.1*paddle.vel[0], -abs(ball.vel[1]))
        return True
    return False
    
def bricks_bounce(brick_rows, ball):
    '''Bounces the ball of the bricks'''
    remove_brick = None
    for brick_row in brick_rows:
        for brick in brick_row:
            if ball.overlaps(brick):
                gap = ball.gap_between(brick)
                if gap[0] < gap[1]:
                    ball.vel = (ball.vel[0], -ball.vel[1])
                else:
                    ball.vel = (-ball.vel[0], ball.vel[1])
                remove_brick = brick
                break
        if remove_brick:
            brick_row.remove(remove_brick)
            return True
    return False

def keep_score(paddle_hit, brick_hit):
    '''Keeps track of the score'''
    global multiplier, score
    if paddle_hit:
        multiplier = 1
    if brick_hit:
        score += 10*multiplier
        multiplier += 1
        
def key_down(key):
    '''Handles the key down events'''
    if control_state.has_key(key):
        control_state[key] = True

def key_up(key):
    '''Handles the key up events'''
    if key == 'space':
        pause()
    elif key == 'return':
        new_game()
    elif control_state.has_key(key):
        control_state[key] = False
        
def pause():
    '''Pauses the game'''
    global game_paused
    game_paused = not game_paused
    
def setup():
    '''Setup the frame and event handlers'''
    global frame, images
    
    #build the frame
    frame = simplegui.Frame('Breakout',(WIDTH,HEIGHT),canvas_color=BACKGROUND_COLOR)
    frame.set_draw_handler(draw)
    frame.set_key_down_handler(key_down)
    frame.set_key_up_handler(key_up)
    
    #configure images
    if IMAGES_ON:
        images = dict([(key, simplegui.Image(image_info)) for key, image_info in image_infos.iteritems()])
    else:
        images = dict([(key, None) for key, image_info in image_infos.iteritems()])
        
    #setup control panel
    
    if SCREEN_SHOT_FILE:
        frame.set_screen_shot_file(SCREEN_SHOT_FILE)

if __name__ == '__main__':
    setup()
    
    new_game()
    frame.start()

