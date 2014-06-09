'''
The classic arcade game pong.

Created on Jun 8, 2014

@author: Robb
'''

import simplegui
import random
import math

# source for sound effects:
# http://opengameart.org/content/3-ping-pong-sounds-8-bit-style

# initialize global constants
WIDTH = 600
HEIGHT = 400
BUTTON_W = 200       
BUTTON_FONT_H = 16
SCORE_FONT_H = 40

BALL_RADIUS = 10
PAD_WIDTH = 8
PAD_HEIGHT = 80
HALF_PAD_WIDTH = PAD_WIDTH / 2
HALF_PAD_HEIGHT = PAD_HEIGHT / 2
LEFT = False
RIGHT = True
HORIZONTAL = True
VERTICAL = False
DT = 1.0/60
PADDLE_VEL = 600

# initialize global variables for structure only
game_paused = False
plyr1_human = True
plyr2_human = True
difficulty_mode = "Easy"
dt_ahead = 0
computer_paddle_factor = 1.1
speedup_factor = 1.1

mute_off = True


paddles = []

class Paddle(object):
    '''Creates a paddle'''
    
    def __init__(self,name,human,pos,size,score_pos,controls=['up','down'],paddle_speed=PADDLE_VEL):
        '''Initialize the paddle'''
        self.name = name
        self.pos = pos
        self.size = size
        self.key_controls = {controls[0]:'up',controls[1]:'down'}
        self.control_states = {'up':False,'down':False}
        self.paddle_speed = paddle_speed
        self.paddle_vel = 0
        self.score = 0
        self.score_pos = score_pos
        self.human = human
    
    def key_press(self, key, state):
        '''Change the control state for a key'''
        if self.key_controls.has_key(key):
            self.control_states[self.key_controls[key]] = state
    
    def set_human(self,human):
        self.human = human
        self.paddle_vel = 0
        
    def get_vel(self):
        '''Get the paddle velocity'''
        if self.control_states['up']:
            return -self.paddle_speed
        elif self.control_states['down']:
            return self.paddle_speed
        else:
            return 0
    
    def get_computer_move(self):
        '''Calculate the computer player's move'''
        if ball.pos[0] > self.pos[0]:
            #return computer1_move()
            ball_pos_est = [ball.pos[0] + dt_ahead*DT*ball.vel[0], ball.pos[1] + dt_ahead*DT*ball.vel[1]]
            
            if ball.vel[0] <0:
                return computer_move(self.pos,self.paddle_vel,ball_pos_est)
            else:
                return 0
        else:
            #return computer2_move()
            ball_pos_est = [WIDTH - (ball.pos[0] + dt_ahead*DT*ball.vel[0]), ball.pos[1] + dt_ahead*DT*ball.vel[1]]
            if ball.vel[0] > 0:
                return computer_move(self.pos,self.paddle_vel,ball_pos_est)
            else:
                return 0
        
        
    def update(self):
        '''Update the paddle position'''
        if not game_paused:
            if self.human:
                self.paddle_vel = self.get_vel()
            else:
                self.paddle_vel = self.get_computer_move()
            self.pos[1] += DT*self.paddle_vel
            
            #keep paddle on the table
            if self.pos[1] < 0:
                self.pos[1] = 0
            elif self.pos[1] + self.size[1] > HEIGHT:
                self.pos[1] = HEIGHT - self.size[1]
                
        
    def draw(self, canvas):
        '''Draw the paddle and the score'''
        # draw paddle
        canvas.draw_rect(self.pos,self.size,1,"White","white")
        # draw score
        canvas.draw_text(str(self.score),self.score_pos,SCORE_FONT_H,"White")
        
    def collide(self):
        '''
        Check to see if ball collided with paddle
        Bounce the ball or spawn a ball and mark score
        '''
        ball_to_paddle = self.get_ball_to_paddle(ball.pos)
        if ((self.pos[0] + 0.5*self.size[0]) - 0.5*WIDTH) * ball.vel[0] >= 0: 
            if abs(ball_to_paddle[0])<ball.radius+0.5*self.size[0]:
                # ball is touching the gutter
                # ball is coming at the paddle
                if abs(ball_to_paddle[1]) <= 0.5*self.size[1]:
                    #bounce
                    ball.bounce(HORIZONTAL, speedup_factor)
                else:
                    spawn_ball(self.pos[0] < 0.5*WIDTH)
                    mark_score(self)
            elif abs(ball.pos[0] - 0.5*WIDTH) >= 0.5*WIDTH:
                spawn_ball(self.pos[0] < 0.5*WIDTH)
                mark_score(self)
                
        #if ball.pos[0] < 0 or ball.pos[0] > WIDTH:
        #    spawn_ball(ball.pos[0] < 0.5*WIDTH)
    
    def get_ball_to_paddle(self, ball_pos):
        pad_center = (self.pos[0] + 0.5*self.size[0], self.pos[1] + 0.5*self.size[1])
        ball_to_paddle = (pad_center[0] - ball_pos[0], pad_center[1] - ball_pos[1])
        return ball_to_paddle
    
    def increment_score(self):
        '''Increment the score'''
        self.score += 1
            
            
    def __str__(self):
        return self.name + ': ' + str(self.key_controls)
        
