# a_star_hex.py
"""
A* and Bidirectional A* Pathfinding for Hexagonal Grids
========================================================

This module provides implementations of the A* pathfinding algorithm and an
improved Bidirectional A* variant, both specifically adapted for hexagonal
grids using axial coordinates.

The module includes:
- A `Node` class to represent individual grid cells for the search.
- A `hex_distance` function for an admissible heuristic.
- Generator versions of each search algorithm for visualisation.

"""

import heapq


class Node:
    """Represents a single node in the search algorithm's grid.

    Each node stores its position, parent, and scoring information required
    to determine the optimal path.

    Attributes:
        parent (Node or None): The parent node from which this node was reached.
        position (tuple): The axial coordinates (q, r) of this node on the grid.
        g (int): The movement cost from the start node to this node.
        h (int): The heuristic estimate of the cost from this node to the goal.
        f (int): The total estimated cost (f = g + h).
    """

    def __init__(self, parent=None, position=None):
        """Initialises a new Node object.

        Args:
            parent (Node, optional): The parent node that led to this node. Defaults to None.
            position (tuple, optional): The (q, r) axial coordinates of the node. Defaults to None.
        """
        self.parent = parent
        self.position = position

        self.g = 0  # Cost from start to the current node
        self.h = 0  # Heuristic (estimated) cost from current node to the end
        self.f = 0  # Total cost (g + h)

    def __eq__(self, other):
        """Checks equality between two nodes by comparing their positions."""
        return self.position == other.position

    def __lt__(self, other):
        """Enables comparison of nodes based on F-score for priority queues."""
        return self.f < other.f


def hex_distance(a, b):
    """Calculates the hexagonal distance between two axial coordinates.

    This is an admissible heuristic for a hexagonal grid as it represents the
    shortest possible number of steps between two hexes.

    Args:
        a (tuple): The first coordinate tuple (q, r).
        b (tuple): The second coordinate tuple (q, r).

    Returns:
        float: The shortest path distance between the two hexes.
    """
    aq, ar = a
    bq, br = b
    # This formula is derived from the conversion to cube coordinates.
    return (abs(aq - bq) + abs(ar - br) + abs(aq + ar - (bq + br))) / 2


def a_star_hex_search_step(grid, start, end):
    """Generator for the A* algorithm that yields each step for visualisation.

    Args:
        grid (dict): A dictionary mapping (q, r) coordinates to cell costs (0=walkable).
        start (tuple): The starting coordinate tuple (q, r).
        end (tuple): The target coordinate tuple (q, r).

    Yields:
        tuple: A tuple containing the current open_list (as Node objects),
               closed_set (as position tuples), and the explored node count.

    Returns:
        list or None: The final path as a list of coordinate tuples upon completion,
                      or None if no path is found.
    """
    start_node = Node(None, start)
    end_node = Node(None, end)

    # The open_list is a priority queue, storing nodes to be evaluated.
    open_list = []
    heapq.heappush(open_list, start_node)
    # The closed_set stores positions of evaluated nodes to prevent reprocessing.
    closed_set = set()

    while open_list:
        current_node = heapq.heappop(open_list)
        closed_set.add(current_node.position)

        # Yield current state to the visualiser.
        yield open_list, closed_set, len(closed_set)

        # If the goal is reached, reconstruct and return the path.
        if current_node == end_node:
            path = []
            current = current_node
            while current is not None:
                path.append(current.position)
                current = current.parent
            return path[::-1]  # Reverse to get path from start to goal.

        # Define the 6 possible neighbour directions in axial coordinates.
        (q, r) = current_node.position
        neighbours = [(1, 0), (1, -1), (0, -1), (-1, 0), (-1, 1), (0, 1)]

        for dq, dr in neighbours:
            neighbour_pos = (q + dq, r + dr)

            # Skip neighbours that are obstacles or have already been evaluated.
            if grid.get(neighbour_pos, 1) != 0 or neighbour_pos in closed_set:
                continue

            # Create a new node for the valid neighbour.
            neighbour_node = Node(current_node, neighbour_pos)
            neighbour_node.g = current_node.g + 1
            neighbour_node.h = hex_distance(neighbour_node.position, end_node.position)
            neighbour_node.f = neighbour_node.g + neighbour_node.h

            # If a better path to this neighbour already exists in the open_list, skip.
            if any(n == neighbour_node and n.g <= neighbour_node.g for n in open_list):
                continue

            heapq.heappush(open_list, neighbour_node)

    return None  # Return None if no path is found.


