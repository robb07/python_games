'''
Created on Jun 11, 2014

@author: Robb
'''

class Sprite(object):
    '''
    Sprite object for drawing and moving around the game canvas
    '''


    def __init__(self, pos, vel, rot, size, color='White', img=None, draw_method=None):
        '''
        Constructor
        '''
        self.pos = list(pos)
        self.vel = list(vel)
        self.rot = rot
        self.size = tuple(size)
        self.color = color
        self.img = img
        self.draw_method = draw_method
        
    def set_pos(self, pos):
        '''Sets the position of the sprite'''
        self.pos = list(pos)
        
    def get_pos(self):
        '''Gets the position of the sprite'''
        return self.pos
    
    def set_vel(self, vel):
        '''Sets the velocity of the sprite'''
        self.vel = list(vel)
        
    def get_vel(self):
        '''Gets the velocity of the sprite'''
        return self.vel
    
    def set_rot(self, rot):
        '''Sets the rotation of the sprite'''
        self.rot = rot
        
    def get_rot(self):
        '''Gets the rotation of the sprite'''
        return self.rot
    
    def rotate(self, direction):
        '''Rotate the sprite'''
        self.rot = (self.rot + direction) % 4
        
    def get_rot_mat(self):
        if self.rot == 0:
            rot_mat = [[1,0],[0,1]]
        elif self.rot == 1:
            rot_mat = [[0,1],[-1,0]]
        elif self.rot == 2:
            rot_mat = [[-1,0],[0,-1]]
        elif self.rot == 3:
            rot_mat = [[0,-1],[1,0]]
        return rot_mat
    
    def set_size(self, size):
        '''Sets the size of the sprite'''
        self.size = tuple(size)
        
    def get_size(self):
        '''Gets the size of the sprite'''
        return self.size
    
    def set_img(self, img):
        '''Sets the image of the sprite'''
        self.img = img
        
    def get_img(self):
        '''Gets the image of the sprite'''
        return self.img
    
    def update(self):
        self.pos[0] += self.vel[0]
        self.pos[1] += self.vel[1]
        
    def draw(self, canvas):
        if self.img:
            #place holder for drawing the sprite's image
            pass
        elif self.draw_method:
            self.draw_method(canvas)
        else:
            #default is to draw a rectangle
            canvas.draw_rect(self.pos, self.size, 0, self.color, self.color)
    
    
    
    