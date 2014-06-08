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
BUTTON_FONT_H = 20#changing this messes up the default fonts
SCORE_FONT_H = 40

BALL_RADIUS = 10
PAD_WIDTH = 8
PAD_HEIGHT = 80
HALF_PAD_WIDTH = PAD_WIDTH / 2
HALF_PAD_HEIGHT = PAD_HEIGHT / 2
LEFT = False
RIGHT = True
DT = 1.0/60
PADDLE_VEL = 600

# initialize global variables for structure only
ball_pos = [0, 0]
ball_vel = [0, 0]
paddle1_pos = 0
paddle2_pos = 0
paddle1_vel = 0
paddle2_vel = 0
score1 = 0
score2 = 0
game_paused = False
plyr1_human = True
plyr2_human = True
difficulty_mode = "Easy"
dt_ahead = 0
computer_paddle_factor = 1.1

mute_off = True

plyr1_up = False
plyr1_down = False
plyr2_up = False
plyr2_down = False

# helper functions
# ball functions
# initialize ball_pos and ball_vel for new bal in middle of table
# if direction is RIGHT, the ball's velocity is upper right, else upper left
def spawn_ball(direction):
    """ Spawns a ball with a random velocity in the given direction. """
    global ball_pos, ball_vel
    ball_pos = [WIDTH/2, HEIGHT/2]
    
    vertical_vel = random.randrange(60, 180)
    horizontal_vel = random.randrange(120, 240)
    if direction:
        ball_vel = [horizontal_vel,-vertical_vel]
    else:
        ball_vel = [-horizontal_vel,-vertical_vel]
    pass

def collide_top_and_bottom():
    """ Bounce the ball off the ceiling and floor. """
    if ball_pos[1] - BALL_RADIUS < 0 and ball_vel[1] < 0:
        #ceiling
        if mute_off: sound_plop.play()
        ball_vel[1] = -ball_vel[1]
    elif ball_pos[1] + BALL_RADIUS > HEIGHT and ball_vel[1] > 0:
        #floor
        if mute_off: sound_plop.play()
        ball_vel[1] = -ball_vel[1]
    pass

def collide_left_and_right():
    """ 
    Bounce off the paddles or spawn a new ball
    if the old one is in the gutter.
    Increment the score if the ball goes in the gutter.
    """
    global score1, score2
    if ball_pos[0] - BALL_RADIUS < PAD_WIDTH:
        #Left
        if ball_pos[1] >= paddle1_pos and ball_pos[1] <= paddle1_pos + PAD_HEIGHT:
            #paddle
            if mute_off: sound_beeep.play()
            ball_vel[0] = -1.1*ball_vel[0]
            ball_vel[1] = 1.1*ball_vel[1]
        else:
            #Gutter
            if mute_off: sound_peeeeeep.play()
            spawn_ball(RIGHT)
            score2 += 1
    elif ball_pos[0] + BALL_RADIUS > WIDTH - PAD_WIDTH:
        #Right
        if ball_pos[1] >= paddle2_pos and ball_pos[1] <= paddle2_pos + PAD_HEIGHT:
            #paddle
            if mute_off: sound_beeep.play()
            ball_vel[0] = -1.1*ball_vel[0]
            ball_vel[1] = 1.1*ball_vel[1]
        else:
            #Gutter
            if mute_off: sound_peeeeeep.play()
            spawn_ball(LEFT)
            score1 += 1
    pass

# paddle functions
def paddle_coords(h_pos,v_pos):
    """ Calculate the corner coordinates of a paddle. """
    pos = [[h_pos, v_pos],
           [h_pos + PAD_WIDTH, v_pos],
           [h_pos + PAD_WIDTH, v_pos + PAD_HEIGHT],
           [h_pos, v_pos + PAD_HEIGHT]]
    return pos

def keep_paddle_on_screen(pos):
    """ Check to see if the paddle's position is off the screen and keep it on """
    if pos < 0:
        pos = 0
    elif pos + PAD_HEIGHT > HEIGHT:
        pos = HEIGHT - PAD_HEIGHT
    return pos

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
    pass

def computer_move(paddle_pos, paddle_vel, ball_pos_est):
    """ Computes a new paddle velocity given the ball's position for a computer player. """
    if ball_pos_est[0] > random.randrange(WIDTH/4,3*WIDTH/4):
       return  paddle_vel
    
    dist = ball_pos_est[1] - (paddle_pos + HALF_PAD_HEIGHT)
    
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

def computer1_move():
    """ Controls paddle1 for the comuter. """ 
    global paddle1_vel
    ball_pos_est = [ball_pos[0] + dt_ahead*DT*ball_vel[0], ball_pos[1] + dt_ahead*DT*ball_vel[1]]
    if ball_vel[0] < 0:
        paddle1_vel = computer_move(paddle1_pos,paddle1_vel,ball_pos_est)
    else:
        paddle1_vel = 0
    pass

def computer2_move():
    """ Controls paddle2 for the computer. """
    global paddle2_vel
    ball_pos_est = [WIDTH - (ball_pos[0] + dt_ahead*DT*ball_vel[0]), ball_pos[1] + dt_ahead*DT*ball_vel[1]]
    if ball_vel[0] > 0:
        paddle2_vel = computer_move(paddle2_pos,paddle2_vel,ball_pos_est)
    else:
        paddle1_vel = 0
    pass

