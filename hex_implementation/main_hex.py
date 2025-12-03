# main_hex.py
"""
Hexagonal A* Pathfinding Visualiser
===================================

This script serves as the main entry point for the pathfinding visualiser.
It handles Pygame initialisation, event processing (keyboard inputs),
and the main application loop. It integrates the algorithm logic from
`a_star_hex.py` and the rendering logic from `visualiser.py` to create an
interactive demonstration.

The visualiser is configured to use a large, complex, maze style grid,
which provides a test case for comparing the performance
of Standard A* versus the improved Bidirectional A* search.
"""

import pygame
import visualiser
import random
from a_star_hex import a_star_hex_search_step, bidirectional_a_star_hex_search_step

def create_complex_grid(size, density=0.3):
    """Creates a grid with randomly scattered obstacles.

    This environment serves as an ideal test case for bidirectional
    search, as it creates a complex search space that forces the standard A*
    algorithm to explore a massive number of nodes.

    Args:
        size (int): The radius of the hexagonal grid to generate.
        density (float, optional): The probability (0.0 to 1.0) that any given
                                   hex will be an obstacle. Defaults to 0.3.

    Returns:
        dict: A dictionary mapping (q, r) coordinate tuples to cell states (0=walkable, 1=obstacle).
    """
    grid = {}
    for q in range(-size, size + 1):
        for r in range(-size, size + 1):
            if abs(q + r) > size: 
                continue
            if random.random() < density:
                grid[(q, r)] = 1  # Obstacle
            else:
                grid[(q, r)] = 0  # Walkable
            
    return grid


def main():
    """Initialises Pygame, sets up the application state, and runs the main loop."""
    pygame.init()
    screen = pygame.display.set_mode((visualiser.SCREEN_WIDTH, visualiser.SCREEN_HEIGHT))
    pygame.display.set_caption("Hexagonal A* Pathfinding Visualizer")
    clock = pygame.time.Clock()
    font = pygame.font.SysFont("Arial", 24)
    font_large = pygame.font.SysFont("Arial", 32, bold=True)

    # --- Application State Variables ---
    grid_size = 30
    grid = create_complex_grid(grid_size, density=0.35)
    
    start = (-grid_size + 2, 0)
    end = (grid_size - 2, 0)

    # Ensure start and end points are always walkable, even in a dense maze.
    grid[start] = 0
    grid[end] = 0
    
    # Variables to hold the current state of the search for visualisation.
    path, open_fwd, closed_fwd, open_bwd, closed_bwd = None, None, None, None, None
    search_generator = None
    animating = False
    search_mode = 'A_STAR'
    explored_count = 0

    def reset_search():
        """Resets all search related state variables and creates a new search generator."""
        nonlocal path, open_fwd, closed_fwd, open_bwd, closed_bwd, search_generator, animating, explored_count
        path, open_fwd, closed_fwd, open_bwd, closed_bwd = None, None, None, None, None
        animating = False
        explored_count = 0
        if search_mode == 'A_STAR':
            search_generator = a_star_hex_search_step(grid, start, end)
        else:
            search_generator = bidirectional_a_star_hex_search_step(grid, start, end)

    reset_search()

    # --- Main Application Loop ---
    running = True
    while running:
        # --- Event Handling ---
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    animating = not animating
                if event.key == pygame.K_r:
                    # 'R' generates a new random maze and resets the search.
                    grid = create_complex_grid(grid_size, density=0.35)
                    grid[start] = 0; grid[end] = 0
                    reset_search()
                if event.key == pygame.K_1:
                    search_mode = 'A_STAR'
                    reset_search()
                if event.key == pygame.K_2:
                    search_mode = 'BIDIRECTIONAL'
                    reset_search()

        # --- Algorithm Step ---
        if animating:
            try:
                # Get the next state from the current search generator.
                result = next(search_generator)
                if search_mode == 'A_STAR':
                    open_fwd, closed_fwd, explored_count = result
                    open_bwd, closed_bwd = None, None
                else:
                    open_fwd, closed_fwd, open_bwd, closed_bwd, explored_count = result
            except StopIteration as e:
                # The generator is exhausted, meaning the search is complete.
                path = e.value
                animating = False

        # --- Drawing ---
        screen.fill(visualiser.COLOUR_BACKGROUND)
        
        # Delegate all grid drawing to the visualiser module.
        visualiser.draw_hex_grid(screen, grid, start, end, path, 
                                open_fwd, closed_fwd, open_bwd, closed_bwd)
        
        # Render and draw UI text elements.
        mode_text = f"Mode: {'Standard A*' if search_mode == 'A_STAR' else 'Bidirectional A*'}"
        controls_text = "1: Standard A* | 2: Bidirectional A* | R: New Maze | SPACE: Animate"
        text1 = font.render(mode_text, True, (255, 255, 255))
        text2 = font.render(controls_text, True, (255, 255, 255))
        screen.blit(text1, (10, 10))
        screen.blit(text2, (10, 40))

        # Render and draw the live counter for explored nodes.
        count_text_label = font.render("Nodes Explored:", True, (200, 200, 200))
        count_text_value = font_large.render(str(explored_count), True, (255, 255, 255))
        screen.blit(count_text_label, (10, 80))
        screen.blit(count_text_value, (10, 110))

        # Update the full display surface to the screen.
        pygame.display.flip()
        
        # Limit the frame rate.
        clock.tick(120)

    pygame.quit()

if __name__ == '__main__':
    main()