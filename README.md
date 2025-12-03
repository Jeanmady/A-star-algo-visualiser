# Hexagonal A* Pathfinding Visualiser

## Overview

This project is an interactive visualisation tool for the A* pathfinding algorithm, specifically implemented for a hexagonal grid. It provides a comparative analysis between the standard (unidirectional) A* search and an improved Bidirectional A* variant.

The application generates a large, complex, maze style environment to create a definitive test case, clearly demonstrating the performance advantages of the bidirectional approach in a complex search space. It serves as a practical demonstration of advanced algorithm design and analysis.

---

## Features

-   **Interactive Visualisation:** Watch the algorithms work, with clear colour coding for open sets, closed sets, obstacles, and the final path.
-   **Algorithm Comparison:** Instantly switch between the standard A* and the improved Bidirectional A* algorithms to compare their performance on the same map.
-   **Live Performance Metrics:** An on screen counter displays the total number of "Nodes Explored" in real time, providing immediate quantitative feedback on efficiency.
-   **Random Maze Generation:** Generate a new, complex maze with a single keypress to test the algorithms on different layouts.
-   **Hexagonal Grid Logic:** Implements pathfinding on a hexagonal grid using axial coordinates, a more natural and realistic model for uniform movement costs compared to a standard square grid.

---

## Requirements

-   Python 3
-   Pygame library

### Setup

1.  **Ensure Python 3 is installed.** You can download it from [python.org](https://www.python.org/).

2.  **Install the Pygame library.** Open your terminal or command prompt and run the following command:
    ```bash
    pip install pygame
    ```

---

## How to Run

1.  Clone or download the project repository to your local machine.
2.  Navigate to the project's root directory in your terminal.
3.  Run the main application file:
    ```bash
    python main_hex.py
    ```
    A Pygame window should open, displaying the grid and the UI controls.

---

## Controls

The application is controlled via keyboard inputs:

-   **`SPACE`**: Start or pause the step-by-step animation of the current algorithm.
-   **`1`**: Select the **Standard A\*** algorithm. The visualiser will reset.
-   **`2`**: Select the **Bidirectional A\*** algorithm. The visualiser will reset.
-   **`R`**: Reset the current search and generate a **new random maze**.