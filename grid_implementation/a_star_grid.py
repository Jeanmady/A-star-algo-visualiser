#a_star.py
import heapq

class Node:

    def __init__(self, parent=None, position=None):
        self.parent = parent
        self.position = position  # Stored as a tuple: (row, col)

        self.g = 0  # Cost from start to the current node
        self.h = 0  # Heuristic cost from current node to the end
        self.f = 0  # Total cost: g + h

    def __eq__(self, other):

        return self.position == other.position

    def __lt__(self, other):
  
        return self.f < other.f


def a_star_search(grid, start, end):
    # Create start and end node objects
    start_node = Node(None, start)
    end_node = Node(None, end)

    # Initialise the open list (as a priority queue) and the closed list (as a set for fast lookups)
    open_list = []
    heapq.heappush(open_list, start_node)
    closed_set = set()

    # Loop until the open list is empty
    while open_list:

        # Get the node with the lowest f score from the priority queue
        current_node = heapq.heappop(open_list)
        closed_set.add(current_node.position)

        # Check if we have reached the end
        if current_node == end_node:
            path = []
            current = current_node
            while current is not None:
                path.append(current.position)
                current = current.parent
            return path[::-1]  # Return reversed path

        # Generate children (neighbors)
        (row, col) = current_node.position
        # Defines possible movements: up, down, left, right
        neighbors = [(0, 1), (0, -1), (1, 0), (-1, 0)] 
        
        for move_r, move_c in neighbors:
            neighbor_pos = (row + move_r, col + move_c)

            # Make sure neighbor is within grid bounds
            if not (0 <= neighbor_pos[0] < len(grid) and 0 <= neighbor_pos[1] < len(grid[0])):
                continue

            # Make sure neighbor is a walkable path
            if grid[neighbor_pos[0]][neighbor_pos[1]] != 0:
                continue
            
            # Make sure neighbor is not on the closed list
            if neighbor_pos in closed_set:
                continue

            # Create neighbor node
            neighbor_node = Node(current_node, neighbor_pos)

            # Calculate the g, h, and f values
            neighbor_node.g = current_node.g + 1 # Cost is 1 for each step
            # Heuristic: Manhattan distance (good for grids)
            neighbor_node.h = abs(neighbor_node.position[0] - end_node.position[0]) + \
                              abs(neighbor_node.position[1] - end_node.position[1])
            neighbor_node.f = neighbor_node.g + neighbor_node.h

            # Check if neighbor is in open list with a lower g score
            # This is an optimization to find better paths
            is_in_open_list = False
            for open_node in open_list:
                if neighbor_node == open_node and neighbor_node.g >= open_node.g:
                    is_in_open_list = True
                    break
            
            if is_in_open_list:
                continue

            # Add the neighbor to the open list
            heapq.heappush(open_list, neighbor_node)
            
    return None # Return None if no path was found