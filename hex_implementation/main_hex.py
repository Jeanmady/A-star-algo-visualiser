# main_hex.py
"""
Hexagonal A* Pathfinding Visualiser
===================================

This script runs the main visualisation loop for the hexagonal A* pathfinding
demonstration. It integrates with the visualiser and a_star_hex modules
to render a hex grid, perform the pathfinding step by step or instantly,
and provide user interaction through keyboard input.
"""

import pygame
import visualiser  # Handles grid rendering and visualisation
from a_star_hex import a_star_hex_search, a_star_hex_search_step


def create_grid(size):
    """
    Create a hexagonal grid with basic obstacle layout.

    This helper function generates a hex grid using axial coordinates,
    initialising all cells as walkable (0). A simple wall of obstacles
    is then added to demonstrate pathfinding behavior.

    :param size: The radius (in hexes) of the grid to generate.
    :return: A dictionary mapping coordinate tuples (q, r) to cell states.
             A value of 0 indicates a free cell, while 1 indicates an obstacle.
    """
    grid = {}
    for q in range(-size, size + 1):
        for r in range(-size, size + 1):
            # Skip cells outside the hexagonal boundary
            if abs(q + r) > size:
                continue
            grid[(q, r)] = 0

    # Add a vertical wall of obstacles
    for r in range(-5, 6):
        grid[(3, r)] = 1

    # Add a few additional obstacles for variation
    grid[(4, -5)] = 1
    grid[(2, 5)] = 1

    return grid


def main():
    """
    Launch the Pygame hexagonal A* pathfinding visualizer.

    This function initializes the display, handles the main game loop,
    processes user input, and renders the grid each frame. It allows the
    user to run the A* search algorithm step-by-step or instantly.

    **Controls**
      - **SPACE** : Start or pause step by step animation.
      - **ENTER** : Solve the path instantly.
      - **R**     : Reset the visualization.

    :return: This function does not return a value.
    """

    # Initialize Pygame and display
    pygame.init()
    screen = pygame.display.set_mode((visualiser.SCREEN_WIDTH, visualiser.SCREEN_HEIGHT))
    pygame.display.set_caption("Hexagonal A* Pathfinding Visualizer")
    clock = pygame.time.Clock()
    font = pygame.font.SysFont("Arial", 24)

    # --- Simulation state variables ---
    grid = create_grid(15)
    start = (-5, 0)
    end = (8, -2)

    path = None
    open_set = None
    closed_set = None

    # Initialize the A* step generator
    search_generator = a_star_hex_search_step(grid, start, end)
    animating = False

    # --- Main event loop ---
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            # Handle keyboard input
            if event.type == pygame.KEYDOWN:
                # SPACE toggles animation on/off
                if event.key == pygame.K_SPACE:
                    animating = not animating

                # ENTER solves the path instantly
                elif event.key == pygame.K_RETURN:
                    path = a_star_hex_search(grid, start, end)
                    animating = False

                # R resets the visualization
                elif event.key == pygame.K_r:
                    path, open_set, closed_set = None, None, None
                    search_generator = a_star_hex_search_step(grid, start, end)
                    animating = False

        # Step the pathfinding algorithm frame by frame
        if animating:
            try:
                open_set, closed_set = next(search_generator)
            except StopIteration as e:
                # Retrieve the final path from the generator
                path = e.value
                animating = False

        # --- Rendering ---
        screen.fill(visualiser.COLOUR_BACKGROUND)
        visualiser.draw_hex_grid(screen, grid, start, end, path, open_set, closed_set)

        # Draw on controls
        text = font.render("SPACE: Animate | ENTER: Solve | R: Reset", True, (255, 255, 255))
        screen.blit(text, (10, 10))

        # Update display
        pygame.display.flip()
        clock.tick(30)  # Limit frame rate (affects animation speed)

    # Clean up when the window is closed
    pygame.quit()


if __name__ == '__main__':
    main()