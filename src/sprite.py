'''
Sprite class for drawing and moving simple objects around

Created on Jun 11, 2014

@author: Robb
'''

class Sprite(object):
    '''
    Sprite object for drawing and moving around the game canvas
    '''

    def __init__(self, pos, vel, rot, size, color='White', line_color='Black', line_width=1, image=None, draw_method=None):
        '''
        Constructor
        '''
        self.pos = list(pos)
        self.vel = list(vel)
        self.rot = rot
        self.size = tuple(size)
        self.color = color
        self.line_color = line_color
        self.line_width = line_width
        self.image = image
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
    
    def update(self, world_size=None):
        '''Updates the sprite's position'''
        self.pos[0] += self.vel[0]
        self.pos[1] += self.vel[1]
        if world_size:
            self.pos[0] %= world_size[0]
            self.pos[1] %= world_size[1]
        
    def draw(self, canvas, default=False):
        '''Draws the sprite'''
        if self.image and not default:
            #place holder for drawing the sprite's image
            canvas.draw_image(self.image, [self.pos[0]-0.5*self.image.get_size()[0],self.pos[1]-0.5*self.image.get_size()[1]], self.rot*90)
        elif self.draw_method and not default:
            self.draw_method(self, canvas)
        else:
            #default is to draw a rectangle centered at pos
            canvas.draw_rect([self.pos[0]-0.5*self.size[0],self.pos[1]-0.5*self.size[1]], self.size, self.line_width, self.line_color, self.color)
    
    
    
    