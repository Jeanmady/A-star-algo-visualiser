# visualiser.py
"""
Hexagonal Grid Visualisation Module
===================================

This module provides all the necessary functions to render a hexagonal grid
and the state of the pathfinding algorithms using Pygame. It is responsible
for converting grid coordinates to pixel coordinates and drawing the grid,
obstacles, paths, and the open/closed sets for both search algorithms.
"""

import pygame
import math

# --- Display and Grid Configuration ---
HEX_SIZE = 10       # The radius of a single hexagon in pixels.
SCREEN_WIDTH = 1280
SCREEN_HEIGHT = 720

# --- Colour Palette ---
COLOUR_BACKGROUND = (20, 30, 40)
COLOUR_GRID = (40, 60, 80)
COLOUR_OBSTACLE = (0, 0, 0)
COLOUR_PATH = (255, 215, 0)    
COLOUR_START = (0, 255, 127)     
COLOUR_END = (255, 69, 0)        
COLOUR_OUTLINE = (100, 120, 140)

# Colours for the standard (forward) A* search.
COLOUR_OPEN_SET = (50, 120, 180)   
COLOUR_CLOSED_SET = (30, 70, 110)  

# Colours for the backward search in the bidirectional algorithm.
COLOUR_OPEN_SET_BWD = (180, 50, 120)   
COLOUR_CLOSED_SET_BWD = (110, 30, 70)  

def axial_to_pixel(q, r):
    """Converts axial hex coordinates to pixel coordinates for rendering.

    This function translates (q, r) axial coordinates into the (x, y) pixel
    space required by Pygame, offsetting the result to center the grid
    on the screen.

    Args:
        q (int): The axial q-coordinate (columnish).
        r (int): The axial r-coordinate (rowish).

    Returns:
        tuple: A tuple containing the pixel coordinates (x, y) of the hex centre.
    """
    x = HEX_SIZE * (math.sqrt(3) * q + math.sqrt(3) / 2 * r)
    y = HEX_SIZE * (3. / 2. * r)
    return x + SCREEN_WIDTH / 2, y + SCREEN_HEIGHT / 2

def draw_hexagon(surface, colour, q, r):
    """Draws a single, outlined hexagon at a specified grid position.

    This function calculates the six vertices of a hexagon based on its axial
    coordinates, fills it with the given colour, and then draws its border.

    Args:
        surface (pygame.Surface): The Pygame surface to draw on.
        colour (tuple): The RGB colour tuple to fill the hexagon with.
        q (int): The axial q-coordinate of the hexagon.
        r (int): The axial r-coordinate of the hexagon.
    """
    center_x, center_y = axial_to_pixel(q, r)
    points = []

    # Calculate the six vertices of the hexagon around its centre point.
    for i in range(6):
        # The -30 degree offset orients the hexagons to be "flat topped".
        angle = math.pi / 180 * (60 * i - 30)
        x_i = center_x + HEX_SIZE * math.cos(angle)
        y_i = center_y + HEX_SIZE * math.sin(angle)
        points.append((x_i, y_i))
    
    # Draw the filled hexagon first.
    pygame.draw.polygon(surface, colour, points)
    
    # Draw the outline on top with a thickness of 2 pixels.
    pygame.draw.polygon(surface, COLOUR_OUTLINE, points, 2) 

def draw_hex_grid(surface, grid, start=None, end=None, path=None, 
                  open_set_fwd=None, closed_set_fwd=None,
                  open_set_bwd=None, closed_set_bwd=None):
    """Draws the entire hex grid, colouring each hex based on its state.

    This function iterates through every hex in the grid and determines its
    correct colour based on a priority order (e.g., a path node overrides a
    closed set node). It supports rendering the state of both standard and
    bidirectional searches.

    Args:
        surface (pygame.Surface): The Pygame surface to draw on.
        grid (dict): The dictionary representing the grid map.
        start (tuple, optional): The coordinates of the start node. Defaults to None.
        end (tuple, optional): The coordinates of the end node. Defaults to None.
        path (list, optional): A list of coordinates representing the final path. Defaults to None.
        open_set_fwd (list, optional): The open set for the forward search. Defaults to None.
        closed_set_fwd (set, optional): The closed set for the forward search. Defaults to None.
        open_set_bwd (list, optional): The open set for the backward search. Defaults to None.
        closed_set_bwd (set, optional): The closed set for the backward search. Defaults to None.
    """
    # Convert lists of Node objects to sets of positions for efficient lookups.
    path_pos = set(path) if path else set()
    open_pos_fwd = set(n.position for n in open_set_fwd) if open_set_fwd else set()
    closed_pos_fwd = set(closed_set_fwd) if closed_set_fwd else set()
    open_pos_bwd = set(n.position for n in open_set_bwd) if open_set_bwd else set()
    closed_pos_bwd = set(closed_set_bwd) if closed_set_bwd else set()

    for (q, r), cost in grid.items():
        # Determine the colour of the hex based on a rendering priority.
        # For example, the final path should be drawn on top of the search area.
        colour = COLOUR_GRID
        if cost == 1: 
            colour = COLOUR_OBSTACLE
        
        # Draw the search areas first.
        if (q, r) in closed_pos_fwd: 
            colour = COLOUR_CLOSED_SET
        if (q, r) in closed_pos_bwd: 
            colour = COLOUR_CLOSED_SET_BWD
        if (q, r) in open_pos_fwd: 
            colour = COLOUR_OPEN_SET
        if (q, r) in open_pos_bwd: 
            colour = COLOUR_OPEN_SET_BWD
        
        # Draw the most important elements last so they appear on top.
        if (q, r) in path_pos: 
            colour = COLOUR_PATH
        if (q, r) == start: 
            colour = COLOUR_START
        if (q, r) == end: 
            colour = COLOUR_END
            
        draw_hexagon(surface, colour, q, r)