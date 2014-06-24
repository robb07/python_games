#!/usr/bin/env python
'''
World class for drawing and updating the world of a game.

Created on Jun 23, 2014

@author: Robb
'''


class World(object):
    '''The world for a game'''
    
    def __init__(self, size=(400,400), background_color='Black', blocks=[]):
        '''Constructs a world'''
        self.size = size
        self.background_color = background_color
        self.blocks = blocks
        
    def draw(self, canvas):
        '''Draw the world and its items'''
        if canvas.background_color != self.background_color:
            canvas.set_background_color(self.background_color)
            canvas.draw_background()
            
        if len(self.blocks)>0:
            for block in self.blocks:
                block.draw(canvas)
                
                
    def update(self):
        '''Update the world'''
        pass
    
    def __repr__(self):
        '''Returns the world representation'''
        return 'World(size={0!r}, background_color={1!r}, blocks={2})'.format(self.size, self.background_color, self.blocks)