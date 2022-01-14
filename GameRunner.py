from Tetris import pygame
from Tetris import create_grid
from Tetris import get_shape
from Tetris import valid_space
from Tetris import rotate_shape
from Tetris import clear_rows
from Tetris import draw_window
from Tetris import draw_next_shape
from Tetris import check_lost
from Tetris import draw_text_middle

pygame.font.init()


s_width = 800
s_height = 700

def main():
    global grid

    locked_positions = {}  # (x,y):(255,0,0)
    grid = create_grid(locked_positions)
    change_piece = False
    run = True
    current_piece = get_shape()
    next_piece = get_shape()
    clock = pygame.time.Clock()
    fall_time = 0
    level_time = 0

    while run:
        level_time += clock.get_rawtime() #this function makes the blocks fall faster as time goes on as well as sets the default fall speed for the blocks
        if level_time/1000 > 5:
            level_time = 0
            if level_time > 0.12:
                level_time -=0.005
        fall_speed = 0.27
        
        grid = create_grid(locked_positions)
        fall_time += clock.get_rawtime()
        clock.tick()
    
        if fall_time/1000 >= fall_speed:
            fall_time = 0
            current_piece.y += 1
            if not (valid_space(current_piece, grid)) and current_piece.y > 0:
                current_piece.y -= 1
                change_piece = True

        for event in pygame.event.get(): #this is for when the user quits, then the program will shut down
            if event.type == pygame.QUIT:
                run = False
                pygame.display.quit()
                quit()

            if event.type == pygame.KEYDOWN: #these are the controls for the user when they input left right up or down
                if event.key == pygame.K_LEFT:
                    current_piece.x -= 1
                    if not valid_space(current_piece, grid):
                        current_piece.x += 1 #makes sure the blocks don't go out of bounds, the way this works is that if they  input left again
                                            #the x position of the block is -1, this will add 1 to the x position so that the block goes back to the play area

                elif event.key == pygame.K_RIGHT:
                    current_piece.x += 1
                    if not valid_space(current_piece, grid):
                        current_piece.x -= 1

                elif event.key == pygame.K_UP: #Up rotates the piece
                    current_piece.rotation = current_piece.rotation + 1 % len(current_piece.shape)
                    if not valid_space(current_piece, grid):
                        current_piece.rotation = current_piece.rotation - 1 % len(current_piece.shape)

                if event.key == pygame.K_DOWN: #down makes the piece fall faster, it has to be pressed multiple times and not held
                    current_piece.y += 1
                    if not valid_space(current_piece, grid):
                        current_piece.y -= 1

        shape_pos = rotate_shape(current_piece)

        for i in range(len(shape_pos)):
            x, y = shape_pos[i]
            if y > -1: 
                grid[y][x] = current_piece.color
        if change_piece:
            for pos in shape_pos:
                p = (pos[0], pos[1])
                locked_positions[p] = current_piece.color
            current_piece = next_piece
            next_piece = get_shape()
            change_piece = False
            clear_rows(grid, locked_positions)

        draw_window(win, grid)
        draw_next_shape(next_piece, win)
        pygame.display.update()

        if check_lost(locked_positions): #checks if the player loses (blocks reach the top of the play area)
            draw_text_middle(win, "YOU LOST!", 80, (255,255,255))
            pygame.display.update()
            pygame.time.delay(1500)
            run = False

win = pygame.display.set_mode((s_width, s_height))
pygame.display.set_caption('Tetris')
main()