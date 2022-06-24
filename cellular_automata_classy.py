import zlib
import numpy as np
import random
import matplotlib.pyplot as plt
from PIL import Image as im
import pygame, sys
from pygame import surfarray

class CA:
    def __init__(self, field):
        self.field = field # field = array
 
    def sumrule_eo(self, sum, x, y):
        return sum%2

    def sumrule(self, sum):
        if sum < 5:
            return sum%2
        else:
            return (sum+1)%2

    def sumrule_life(self, sum, x, y):
        if sum > 3 or sum <2:
            return 0
        elif sum == 3:
            return 1
        else:
            return self.field[x,y]

    def stoch_rule(self, sum, x, y):
        if sum == 0 or sum == 8:
            return 0
        elif sum < 4 and sum > 5:
            return sum%2
        else:
            return (x+y)%2

    def evolve(self):
        w, h = self.field.shape
        newfield = np.zeros((w,h), dtype='uint8')
        for idx, i in np.ndenumerate(self.field):
            x, y = idx  
            n_sum= 0
            for neighborhood_x in range(-1,2):
                for neighborhood_y in range(-1,2):
                    if neighborhood_x == 0 and neighborhood_y == 0:
                        continue
                    else:
                        n_sum += self.field[(x+neighborhood_x)%w][(y+neighborhood_y)%h]
            newfield[x][y] = self.sumrule(n_sum)
        self.field = newfield
        return newfield    

class RenderCellAuto:
    def __init__(self, cell, display_width, display_height, number_of_files, timescale, file_number=1000, file_name='CA_classic', save_loc='Z:/Animated_CA', mode=0, file_type='.png', render=True):
        self.cell = cell
        self.display_width = display_width
        self.display_height = display_height
        self.field_w = int(self.display_width/self.cell)
        self.field_h = int(self.display_height/self.cell)
        self.field = np.zeros((self.field_w, self.field_h), dtype='uint8')
        self.agent = CA(self.field)
        self.file_number = file_number
        self.number_of_files = number_of_files
        self.timescale = timescale
        self.save_loc = save_loc
        self.file_name = file_name
        self.file_type = file_type
        self.render = render
        self.seed(mode=mode)

    def seed(self, mode=0):
        if mode == 0:
            self.field[int(self.field_w/2),int(self.field_h/2)] = 1
        else:
            print('mode unknown. no change to field.')
            
    def run(self):
        pygame.init()
        screen = pygame.display.set_mode([self.field_w*self.cell, self.field_h*self.cell])
        
        while True:
            # print('inside while True')
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

            pygame.display.flip()

            for _ in range(self.timescale):
                # print('range in timescale loop')
                self.field = self.agent.evolve()

            if self.cell > 1:
                cell_field = self.field.repeat(self.cell, axis=0).repeat(self.cell, axis=1)
            else:
                cell_field = self.field
            show_field = np.dstack((cell_field*255, cell_field*77, cell_field*123))

            surfarray.blit_array(screen, show_field)

            # likely doesn't need to be a full-on class but it would be good to make this into a function that can be imported into future projects
            if self.render == True:
                filename = self.save_loc+'/'+self.file_name + '_' + str(self.file_number)+self.file_type
                S = np.rot90(show_field, k=1, axes=(0, 1))
                plt.imsave(filename, S)
                self.file_number +=1
                if self.file_number > self.file_number + self.number_of_files:
                    pygame.quit()
                    sys.exit()

if __name__ == "__main__":
    
    R = RenderCellAuto(cell=3, display_width=1452, display_height=927, number_of_files=900, timescale=1)
    print(R.__dict__)
    R.run()