class Ball(object):
    '''Creates the ball'''
    
    def __init__(self, pos, radius, vel):
        '''Initialize the ball'''
        self.pos = pos
        self.radius = radius
        self.vel = vel
        
    def update(self):
        '''Update the ball's position'''
        if not game_paused:
            self.pos[0] += DT * self.vel[0]
            self.pos[1] += DT * self.vel[1]
    
    def draw(self, canvas):
        '''Draw the ball on the canvas'''
        canvas.draw_circle(self.pos,self.radius,1,"White","White")
    
    def bounce(self,horizontal,speedup=1):
        '''Bounce the ball'''
        if horizontal:
            self.vel[0] *= -speedup
            self.vel[1] *= speedup
        else:
            self.vel[0] *= speedup
            self.vel[1] *= -speedup
    
    def collide_top_and_bottom(self):
        """ Bounce the ball off the ceiling and floor. """
        if self.pos[1] - self.radius < 0 and self.vel[1] < 0:
            #ceiling
            if mute_off: sound_plop.play()
            self.bounce(VERTICAL)
        elif self.pos[1] + self.radius > HEIGHT and self.vel[1] > 0:
            #floor
            if mute_off: sound_plop.play()
            self.bounce(VERTICAL)
            
            
    
# helper functions
# ball functions
# initialize ball_pos and ball_vel for new bal in middle of table
# if direction is RIGHT, the ball's velocity is upper right, else upper left
def spawn_ball(direction):
    """ Spawns a ball with a random velocity in the given direction. """
    #global ball_pos, ball_vel
    global ball
    ball_pos = [WIDTH/2, HEIGHT/2]
    
    vertical_vel = random.randrange(60, 180)
    horizontal_vel = random.randrange(120, 240)
    if direction:
        ball_vel = [horizontal_vel,-vertical_vel]
    else:
        ball_vel = [-horizontal_vel,-vertical_vel]
    
    ball = Ball(ball_pos, BALL_RADIUS, ball_vel)



def mark_score(scored_on_paddle):
    '''Marks the score'''
    [paddle.increment_score() for paddle in paddles if paddle != scored_on_paddle]

# computer player helper functions
def set_difficulty(mode):
    """ Sets the computer's difficulty mode. """
    global difficulty_mode, dt_ahead, computer_paddle_factor
    difficulty_mode = mode
    if difficulty_mode is "Medium":
        dt_ahead = 2
        computer_paddle_factor = 1
    elif difficulty_mode is "Difficult":
        dt_ahead = 5
        computer_paddle_factor = 0.75
    else:
        dt_ahead = 0
        computer_paddle_factor = 1.1

