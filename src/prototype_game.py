#!/usr/bin/env python
'''
Creates a prototype game like simplegui from codeskulptor.

Created on Jun 7, 2014

@author: Robb
'''

import os
import pygame

#from pygame.locals import *

if not pygame.font: print('Warning, fonts disabled')
if not pygame.mixer: print('Warning, sound disabled')
 
# initializations
pygame.init()

# a bit similar to CodeSkulptor frame creation -- we'll call the window the canvas
canvas = pygame.display.set_mode((640, 480))
pygame.display.set_caption("My_Project")

fontObj3 = pygame.font.Font(pygame.font.match_font('timesnewroman'), 32)

gold_color = pygame.Color(255, 215, 0)
white_color = pygame.Color(255, 255, 255)

# call this function to start everything
# could be thought of as the implementation of the CodeSkulptor frame .start() method.
def run():
    # initialize loop until quit variable
    running = True
    
    # create our FPS timer clock
    clock = pygame.time.Clock()    

#---------------------------Frame is now Running-----------------------------------------
    
    # doing the infinite loop until quit -- the game is running
    while running:
        
        # event queue iteration
        for event in pygame.event.get():
            
            # window GUI ('x' the window)
            if event.type == pygame.QUIT:
                running = False

            # input - key and mouse event handlers
            elif event.type == pygame.MOUSEBUTTONDOWN:
                pass
                # just respond to left mouse clicks
                #if pygame.mouse.get_pressed()[0]:
                    #mc_handler(pygame.mouse.get_pos())
            elif event.type == pygame.KEYDOWN:
                pass
                #kd_handler(event.key)

            # timers
            #elif event.type == timer_example:
                #t_example()      
                
        # the call to the draw handler
        draw_handler(canvas)
        
        # FPS limit to 60 -- essentially, setting the draw handler timing
        # it micro pauses so while loop only runs 60 times a second max.
        clock.tick(60)
        
#-----------------------------Frame Stops------------------------------------------

    # quit game -- we're now allowed to hit the quit call
    pygame.quit ()

count = 0
draw_colour = white_color
def draw_handler(canvas):

    # clear canvas -- fill canvas with uniform colour, then draw everything below.
    # this removes everything previously drawn and refreshes 
    canvas.fill((0, 0, 0))
    

    # draw example
    global count
    count += 1
    
    text_draw = fontObj3.render("CodeSkulptor Port", True, draw_colour)
    text_draw2 = fontObj3.render("Tutorial", True, draw_colour)

    if count % 90 < 45:
        canvas.blit(text_draw, (190, 220))
    else:
        canvas.blit(text_draw2, (250, 220))

    # update the display
    pygame.display.update()
    
if __name__ == '__main__':
    run()