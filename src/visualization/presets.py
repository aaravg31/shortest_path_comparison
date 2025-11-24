"""
Preset maze configurations for visualization
"""
import random

def get_50x50_maze():
    """
    Returns a preset maze for 50x50 grid with:
    - Start: (0, 0) - top left
    - End: (49, 49) - bottom right
    - Generated using Recursive Backtracker for a solveable maze structure
    """
    rows, cols = 50, 50
    walls = set()
    
    # Initialize all cells as walls
    for r in range(rows):
        for c in range(cols):
            walls.add((r, c))
            
    start_cell = (1, 1)
    visited = {start_cell}
    stack = [start_cell]
    
    # Remove start cell from walls
    walls.discard(start_cell)
    
    # Recursive Backtracker
    while stack:
        current = stack[-1]
        r, c = current
        
        # Find unvisited neighbors
        neighbors = []
        # Directions for jumping 2 cells
        directions = [(0, 2), (0, -2), (2, 0), (-2, 0)]
        
        for dr, dc in directions:
            nr, nc = r + dr, c + dc
            if 1 <= nr < rows and 1 <= nc < cols and (nr, nc) not in visited:
                neighbors.append((nr, nc))
                
        if neighbors:
            next_cell = random.choice(neighbors)
            nr, nc = next_cell
            
            # Remove the wall between current and next
            wall_r, wall_c = (r + nr) // 2, (c + nc) // 2
            walls.discard((wall_r, wall_c))
            
            # Remove the next cell from walls to make it a path
            walls.discard(next_cell)
            
            visited.add(next_cell)
            stack.append(next_cell)
        else:
            stack.pop()
            
    # Post-processing to ensure start and end are open and connected
    walls.discard((0, 0))
    walls.discard((0, 1))
    walls.discard((49, 49))
    
    return {
        'start': (0, 0),
        'end': (49, 49),
        'walls': walls
    }
