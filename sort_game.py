from typing import List
import pygame
import random

from pygame.constants import KEYDOWN
from pygame.font import SysFont

from sorts import insertion_sort_iteration, bubble_sort_iteration, merge_sort_iteration

class DrawInformation:

    # Constants
    BLACK = 0,0,0
    WHITE = 255,255,255
    GREEN = 0,255,0
    RED = 255,0,0
    GREY = 128,128,128,
    BACKGROUND_COLOR = WHITE

    GRADIENTS = [
        (160,160,160),
        (192,192,192),
        (128,128,128)
    ]

    # Display Variables
    SIDE_PAD = 100 # 50 px left and 50 px right
    TOP_PAD = 150

    def __init__(self, width, height, lst, tick_speed) -> None:
        self.width = width
        self.height = height
        self.window = pygame.display.set_mode((width,height))
        pygame.display.set_caption("Sorting Algorithm Visualizer")
        self.set_list(lst)

        # Intialize Fonts
        pygame.font.init()
        self.sysfont = pygame.font.SysFont('Comic Sans MS',18)
        self.largefont = pygame.font.SysFont('Comic Sans MS',30)

        # Set Tick Speed
        self.set_tick_speed(tick_speed)

    def set_list(self,lst) -> None:
        self.lst = lst
        self.min_val = min(lst)
        self.max_val = max(lst)

        self.block_width = round((self.width - self.SIDE_PAD) / len(lst))
        self.block_height = round((self.height - 2 * self.TOP_PAD) / (self.max_val - self.min_val))
        self.start_x = self.SIDE_PAD // 2

    def set_tick_speed(self, tick_speed):
        self.tick_speed = tick_speed

def generate_start_list(n : int, min_val : int, max_val : int) -> List:
    lst = []
    for _ in range(n):
        val = random.randint(min_val,max_val)
        lst.append(val)
    
    return lst

def center_x(draw_info: DrawInformation, render: pygame.Surface) -> int:
    text_width = render.get_width()
    return (draw_info.width - text_width) // 2

# Main Draw Method: Draws everything
def draw(draw_info : DrawInformation) -> None:
    draw_info.window.fill(draw_info.BACKGROUND_COLOR)
    draw_text(draw_info)
    draw_list(draw_info)
    pygame.display.update()

def draw_list(draw_info : DrawInformation) -> None:
    lst = draw_info.lst

    for i, val in enumerate(lst):
        # Determine starting locations to draw to
        x = draw_info.start_x + i * draw_info.block_width
        y = draw_info.height - (val - draw_info.min_val) * draw_info.block_height
        
        color = draw_info.GRADIENTS[i % 3]

        # TODO: Update Calculations to be more precise 
        pygame.draw.rect(draw_info.window, color, (x,y,draw_info.block_width, draw_info.height))

def draw_text(draw_info: DrawInformation) -> None:
    # Define Fonts
    sys_font = draw_info.sysfont
    large_font = draw_info.largefont

    # Title
    title_surface = large_font.render("Sort Simulator", True, draw_info.BLACK)
    draw_info.window.blit(title_surface,(center_x(draw_info,title_surface),10))

    # Speed
    speed_surface = sys_font.render("Speed: {}".format(draw_info.tick_speed), True, draw_info.BLACK)
    draw_info.window.blit(speed_surface, (center_x(draw_info,speed_surface),35))

    # Sorting 
    sorting_surface = sys_font.render("B - Bubble Sort | I - Insertion Sort | M - Merge Sort", True, draw_info.BLACK)
    draw_info.window.blit(sorting_surface,(center_x(draw_info,sorting_surface),55))

    # Instructions
    instruction_surface = sys_font.render("R - Reset | SPACE - Start Sorting | A - Ascending | D - Descending", True, draw_info.BLACK)
    draw_info.window.blit(instruction_surface,(center_x(draw_info,instruction_surface),75))


def main():

    # Game Parameters
    pygame.init()
    run = True
    clock = pygame.time.Clock()
    tick_speed = 60 # Modify to change max update speed
    tick_min = 5
    tick_max = 300
    tick = 5

    # List Creation Parameters
    n = 100
    min_val = 0
    max_val = 100
    lst = generate_start_list(n,min_val,max_val)
    draw_info = DrawInformation(800,600,lst, tick_speed)


    # Sorting and Iteration Variables
    sorting = False
    sorting_iteration_function = bubble_sort_iteration
    sorting_iterator = None


    # Game Main Loop
    while run:

        clock.tick(tick_speed)

        if sorting:
            try:
                next(sorting_iterator)
                draw(draw_info)

            except StopIteration:
                sorting = False

        draw(draw_info)

        # Handles all in game events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            if event.type != pygame.KEYDOWN:
                continue
            if event.key == pygame.K_r:
                lst = generate_start_list(n,min_val,max_val)
                draw_info.set_list(lst)
            # Bubble Sort
            elif event.key == pygame.K_b:
                sorting_iteration_function = bubble_sort_iteration
            # Merge Sort
            elif event.key == pygame.K_m:
                sorting_iteration_function = merge_sort_iteration
            # Insertion Sort
            elif event.key == pygame.K_i:
                sorting_iteration_function = insertion_sort_iteration
            
            # Start Sorts
            elif event.key == pygame.K_SPACE:
                if sorting == False:
                    sorting_iterator = sorting_iteration_function(lst)
                sorting = not sorting

            # Speed Control of the Sort
            elif event.key == pygame.K_LEFT:
                if tick_speed > tick_min:
                    tick_speed -= tick
                    draw_info.set_tick_speed(tick_speed)
            elif event.key == pygame.K_RIGHT:
                if tick_speed < tick_max:
                    tick_speed += tick
                    draw_info.set_tick_speed(tick_speed)

    # Exit game once clicked out
    pygame.quit()

if __name__ == "__main__":
    main()

