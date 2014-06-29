#!/usr/bin/env python
'''
Sprite class for drawing and moving simple objects around

Created on Jun 11, 2014

@author: Robb
'''

class Sprite(object):
    '''
    Sprite object for drawing and moving around the game canvas
    '''

    def __init__(self, name=None, pos=[0,0], vel=[0,0], rot=0, size=(10,10), color='White', line_color='Black', line_width=1, image=None, draw_method=None, update_method=None):
        '''
        Constructor
        '''
        self.name = name
        self.pos = pos
        self.vel = vel
        self.rot = rot
        self.size = tuple(size)
        self.color = color
        self.line_color = line_color
        self.line_width = line_width
        self.image = image
        self.draw_method = draw_method
        self.update_method = update_method
        
    def set_pos(self, pos):
        '''Sets the position of the sprite'''
        self._pos = tuple(pos)
    
    def get_pos(self):
        '''Gets the position of the sprite'''
        return self._pos
     
    pos = property(get_pos, set_pos)
    
    def set_vel(self, vel):
        '''Sets the velocity of the sprite'''
        self._vel = tuple(vel)
         
    def get_vel(self):
        '''Gets the velocity of the sprite'''
        return self._vel
    
    vel = property(get_vel,set_vel)
    
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
    
    rot_mat = property(get_rot_mat)
    
    def rotate_offset(self, offset):
        '''Rotates an offset vector around the center point by the sprite's rotation'''
        return [self.pos[0] + self.rot_mat[0][0]*offset[0]+self.rot_mat[0][1]*offset[1],
                self.pos[1] + self.rot_mat[1][0]*offset[0]+self.rot_mat[1][1]*offset[1]]
    
    def set_size(self, size):
        '''Sets the size of the sprite'''
        self._size = tuple(size)
         
    def get_size(self):
        '''Gets the size of the sprite'''
        return self._size
    
    size = property(get_size, set_size)
    
    def move(self, movement):
        '''Moves the sprite the movement amount'''
        self.pos = [self.pos[0]+movement[0], self.pos[1]+movement[1]]
        
    def update(self, world_size=None, default=False):
        '''Updates the sprite's position'''
        if self.update_method and not default:
            self.update_method(self, world_size)
        else:
            self.move(self.vel)
            
        
    def draw(self, canvas, default=False):
        '''Draws the sprite'''
        if self.image and not default:
            #place holder for drawing the sprite's image
            canvas.draw_image(self.image, 
                              [self.pos[0]-0.5*self.image.get_size()[0],
                               self.pos[1]-0.5*self.image.get_size()[1]],
                              self.rot*90)
        elif self.draw_method and not default:
            self.draw_method(self, canvas)
        else:
            #default is to draw a rectangle centered at pos
            canvas.draw_rect([self.pos[0]-0.5*self.size[0],
                              self.pos[1]-0.5*self.size[1]],
                              self.size, self.line_width, self.line_color, self.color)
    
    def contains(self, pos):
        '''Returns true if the position is contained in the sprite's rectangle'''
        return (-0.5*self.size[0] <= pos[0] - self.pos[0] < 0.5*self.size[0]) \
            and (-0.5*self.size[1] <= pos[1] - self.pos[1] < 0.5*self.size[1]) 
    
    def gap_between(self, other_sprite):
        '''Returns the x,y gap between the two sprites'''
        return [abs(p1-p2) - 0.5*(s1+s2) for p1, s1, p2, s2 in zip(self.pos, self.size, other_sprite.pos, other_sprite.size)]
    
    def overlaps(self, other_sprite):
        '''Returns true if the two sprites overlap'''
        return all([g < 0 for g in self.gap_between(other_sprite)])
            
    def __repr__(self):
        '''Returns the class of the object and its fields'''
        return 'Sprite(name={0!r}, pos={1!r}, vel={2!r}, rot={3!r}, size={4!r}, color={5!r}, line_color={6!r}, line_width={7!r}, image={8!r}, draw_method={9!r}, update_method={10!r})'.format(self.name, self.pos, self.vel, self.rot, self.size, self.color, self.line_color, self.line_width, self.image, self.draw_method, self.update_method)
    
def draw_circle(circle, canvas):
    '''draws a circle'''
    canvas.draw_circle(circle.pos,circle.size[0]/2,circle.line_width,circle.line_color,circle.color)

def update_bounce(the_sprite, world_size):
    '''Bounces off the edge of the world'''
    the_sprite.move(the_sprite.vel)
    the_sprite.vel = [abs(v) if (p-0.5*s < 0) else (-abs(v) if (p+0.5*s > w) else v) for p, v, s, w in zip(the_sprite.pos, the_sprite.vel, the_sprite.size, world_size)]

def update_toroid(the_sprite, world_size):
    '''Treats the world as a 2D toroid'''
    the_sprite.move(the_sprite.vel)
    the_sprite.pos = (the_sprite.pos[0] % world_size[0], the_sprite.pos[1] % world_size[1])

def update_stay_in_world(the_sprite, world_size):
    '''Keeps the sprite from moving out of the world'''
    stay_in_vel = [0 if (p+v-0.5*s < 0 or p+v+0.5*s > w) else v for p, v, s, w in zip(the_sprite.pos, the_sprite.vel, the_sprite.size, world_size)]
    the_sprite.vel = stay_in_vel
    the_sprite.move(the_sprite.vel)
    
    