def computer_move(paddle_pos, paddle_vel, ball_pos_est):
    """ Computes a new paddle velocity given the ball's position for a computer player. """
    if ball_pos_est[0] > random.randrange(WIDTH/4,3*WIDTH/4):
        return paddle_vel
    
    dist = ball_pos_est[1] - (paddle_pos[1] + HALF_PAD_HEIGHT)
    
    if math.fabs(dist) < computer_paddle_factor * HALF_PAD_HEIGHT:
        if random.randrange(0,100) >= 90:
            if dist > 0:
                paddle_vel = PADDLE_VEL
            else:
                paddle_vel = -PADDLE_VEL
        else:
            paddle_vel = 0
    elif math.fabs(dist) < PAD_HEIGHT:
        if random.randrange(0,100) >= 40:
            if dist > 0:
                paddle_vel = PADDLE_VEL
            else:
                paddle_vel = -PADDLE_VEL
        else:
            paddle_vel = 0
    elif random.randrange(HALF_PAD_HEIGHT,HEIGHT) >= math.fabs(dist):
        if dist > 0:
            paddle_vel = PADDLE_VEL
        else:
            paddle_vel = -PADDLE_VEL
    #else:
    #    paddle_vel = 0
        
    return paddle_vel

# def computer1_move():
#     """ Controls paddle1 for the computer. """ 
#     #global paddle1_vel
#     paddle1_pos = paddles[0].pos
#     paddle1_vel = paddles[0].paddle_vel
#     ball_pos_est = [ball.pos[0] + dt_ahead*DT*ball.vel[0], ball.pos[1] + dt_ahead*DT*ball.vel[1]]
#     if ball.vel[0] < 0:
#         paddle1_vel = computer_move(paddle1_pos,paddle1_vel,ball_pos_est)
#     else:
#         paddle1_vel = 0
#     return paddle1_vel
# 
# def computer2_move():
#     """ Controls paddle2 for the computer. """
#     #global paddle2_vel
#     paddle2_pos = paddles[1].pos
#     paddle2_vel = paddles[1].paddle_vel
#     ball_pos_est = [WIDTH - (ball.pos[0] + dt_ahead*DT*ball.vel[0]), ball.pos[1] + dt_ahead*DT*ball.vel[1]]
#     if ball.vel[0] > 0:
#         paddle2_vel = computer_move(paddle2_pos,paddle2_vel,ball_pos_est)
#     else:
#         paddle2_vel = 0
#     return paddle2_vel

# define event handlers
def new_game():
    """ Starts a new game. Spawns a ball, resets paddles, resets score """
    global game_paused
    global paddles
    
    if random.randrange(0,2) == 1:
        spawn_ball(RIGHT)
    else:
        spawn_ball(LEFT)
    
    paddles = [Paddle('Player 1',(plyr1_button.get_text() == "Player 1: Human"),[0, HEIGHT/2 - HALF_PAD_HEIGHT],(PAD_WIDTH, PAD_HEIGHT),(WIDTH/4,50),['w','s']),
               Paddle('Player 2',(plyr2_button.get_text() == "Player 2: Human"),[WIDTH-PAD_WIDTH, HEIGHT/2 - HALF_PAD_HEIGHT],(PAD_WIDTH, PAD_HEIGHT),(WIDTH*3/4,50),['up','down'])]
    
        
    game_paused = False

def draw(c):
    """ Draw the board, ball, paddles, and score. """
    global ball_pos, ball_vel
    
    # draw mid line and gutters
    c.draw_line([int(WIDTH / 2), 0],[int(WIDTH / 2), HEIGHT], 1, "White")
    c.draw_line([PAD_WIDTH, 0],[PAD_WIDTH, HEIGHT], 1, "White")
    c.draw_line([WIDTH - PAD_WIDTH, 0],[WIDTH - PAD_WIDTH, HEIGHT], 1, "White")
        
    # update ball
    ball.update()
    
    # draw ball
    ball.draw(c)
    ball.collide_top_and_bottom()

    #update and draw paddles
    for paddle in paddles:
        paddle.collide()
        paddle.update()
        paddle.draw(c)
    
        
