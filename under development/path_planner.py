import numpy as np 
import heapq

class Dijkstra:
    def __init__(self):
        self.start=(0,0)
        self.goal=(9,9)
        self.path = ()
        
        self.grid = np.array([
            [0, 0, 0, 0, 0, 0, 0, 1, 0, 0],
            [0, 1, 1, 1, 0, 0, 0, 1, 0, 0],
            [0, 0, 0, 1, 0, 0, 0, 1, 0, 0],
            [0, 0, 0, 1, 0, 1, 1, 1, 0, 0],
            [0, 1, 0, 0, 0, 0, 0, 1, 0, 0],
            [0, 1, 1, 1, 1, 1, 0, 1, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 1, 0, 0],
            [0, 0, 1, 1, 1, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 1, 1, 1, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        ])
        
        self.costs = np.array([
            [1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
            [1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
            [1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
            [1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
            [1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
            [1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
            [1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
            [1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
            [1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
            [1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
        ])

    # def plot_grid(self,grid, path=None):
    #     """
    #     Plots the grid with optional path overlay.
    #     Args:
    #     - grid (2D array): The environment.
    #     - path (list of tuples): The path to overlay (optional).
    #     """
    #     # Anootate costs
    #     rows, cols = self.grid.shape
    #     for i in range(rows):
    #         for j in range(cols):
    #             if grid[i][j] == 0:
    #                 plt.text(j, i, f'{costs[i][j]}', ha='center', va='center', color=('lightgray'), fontsize=10)

    #     if path:
    #         i = []
    #         j = []
    #         for (x, y) in path:
    #             plt.scatter(y, x, color="red")
    #             i.append(x)
    #             j.append(y)
    #         plt.plot(j,i, 'r')
    #     plt.title("Map of the Environment")
    #     # plt.grid(True)
    #     plt.show()

    # grid = create_grid()
    # plot_grid(grid)

    def plan(self, grid, costs, start, goal):
        """
        Implements Dijkstra's Algorithm for a grid-based environment.
        Args:
        - grid (2D array): The environment grid.
        - costs (2D array): The cost of moving through each cell.
        - start (tuple): The start node (row, col).
        - goal (tuple): The goal node (row, col).

        Returns:
        - path (list of tuples): The shortest path from start to goal.
        """
        rows, cols = self.grid.shape
        visited = set()
        distances = {start: 0}  # Distance to the start node is 0
        parents = {start: None}  # A parent is the node that preceeds the current one: used to reconstruct the path

        priority_queue = []  # Priority queue ensures that nodes are processed in order of increasing distance
        heapq.heappush(priority_queue, (0, start))  # Initializes queue with the start node and distance to start

        directions = [(0, 1), (1, 0), (0, -1), (-1, 0)]  # Right, Down, Left, Up

        while priority_queue:
            current_distance, current_node = heapq.heappop(priority_queue)

            #  If a node has already been visited, it means the shortest distance to that node has been determined.
            if current_node in visited:
                continue 
            visited.add(current_node)

            # If the current node is the goal node, then the path has been found.
            if current_node == goal:
                break

            # Gets the coordinates of each neighboring cell
            for direction in directions:
                neighbor = (current_node[0] + direction[0], current_node[1] + direction[1])

                # Can only move within the boundaries of the world, and if there's no obstacle
                if (0 <= neighbor[0] < rows and 0 <= neighbor[1] < cols and grid[neighbor] == 0):
                    distance = current_distance + costs[neighbor]  # Use cost from the `costs` array

                    # Updates the shortest known distance to a neighboring node and prepares it for further exploration
                    if neighbor not in distances or distance < distances[neighbor]:
                        distances[neighbor] = distance  # Updates the shortest known distance to the neighbor
                        parents[neighbor] = current_node # Makes the current node be the parent of the neighbor to reconstruct the shortest path
                        heapq.heappush(priority_queue, (distance, neighbor))  # Adds the neighbor to the priority queue with its updated distance as the priority

        # Reconstruct path from the goal to the start
        path = []
        node = goal
        while node is not None:
            if node not in parents:
                print(f"Error: Node {node} has no parent. Path reconstruction failed.")
                return []
            path.append(node)
            node = parents[node]  # Gets the parent of the node
        path.reverse()  # Reverse the path to make it from start to the goal node
        return self.path
                

        
        
    
        
    