def reconstruct_full_bidirectional_path(node_fwd, node_bwd):
    """Reconstructs the full path where two bidirectional searches meet.

    Args:
        node_fwd (Node): The meeting node from the forward search.
        node_bwd (Node): The meeting node from the backward search.

    Returns:
        list: A single list of coordinate tuples representing the complete path.
    """
    path = []
    current = node_fwd
    while current is not None:
        path.append(current.position)
        current = current.parent
    path.reverse()  # Path from start to meeting point is now in correct order.

    # Trace back from the backward search, skipping the already-added meeting point.
    current = node_bwd.parent
    while current is not None:
        path.append(current.position)
        current = current.parent
    
    return path


def bidirectional_a_star_hex_search_step(grid, start, end):
    """Generator for the Bidirectional A* algorithm using strict alternation.

    This improved algorithm is particularly effective on large, complex maps
    where a standard A* heuristic can be misleading. It explores from both
    the start and end points simultaneously, taking one step from each search
    in each iteration.

    Args:
        grid (dict): A dictionary mapping (q, r) coordinates to cell costs (0=walkable).
        start (tuple): The starting coordinate tuple (q, r).
        end (tuple): The target coordinate tuple (q, r).

    Yields:
        tuple: A tuple containing the forward and backward open/closed sets
               and the total explored node count.

    Returns:
        list or None: The final path as a list of coordinate tuples upon completion,
                      or None if no path is found.
    """
    # --- Setup for Forward Search (from Start) ---
    open_list_fwd = []
    heapq.heappush(open_list_fwd, Node(None, start))
    closed_set_fwd = {}  # Using a dict {pos: Node} to enable path reconstruction.

    # --- Setup for Backward Search (from End) ---
    open_list_bwd = []
    heapq.heappush(open_list_bwd, Node(None, end))
    closed_set_bwd = {}

    while open_list_fwd and open_list_bwd:
        # --- FORWARD STEP ---
        if open_list_fwd:
            current_node = heapq.heappop(open_list_fwd)
            closed_set_fwd[current_node.position] = current_node

            # If a meeting point is found, reconstruct and return the full path.
            if current_node.position in closed_set_bwd:
                node_bwd = closed_set_bwd[current_node.position]
                return reconstruct_full_bidirectional_path(current_node, node_bwd)

            # Standard neighbour generation for the forward search.
            for dq, dr in [(1, 0), (1, -1), (0, -1), (-1, 0), (-1, 1), (0, 1)]:
                neighbor_pos = (current_node.position[0] + dq, current_node.position[1] + dr)
                if grid.get(neighbor_pos, 1) != 0 or neighbor_pos in closed_set_fwd:
                    continue
                neighbor_node = Node(current_node, neighbor_pos)
                neighbor_node.g = current_node.g + 1
                neighbor_node.h = hex_distance(neighbor_node.position, end)
                neighbor_node.f = neighbor_node.g + neighbor_node.h
                if not any(n == neighbor_node and n.g <= neighbor_node.g for n in open_list_fwd):
                    heapq.heappush(open_list_fwd, neighbor_node)

        # --- BACKWARD STEP ---
        if open_list_bwd:
            current_node = heapq.heappop(open_list_bwd)
            closed_set_bwd[current_node.position] = current_node

            # If a meeting point is found, reconstruct and return the full path.
            if current_node.position in closed_set_fwd:
                node_fwd = closed_set_fwd[current_node.position]
                return reconstruct_full_bidirectional_path(node_fwd, current_node)

            # Standard neighbour generation for the backward search.
            for dq, dr in [(1, 0), (1, -1), (0, -1), (-1, 0), (-1, 1), (0, 1)]:
                neighbor_pos = (current_node.position[0] + dq, current_node.position[1] + dr)
                if grid.get(neighbor_pos, 1) != 0 or neighbor_pos in closed_set_bwd:
                    continue
                neighbor_node = Node(current_node, neighbor_pos)
                neighbor_node.g = current_node.g + 1
                neighbor_node.h = hex_distance(neighbor_node.position, start)
                neighbor_node.f = neighbor_node.g + neighbor_node.h
                if not any(n == neighbor_node and n.g <= neighbor_node.g for n in open_list_bwd):
                    heapq.heappush(open_list_bwd, neighbor_node)

        # Yield the state of both searches to the visualiser.
        total_explored = len(closed_set_fwd) + len(closed_set_bwd)
        yield open_list_fwd, closed_set_fwd.keys(), open_list_bwd, closed_set_bwd.keys(), total_explored
        
    return None  # Return None if no path is found.