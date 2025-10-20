# visualiser.py
"""
Hex Grid Visualisation Module
=============================

Provides functions to render a hexagonal grid using Pygame.
This module supports drawing individual hexagons and entire grids,
and can visually represent start/end nodes, paths, and open/closed sets
for A*
"""

import pygame
import math

# --- Configuration ---
HEX_SIZE = 20  # Size of a hexagon
SCREEN_WIDTH = 1280
SCREEN_HEIGHT = 720

# --- Colours ---
COLOUR_BACKGROUND = (20, 30, 40)
COLOUR_GRID = (40, 60, 80)
COLOUR_OBSTACLE = (0,0,0)#(80, 100, 120)
COLOUR_PATH = (255, 215, 0) 
COLOUR_START = (0, 255, 127) 
COLOUR_END = (255, 69, 0) 
COLOUR_OUTLINE = (100, 120, 140)
COLOUR_OPEN_SET = (50, 120, 180)  
COLOUR_CLOSED_SET = (30, 70, 110) 

def axial_to_pixel(q, r):
    """
    Convert axial hex coordinates to pixel coordinates.

    This function converts axial hex coordinates (q, r) into pixel
    coordinates suitable for rendering on a centered Pygame surface.

    :param q: Axial q-coordinate (column index).
    :param r: Axial r-coordinate (row index).
    :return: A tuple containing the pixel coordinates (x, y) of the hex center.
    """

    x = HEX_SIZE * (math.sqrt(3) * q + math.sqrt(3) / 2 * r)
    y = HEX_SIZE * (3. / 2. * r)

    # Offset to center the grid on the screen
    return x + SCREEN_WIDTH / 2, y + SCREEN_HEIGHT / 2

def draw_hexagon(surface, colour, q, r):
    """
    Draw a single hexagon at the specified grid position.

    Calculates the hexagon's six vertex positions, fills it with the
    specified colour, and outlines it with a border.

    :param surface: The Pygame surface to draw on.
    :param colour: RGB colour used to fill the hexagon.
    :param q: Axial q-coordinate of the hexagon (column).
    :param r: Axial r-coordinate of the hexagon (row).
    :return: This function does not return a value.
    """

    center_x, center_y = axial_to_pixel(q, r)
    points = []

    # Compute the six vertices of the hexagon
    for i in range(6):
        angle = math.pi / 180 * (60 * i - 30)
        x_i = center_x + HEX_SIZE * math.cos(angle)
        y_i = center_y + HEX_SIZE * math.sin(angle)
        points.append((x_i, y_i))
    
    # Draw the filled hexagon first
    pygame.draw.polygon(surface, colour, points)
    
    # Draw outline
    pygame.draw.polygon(surface, COLOUR_OUTLINE, points, 2) 

def draw_hex_grid(surface, grid, start=None, end=None, path=None, open_set=None, closed_set=None):
    """
    Draw the entire hex grid, colour coding each cell based on its state.

    This function iterates through the hex grid and assigns a colour
    to each cell depending on its type: such as start, end, path,
    open/closed set, or obstacle. It visually represents the progress
    of pathfinding algorithms.

    :param surface: The Pygame surface to render the grid on.
    :param grid: Dictionary mapping coordinates (q, r) to cell costs or states.
    :param start: Coordinates of the start node.
    :param end: Coordinates of the goal node.
    :param path: List of coordinates representing the final path.
    :param open_set: List of nodes currently in the open set.
    :param closed_set: List of coordinates for nodes already explored.
    :return: This function does not return a value.
    """

    # Create sets of positions for fast lookups
    path_positions = set(path) if path else set()
    open_positions = set(node.position for node in open_set) if open_set else set()
    closed_positions = set(closed_set) if closed_set else set()

    # Iterate through each grid cell and determine colour
    for (q, r), cost in grid.items():
        if (q, r) == start:
            colour = COLOUR_START
        elif (q, r) == end:
            colour = COLOUR_END
        elif (q, r) in path_positions:
            colour = COLOUR_PATH
        elif (q, r) in open_positions:
            colour = COLOUR_OPEN_SET
        elif (q, r) in closed_positions:
            colour = COLOUR_CLOSED_SET
        elif cost == 1:
            colour = COLOUR_OBSTACLE
        else:
            colour = COLOUR_GRID
            
        draw_hexagon(surface, colour, q, r)