# define event handlers
def new_game():
    """ Starts a new game. Spawns a ball, resets paddles, resets score """
    global paddle1_pos, paddle2_pos, paddle1_vel, paddle2_vel 
    global plyr1_up, plyr1_down, plyr2_up, plyr2_down
    global score1, score2
    global game_paused
    
    if random.randrange(0,2) == 1:
        spawn_ball(RIGHT)
    else:
        spawn_ball(LEFT)
    
    paddle1_pos = HEIGHT/2 - HALF_PAD_HEIGHT
    paddle2_pos = HEIGHT/2 - HALF_PAD_HEIGHT
    paddle1_vel = 0
    paddle2_vel = 0
    
    plyr1_up = False
    plyr1_down = False
    plyr2_up = False
    plyr2_down = False
        
    score1 = 0
    score2 = 0
    
    game_paused = False
    pass

def draw(c):
    """ Draw the board, ball, paddles, and score. """
    global score1, score2, paddle1_pos, paddle2_pos, ball_pos, ball_vel, paddle1_vel, paddle2_vel
 
    # draw mid line and gutters
    c.draw_line([int(WIDTH / 2), 0],[int(WIDTH / 2), HEIGHT], 1, "White")
    c.draw_line([PAD_WIDTH, 0],[PAD_WIDTH, HEIGHT], 1, "White")
    c.draw_line([WIDTH - PAD_WIDTH, 0],[WIDTH - PAD_WIDTH, HEIGHT], 1, "White")
        
    # update ball
    collide_top_and_bottom()
    collide_left_and_right()
    
    if not game_paused:
        ball_pos[0] += DT * ball_vel[0]
        ball_pos[1] += DT * ball_vel[1]
    
    # draw ball
    c.draw_circle(ball_pos,BALL_RADIUS,1,"White","White")
    
    # update paddle's vertical position, keep paddle on the screen
    if plyr1_human:
        if plyr1_up:
            paddle1_vel = -PADDLE_VEL
        elif plyr1_down:
            paddle1_vel = PADDLE_VEL
        else:
            paddle1_vel = 0
    else:
        computer1_move()
    
    if plyr2_human:
        if plyr2_up:
            paddle2_vel = -PADDLE_VEL
        elif plyr2_down:
            paddle2_vel = PADDLE_VEL
        else:
            paddle2_vel = 0
    else:
        computer2_move()
    
    if not game_paused:
        paddle1_pos += DT * paddle1_vel
        paddle2_pos += DT * paddle2_vel
    
    paddle1_pos = keep_paddle_on_screen(paddle1_pos)
    paddle2_pos = keep_paddle_on_screen(paddle2_pos)
    
    # draw paddles
    c.draw_polygon(paddle_coords(0,paddle1_pos),1,"White","White")
    c.draw_polygon(paddle_coords(WIDTH-PAD_WIDTH,paddle2_pos),1,"White","White")
    
    # draw scores
    c.draw_text(str(score1),[WIDTH/4,50],SCORE_FONT_H,"White")
    c.draw_text(str(score2),[WIDTH*3/4,50],SCORE_FONT_H,"White")
    pass
        
def keydown(key):
    """ Record players commands to move the paddles. """
    global plyr1_up, plyr1_down, plyr2_up, plyr2_down
    if key == 'w':
        plyr1_up = True
    elif key == 's':
        plyr1_down = True
    elif key == 'up':
        plyr2_up = True
    elif key == 'down':
        plyr2_down = True
    pass
   
def keyup(key):
    """ Record players commands to stop the paddles. """
    global plyr1_up, plyr1_down, plyr2_up, plyr2_down
    if key == 'w':
        plyr1_up = False
    elif key == 's':
        plyr1_down = False
    elif key == 'up':
        plyr2_up = False
    elif key == 'down':
        plyr2_down = False
    pass

def plyr1_toggle():
    """ Switch between player 1 being controlled by human and computer """
    global paddle1_vel
    global plyr1_human
    if plyr1_button.get_text() == "Player 1: Human":
        plyr1_button.set_text("Player 1: Computer")
        plyr1_human = False
    else:
        plyr1_button.set_text("Player 1: Human")
        plyr1_human = True
        paddle1_vel = 0
    pass

def plyr2_toggle():
    """ Switch between player 2 being controlled by human and computer """
    global paddle2_vel
    global plyr2_human
    if plyr2_button.get_text() == "Player 2: Human":
        plyr2_button.set_text("Player 2: Computer")
        plyr2_human = False
    else:
        plyr2_button.set_text("Player 2: Human")
        plyr2_human = True
        paddle2_vel = 0
    pass

def pause_game():
    """ Pause or unpause the game. """
    global game_paused
    game_paused = not game_paused
    pass

def change_difficulty():
    """ Changes the computer's difficulty. """
    if difficulty_mode is "Easy":
        set_difficulty("Medium")
    elif difficulty_mode is "Medium":
        set_difficulty("Difficult")
    else:
        set_difficulty("Easy")
    difficulty_button.set_text("Computer: " + difficulty_mode)
    pass

def mute():
    """ Mute the sound effects. """
    global mute_off
    mute_off = not mute_off
    pass


if __name__ == '__main__':
    # create frame
    frame = simplegui.Frame("Pong", (WIDTH, HEIGHT), BUTTON_W)
    
    # register event handlers
    frame.set_draw_handler(draw)
    frame.set_key_down_handler(keydown)
    frame.set_key_up_handler(keyup)
    
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
    
    frame.set_font_sizes([BUTTON_FONT_H,SCORE_FONT_H])
    
    sound_beeep = simplegui.Sound('https://dl.dropboxusercontent.com/u/22969407/sounds_ping_pong_8bit/ping_pong_8bit_beeep.ogg')
    sound_peeeeeep = simplegui.Sound('https://dl.dropboxusercontent.com/u/22969407/sounds_ping_pong_8bit/ping_pong_8bit_peeeeeep.ogg')
    sound_plop = simplegui.Sound('https://dl.dropboxusercontent.com/u/22969407/sounds_ping_pong_8bit/ping_pong_8bit_plop.ogg')
    
    # start frame
    new_game()
    frame.start()
    
