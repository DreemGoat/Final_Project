import pygame
import random

# Global Variables
s_width = 800
s_height = 700
play_width = 300  # meaning 300 // 10 = 30 width per block
play_height = 600  # meaning 600 // 20 = 20 height per block
block_size = 30

top_left_x = (s_width - play_width) // 2
top_left_y = s_height - play_height


# Shapes of the blocks that will fall

S = [['.....',
      '......',
      '..00..',
      '.00...',
      '.....'],
     ['.....',
      '..0..',
      '..00.',
      '...0.',
      '.....']]

Z = [['.....',
      '.....',
      '.00..',
      '..00.',
      '.....'],
     ['.....',
      '..0..',
      '.00..',
      '.0...',
      '.....']]

I = [['..0..',
      '..0..',
      '..0..',
      '..0..',
      '.....'],
     ['.....',
      '0000.',
      '.....',
      '.....',
      '.....']]

O = [['.....',
      '.....',
      '.00..',
      '.00..',
      '.....']]

J = [['.....',
      '.0...',
      '.000.',
      '.....',
      '.....'],
     ['.....',
      '..00.',
      '..0..',
      '..0..',
      '.....'],
     ['.....',
      '.....',
      '.000.',
      '...0.',
      '.....'],
     ['.....',
      '..0..',
      '..0..',
      '.00..',
      '.....']]

L = [['.....',
      '...0.',
      '.000.',
      '.....',
      '.....'],
     ['.....',
      '..0..',
      '..0..',
      '..00.',
      '.....'],
     ['.....',
      '.....',
      '.000.',
      '.0...',
      '.....'],
     ['.....',
      '.00..',
      '..0..',
      '..0..',
      '.....']]

T = [['.....',
      '..0..',
      '.000.',
      '.....',
      '.....'],
     ['.....',
      '..0..',
      '..00.',
      '..0..',
      '.....'],
     ['.....',
      '.....',
      '.000.',
      '..0..',
      '.....'],
     ['.....',
      '..0..',
      '.00..',
      '..0..',
      '.....']]

shapes = [S, Z, I, O, J, L, T]
shape_colors = [(255, 147, 0), (255, 0, 255), (255, 255, 0), (82, 0, 81), (255, 165, 0), (0, 255, 0), (0, 255, 255)]

class Piece(object): #class function that holds all the essential data for the game which will be used many times throughout the code
    columns = 10  # x
    rows = 20  # y
 
    def __init__(self, column, row, shape): 
        self.x = column
        self.y = row
        self.shape = shape
        self.color = shape_colors[shapes.index(shape)]
        self.rotation = 0  # number from 0-3

def create_grid(locked_positions={}):
    grid = [[(0,0,0) for x in range(10)] for x in range(20)] #the 10 by 20 grid in Tetris is done by creating a large list that has 20 sub-list with 10 colors
 
    for i in range(len(grid)): #this loop will create the entire grid for the Tetris game 
        for j in range(len(grid[i])): #this loop also checks if there is already a tetris block that has been locked in place and changes that grid's color
            if (j,i) in locked_positions:
                c = locked_positions[(j,i)]
                grid[i][j] = c
    return grid

def get_shape(): #this function will randomly generate what shapes that the blocks will take place in 
    global shapes, shape_colors
 
    return Piece(5, 0, random.choice(shapes))

def draw_window(surface, grid): #the title at the top of the game
    surface.fill((0,0,0))
    font = pygame.font.SysFont('arial', 55)
    label = font.render('TETRIS', 1, (255,255,255))
 
    surface.blit(label, (top_left_x + play_width / 2 - (label.get_width() / 2), 30))
 
    for i in range(len(grid)):
        for j in range(len(grid[i])):
            pygame.draw.rect(surface, grid[i][j], (top_left_x + j* 30, top_left_y + i * 30, 30, 30), 0)
 
    # draw grid and border
    draw_grid(surface, 20, 10)
    pygame.draw.rect(surface, (255, 0, 0), (top_left_x, top_left_y, play_width, play_height), 5)
    pygame.display.update()

def draw_grid(surface, row, col): #this function draws the grey gridlines that we see in the game
    sx = top_left_x
    sy = top_left_y
    for i in range(row):
        pygame.draw.line(surface, (128,128,128), (sx, sy+ i*30), (sx + play_width, sy + i * 30))  # horizontal lines
        for j in range(col):
            pygame.draw.line(surface, (128,128,128), (sx + j * 30, sy), (sx + j * 30, sy + play_height))  # vertical lines

def rotate_shape(shape): #this is the function that rotates the blocks when pressing the UP key
    position = []
    format = shape.shape[shape.rotation % len(shape.shape)]
 
    for i, line in enumerate(format):
        row = list(line)
        for j, column in enumerate(row):
            if column == '0':
                position.append((shape.x + j, shape.y + i))
 
    for i, pos in enumerate(position):
        position[i] = (pos[0] - 2, pos[1] - 4)
 
    return position

def valid_space(shape, grid): #the function that ensures the blocks don't fall out of the play area
    valid_positions = [[(j, i) for j in range(10) if grid[i][j] == (0,0,0)] for i in range(20)]
    valid_positions = [j for sub in valid_positions for j in sub]
    reformat = rotate_shape(shape)
 
    for pos in reformat: #this function will push the blocks back into place if it goes out of the boundaries of the game
        if pos not in valid_positions:
            if pos[1] > -1:
                return False
 
    return True

def check_lost(position): 
    for pos in position:
        x, y = pos
        if y < 1: #checks if the player loses
            return True
    return False

def draw_next_shape(shape, surface): #the function that draws the next shape
    font = pygame.font.SysFont('arial', 30)
    label = font.render('Next Shape', 1, (255,255,255)) 

    sx = top_left_x + play_width + 50
    sy = top_left_y + play_height/2 - 100
    format = shape.shape[shape.rotation % len(shape.shape)] #drawing showing the player what the next block will be

    for i, line in enumerate(format):
        row = list(line)
        for j, column in enumerate(row):
            if column == '0':
                pygame.draw.rect(surface, shape.color, (sx + j*30, sy + i*30, 30, 30), 0)

    surface.blit(label, (sx + 10, sy- 30))

def clear_rows(grid, locked):
    inc = 0
    for i in range(len(grid)-1,-1,-1):
        row = grid[i]
        if (0, 0, 0) not in row:
            inc += 1
            ind = i #adds positions to remove from locked positions
            for j in range(len(row)):
                try:
                    del locked[(j, i)] #deletes the row if it is filled with blocks
                except:
                    continue
    if inc > 0:
        for key in sorted(list(locked), key=lambda x: x[1])[::-1]:
            x, y = key
            if y < ind:
                newKey = (x, y + inc)
                locked[newKey] = locked.pop(key)

def draw_text_middle(surface, text, size, color): #the game over text if you lose the game
    font = pygame.font.SysFont("arial", size, bold=True)
    label = font.render(text, 1, color)

    surface.blit(label, (top_left_x + play_width /2 - (label.get_width()/2), top_left_y + play_height/2 - label.get_height()/2))