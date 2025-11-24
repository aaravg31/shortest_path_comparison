"""
Preset maze configurations for visualization
"""

def get_50x50_maze():
    """
    Returns a preset maze for 50x50 grid with:
    - Start: (0, 0) - top left
    - End: (49, 49) - bottom right
    - Multiple possible paths
    - Interesting maze structure
    """
    walls = set()
    
    # Create vertical walls with gaps for multiple paths
    for row in range(5, 45):
        if row % 10 not in [3, 4, 7]:  # Gaps every 10 rows
            walls.add((row, 10))
            walls.add((row, 20))
            walls.add((row, 30))
            walls.add((row, 40))
    
    # Create horizontal walls with gaps
    for col in range(5, 45):
        if col % 10 not in [2, 5, 8]:  # Gaps every 10 cols
            walls.add((15, col))
            walls.add((25, col))
            walls.add((35, col))
    
    # Add some diagonal barriers
    for i in range(20):
        walls.add((i + 5, i + 5))
        walls.add((i + 25, 45 - i))
    
    # Create a challenging center section
    for row in range(20, 30):
        for col in range(20, 30):
            if (row + col) % 3 == 0 and (row, col) not in [(20, 20), (29, 29)]:
                walls.add((row, col))
    
    # Add some random obstacles in quadrants
    obstacles = [
        # Top-left quadrant
        (8, 15), (8, 16), (9, 15), (9, 16),
        # Top-right quadrant  
        (12, 42), (13, 42), (12, 43), (13, 43),
        # Bottom-left quadrant
        (38, 8), (38, 9), (39, 8), (39, 9),
        # Bottom-right quadrant
        (42, 38), (43, 38), (42, 39), (43, 39),
    ]
    walls.update(obstacles)
    
    # Ensure start and end are not blocked
    walls.discard((0, 0))
    walls.discard((49, 49))
    walls.discard((0, 1))
    walls.discard((1, 0))
    walls.discard((48, 49))
    walls.discard((49, 48))
    
    return {
        'start': (0, 0),
        'end': (49, 49),
        'walls': walls
    }