def keydown(key):
    """ Record players commands to move the paddles. """
    for paddle in paddles:
        paddle.key_press(key, True)
   
def keyup(key):
    """ Record players commands to stop the paddles. """
    for paddle in paddles:
        paddle.key_press(key, False)

def plyr1_toggle():
    """ Switch between player 1 being controlled by human and computer """
    if plyr1_button.get_text() == "Player 1: Human":
        plyr1_button.set_text("Player 1: Computer")
        paddles[0].set_human(False)
    else:
        plyr1_button.set_text("Player 1: Human")
        paddles[0].set_human(True)

def plyr2_toggle():
    """ Switch between player 2 being controlled by human and computer """
    if plyr2_button.get_text() == "Player 2: Human":
        plyr2_button.set_text("Player 2: Computer")
        paddles[1].set_human(False)
    else:
        plyr2_button.set_text("Player 2: Human")
        paddles[1].set_human(True)

def pause_game():
    """ Pause or unpause the game. """
    global game_paused
    game_paused = not game_paused

def change_difficulty():
    """ Changes the computer's difficulty. """
    if difficulty_mode is "Easy":
        set_difficulty("Medium")
    elif difficulty_mode is "Medium":
        set_difficulty("Difficult")
    else:
        set_difficulty("Easy")
    difficulty_button.set_text("Computer: " + difficulty_mode)

def mute():
    """ Mute the sound effects. """
    global mute_off
    mute_off = not mute_off

def setup():
    global frame, plyr1_button, plyr2_button, difficulty_button
    global sound_beeep, sound_peeeeeep, sound_plop
    # create frame
    frame = simplegui.Frame("Pong", (WIDTH, HEIGHT), BUTTON_W)
    
    # register event handlers
    frame.set_draw_handler(draw)
    frame.set_key_down_handler(keydown)
    frame.set_key_up_handler(keyup)
    
    frame.add_label(" ")
    frame.add_button("Restart",new_game, 0.9*BUTTON_W, BUTTON_FONT_H)
    frame.add_button("Pause",pause_game, 0.9*BUTTON_W, BUTTON_FONT_H)
    
    #frame.add_label(" ")
    frame.add_label("Player 1: w up, s down")
    frame.add_label("Player 2: up and down arrows")
    
    #frame.add_label(" ")
    plyr1_button = frame.add_button("Player 1: Human",plyr1_toggle, 0.9*BUTTON_W, BUTTON_FONT_H)
    plyr2_button = frame.add_button("Player 2: Human",plyr2_toggle, 0.9*BUTTON_W, BUTTON_FONT_H)
    
    #frame.add_label(" ")
    difficulty_button = frame.add_button("Computer: " + difficulty_mode,change_difficulty, 0.9*BUTTON_W, BUTTON_FONT_H)
    
    #frame.add_label(" ")
    frame.add_button("Mute",mute, 0.9*BUTTON_W, BUTTON_FONT_H)
    
    sound_beeep = simplegui.Sound('https://dl.dropboxusercontent.com/u/22969407/sounds_ping_pong_8bit/ping_pong_8bit_beeep.ogg')
    sound_peeeeeep = simplegui.Sound('https://dl.dropboxusercontent.com/u/22969407/sounds_ping_pong_8bit/ping_pong_8bit_peeeeeep.ogg')
    sound_plop = simplegui.Sound('https://dl.dropboxusercontent.com/u/22969407/sounds_ping_pong_8bit/ping_pong_8bit_plop.ogg')
    
if __name__ == '__main__':
    setup()
    
    # start frame
    new_game()
    frame.start()
    
