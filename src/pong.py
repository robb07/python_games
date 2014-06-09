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
difficulty_mode = "Easy"
DT_AHEAD = 0
COMPUTER_PADDLE_FACTOR = 1.1
SPEEDUP_FACTOR = 1.1

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
        '''Changes the control state for a key'''
        if self.key_controls.has_key(key):
            self.control_states[self.key_controls[key]] = state
    
    def set_human(self,human):
        '''Sets the player to human or computer'''
        self.human = human
        self.paddle_vel = 0
        
    def get_vel(self):
        '''Gets the paddle velocity'''
        if self.control_states['up']:
            return -self.paddle_speed
        elif self.control_states['down']:
            return self.paddle_speed
        else:
            return 0
    
    def get_computer_move(self):
        '''Calculates the computer player's move'''
        if ball.pos[0] - self.pos[0] > 0 and ball.vel[0] < 0:
            ball_pos_est = [ball.pos[0] + DT_AHEAD*DT*ball.vel[0], ball.pos[1] + DT_AHEAD*DT*ball.vel[1]]
        elif ball.pos[0] - self.pos[0] < 0 and ball.vel[0] > 0:
            ball_pos_est = [WIDTH - (ball.pos[0] + DT_AHEAD*DT*ball.vel[0]), ball.pos[1] + DT_AHEAD*DT*ball.vel[1]]
        else:
            return 0
        
        if ball_pos_est[0] > random.randrange(WIDTH/4,3*WIDTH/4):
            return self.paddle_vel
        
        dist = ball_pos_est[1] - (self.pos[1] + HALF_PAD_HEIGHT)
        direction = 1 if dist > 0 else -1
        if math.fabs(dist) < COMPUTER_PADDLE_FACTOR * HALF_PAD_HEIGHT:
            return direction*self.paddle_speed if random.randrange(0,100) >= 90 else 0
        elif math.fabs(dist) < PAD_HEIGHT:
            return direction*self.paddle_speed if random.randrange(0,100) >= 40 else 0
        elif random.randrange(HALF_PAD_HEIGHT,HEIGHT) >= math.fabs(dist):
            return direction*self.paddle_speed
        else:
            return self.paddle_vel
        
    def update(self):
        '''Updates the paddle position'''
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
        '''Draws the paddle and the score'''
        # draw paddle
        canvas.draw_rect(self.pos,self.size,1,"White","white")
        # draw score
        canvas.draw_text(str(self.score),self.score_pos,SCORE_FONT_H,"White")
        
    def collide(self):
        '''
        Checks to see if ball collided with paddle
        Bounces the ball or spawn a ball and mark score
        '''
        ball_to_paddle = self.get_ball_to_paddle(ball.pos)
        if ((self.pos[0] + 0.5*self.size[0]) - 0.5*WIDTH) * ball.vel[0] >= 0: 
            if abs(ball_to_paddle[0])<ball.radius+0.5*self.size[0]:
                # ball is touching the gutter
                # ball is coming at the paddle
                if abs(ball_to_paddle[1]) <= 0.5*self.size[1]:
                    #bounce
                    ball.bounce(HORIZONTAL, SPEEDUP_FACTOR)
                else:
                    spawn_ball(self.pos[0] < 0.5*WIDTH)
                    mark_score(self)
            elif abs(ball.pos[0] - 0.5*WIDTH) >= 0.5*WIDTH:
                spawn_ball(self.pos[0] < 0.5*WIDTH)
                mark_score(self)
                
        #if ball.pos[0] < 0 or ball.pos[0] > WIDTH:
        #    spawn_ball(ball.pos[0] < 0.5*WIDTH)
    
    def get_ball_to_paddle(self, ball_pos):
        '''Distance from the ball to the paddle in (x,y)'''
        pad_center = (self.pos[0] + 0.5*self.size[0], self.pos[1] + 0.5*self.size[1])
        ball_to_paddle = (pad_center[0] - ball_pos[0], pad_center[1] - ball_pos[1])
        return ball_to_paddle
    
    def increment_score(self):
        '''Increment the score'''
        self.score += 1
            
            
    def __str__(self):
        '''Converts the paddle to a string'''
        return self.name + ': ' + str(self.key_controls)
        
class Ball(object):
    '''Creates the ball'''
    
    def __init__(self, pos, radius, vel):
        '''Initializes the ball'''
        self.pos = pos
        self.radius = radius
        self.vel = vel
        
    def update(self):
        '''Updates the ball's position'''
        if not game_paused:
            self.pos[0] += DT * self.vel[0]
            self.pos[1] += DT * self.vel[1]
    
    def draw(self, canvas):
        '''Draws the ball on the canvas'''
        canvas.draw_circle(self.pos,self.radius,1,"White","White")
    
    def bounce(self,horizontal,speedup=1):
        '''Bounces the ball'''
        if horizontal:
            self.vel[0] *= -speedup
            self.vel[1] *= speedup
        else:
            self.vel[0] *= speedup
            self.vel[1] *= -speedup
    
    def collide_top_and_bottom(self):
        """Bounces the ball off the ceiling and floor"""
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
    global difficulty_mode, DT_AHEAD, COMPUTER_PADDLE_FACTOR
    difficulty_mode = mode
    if difficulty_mode is "Medium":
        DT_AHEAD = 2
        COMPUTER_PADDLE_FACTOR = 1
    elif difficulty_mode is "Difficult":
        DT_AHEAD = 5
        COMPUTER_PADDLE_FACTOR = 0.75
    else:
        DT_AHEAD = 0
        COMPUTER_PADDLE_FACTOR = 1.1



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
        
    # update, draw, collide the ball
    ball.update()
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
    '''Setup the frame and buttons'''
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
    
