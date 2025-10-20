# a_star.py
"""
A* Pathfinding Algorithm for Hexagonal Grids
============================================

This module implements the A* pathfinding algorithm adapted for use
on hexagonal grids with axial coordinates. It also includes a generator
version of A* for visualisation purposes.
"""

import heapq


class Node:
    """
    Represents a single node used in the A* pathfinding algorithm.

    Each node stores its position, parent, and scoring information used
    to determine the optimal path between two points on a hexagonal grid.

    **Attributes**
        parent : Node | None
            The parent node from which this node was reached.
        position : tuple[int, int]
            The axial coordinates (q, r) of this node on the grid.
        g : float
            The movement cost from the start node to this node.
        h : float
            The heuristic estimate of the cost from this node to the goal.
        f : float
            The total estimated cost (f = g + h).

    **Methods**
        __eq__(other)
            Checks equality between nodes by comparing positions.
        __lt__(other)
            Enables comparison of nodes based on F-score for use in priority queues.
    """

    def __init__(self, parent=None, position=None):
        """
        Initialise a new Node object.

        :param parent: The parent node that led to this node.
        :param position: The position of the node on the grid as (q, r).
        """
        self.parent = parent
        self.position = position  # Axial coordinates: (q, r)

        self.g = 0  # Cost from start to the current node
        self.h = 0  # Estimated cost to the goal
        self.f = 0  # Total cost (g + h)

    def __eq__(self, other):
        """
        Compare two nodes for equality based on their positions.

        :param other: Another Node instance to compare against.
        :return: True if both nodes have the same position, otherwise False.
        """
        return self.position == other.position

    def __lt__(self, other):
        """
        Compare two nodes based on their F scores.

        Enables nodes to be correctly ordered in a priority queue (min heap).

        :param other: Another Node instance to compare against.
        :return: True if this node's F score is less than the others, otherwise False.
        :rtype: bool
        """
        return self.f < other.f


def hex_distance(a, b):
    """
    Calculate the hexagonal distance between two axial coordinates.

    Uses the standard hex grid distance formula based on cube coordinate equivalence.

    :param a: The first coordinate (q, r).
    :param b: The second coordinate (q, r).
    :return: The hexagonal distance between the two coordinates.
    """
    aq, ar = a
    bq, br = b
    return (abs(aq - bq) + abs(ar - br) + abs(aq + ar - (bq + br))) / 2


def a_star_hex_search(grid, start, end):
    """
    Find a path between two points on a hexagonal grid using the A* algorithm.

    The function returns a list of coordinates representing the optimal path
    from start to end, avoiding any obstacles defined in grid.

    :param grid: A dictionary mapping axial coordinates (q, r) to cell states.
                 A value of 0 represents a walkable cell, while 1 represents an obstacle.
    :param start: The starting coordinate as a tuple (q, r).
    :param end: The target coordinate as a tuple (q, r).
    :return: A list of coordinates forming the path from start to end, or None if no path exists.
    """
    start_node = Node(None, start)
    end_node = Node(None, end)

    open_list = []
    heapq.heappush(open_list, start_node)
    closed_set = set()

    while open_list:
        current_node = heapq.heappop(open_list)
        closed_set.add(current_node.position)

        # If the goal is reached, reconstruct the path
        if current_node == end_node:
            path = []
            current = current_node
            while current is not None:
                path.append(current.position)
                current = current.parent
            return path[::-1]  # Reverse to get path from start to goal

        # Neighbouring hex cells 
        (q, r) = current_node.position
        neighbours = [(1, 0), (1, -1), (0, -1), (-1, 0), (-1, 1), (0, 1)]

        for dq, dr in neighbours:
            neighbour_pos = (q + dq, r + dr)

            # Skip obstacles or out of bound cells
            if grid.get(neighbour_pos, 1) != 0:
                continue
            if neighbour_pos in closed_set:
                continue

            neighbour_node = Node(current_node, neighbour_pos)
            neighbour_node.g = current_node.g + 1
            neighbour_node.h = hex_distance(neighbour_node.position, end_node.position)
            neighbour_node.f = neighbour_node.g + neighbour_node.h

            # Skip if already in open list with a lower g score
            in_open_list = False
            for open_node in open_list:
                if neighbour_node == open_node and neighbour_node.g >= open_node.g:
                    in_open_list = True
                    break

            if in_open_list:
                continue

            heapq.heappush(open_list, neighbour_node)

    # No valid path found
    return None


def a_star_hex_search_step(grid, start, end):
    """
    Generator version of A* for visualisation or debugging.

    Yields the open and closed sets after each expansion step,
    allowing the algorithms progress to be visualised frame-by-frame.

    :param grid: A dictionary mapping axial coordinates (q, r) to cell states.
    :param start: The starting coordinate as a tuple (q, r).
    :param end: The target coordinate as a tuple (q, r).
    :yield: The current open_list and closed_set at each step.
    :return: The final path as a list of coordinates when the search completes.
    """
    start_node = Node(None, start)
    end_node = Node(None, end)

    open_list = []
    heapq.heappush(open_list, start_node)
    closed_set = set()

    while open_list:
        current_node = heapq.heappop(open_list)
        closed_set.add(current_node.position)

        # Yield current state to allow live visualisation
        yield open_list, closed_set

        # If goal reached, return full path
        if current_node == end_node:
            path = []
            current = current_node
            while current is not None:
                path.append(current.position)
                current = current.parent
            return path[::-1]

        (q, r) = current_node.position
        neighbours = [(1, 0), (1, -1), (0, -1), (-1, 0), (-1, 1), (0, 1)]

        for dq, dr in neighbours:
            neighbour_pos = (q + dq, r + dr)

            if grid.get(neighbour_pos, 1) != 0:
                continue
            if neighbour_pos in closed_set:
                continue

            neighbour_node = Node(current_node, neighbour_pos)
            neighbour_node.g = current_node.g + 1
            neighbour_node.h = hex_distance(neighbour_node.position, end_node.position)
            neighbour_node.f = neighbour_node.g + neighbour_node.h

            in_open_list = False
            for open_node in open_list:
                if neighbour_node == open_node and neighbour_node.g >= open_node.g:
                    in_open_list = True
                    break

            if in_open_list:
                continue

            heapq.heappush(open_list, neighbour_node)

    # No valid path found
    return None
