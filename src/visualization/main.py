import pygame
import math
import time
from src.visualization.grid import Grid
from src.visualization.visual_algorithms import (
    dijkstra_visual,
    bidirectional_dijkstra_visual,
    contraction_hierarchy_visual
)
# Import non-visual versions for timing
from src.algorithms.dijkstra import dijkstra
from src.algorithms.bidirectional_skewed import BidirectionalDijkstra
from src.algorithms.contraction_hierarchy import ContractionHierarchy

# Window setup
ROWS = 50 # dimension of N x N grid
WIDTH = math.floor(1000/ROWS) * ROWS # Create the window rougly 1000 pixels wide
WIN = pygame.display.set_mode((WIDTH, WIDTH))
pygame.display.set_caption("Shortest Path Visualization")

def main():
    grid = Grid(ROWS, WIDTH)

    start = None
    end = None

    run = True
    started = False
    
    current_algo_name = "Dijkstra"
    algorithm_generator = None
    shortcuts_to_draw = []  # For CH visualization
    
    clock = pygame.time.Clock()

    while run:
        grid.draw(WIN, shortcuts=shortcuts_to_draw if current_algo_name == "Contraction Hierarchy" else None)
        
        # If algorithm is running
        if started and algorithm_generator:
            try:
                # Control speed
                # clock.tick(60) # Uncapped for max speed, or limit for visibility
                
                result = next(algorithm_generator)
                
                # Handle different return formats
                if current_algo_name == "Contraction Hierarchy" and len(result) == 4:
                    visited, frontier, path, shortcuts = result
                    shortcuts_to_draw = shortcuts  # Store shortcuts for drawing
                else:
                    visited, frontier, path = result
                    shortcuts_to_draw = []
                
                for r, c in visited:
                    node = grid.get_node(r, c)
                    if not node.is_start() and not node.is_end():
                        node.make_closed()
                        
                for r, c in frontier:
                    node = grid.get_node(r, c)
                    if not node.is_start() and not node.is_end():
                        node.make_open()
                        
                if path:
                    for r, c in path:
                        node = grid.get_node(r, c)
                        if not node.is_start() and not node.is_end():
                            node.make_path()
                    started = False # Finished
                    
            except StopIteration:
                started = False
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False

            if started:
                continue

            if pygame.mouse.get_pressed()[0]: # LEFT CLICK
                pos = pygame.mouse.get_pos()
                row, col = grid.get_clicked_pos(pos)
                node = grid.get_node(row, col)
                if node:
                    if not start and node != end:
                        start = node
                        start.make_start()
                    elif not end and node != start:
                        end = node
                        end.make_end()
                    elif node != end and node != start:
                        node.make_barrier()

            elif pygame.mouse.get_pressed()[2]: # RIGHT CLICK
                pos = pygame.mouse.get_pos()
                row, col = grid.get_clicked_pos(pos)
                node = grid.get_node(row, col)
                if node:
                    node.reset()
                    if node == start:
                        start = None
                    elif node == end:
                        end = None

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE and start and end:
                    graph = grid.to_adjacency_dict()
                    start_pos = start.get_pos()
                    end_pos = end.get_pos()
                    
                    grid.clear_path()
                    
                    # Run non-visual version for timing
                    print(f"\nRunning {current_algo_name}...")
                    start_time = time.perf_counter()
                    
                    if current_algo_name == "Dijkstra":
                        distances = dijkstra(graph, start_pos, heap_type="binary")
                        elapsed_time = time.perf_counter() - start_time
                        print(f"Dijkstra completed in {elapsed_time*1000:.2f} ms")
                        algorithm_generator = dijkstra_visual(graph, start_pos, end_pos)
                        
                    elif current_algo_name == "Bidirectional":
                        bi_dijkstra = BidirectionalDijkstra(graph, heap_type="binary")
                        distance = bi_dijkstra.find_shortest_path(start_pos, end_pos)
                        elapsed_time = time.perf_counter() - start_time
                        print(f"Bidirectional Dijkstra completed in {elapsed_time*1000:.2f} ms")
                        algorithm_generator = bidirectional_dijkstra_visual(graph, start_pos, end_pos)
                        
                    elif current_algo_name == "Contraction Hierarchy":
                        print("Preprocessing CH...")
                        ch = ContractionHierarchy(graph)
                        ch.preprocess()
                        preprocess_time = time.perf_counter() - start_time
                        
                        query_start = time.perf_counter()
                        distance = ch.query(start_pos, end_pos)
                        query_time = time.perf_counter() - query_start
                        
                        print(f"CH Preprocessing: {preprocess_time*1000:.2f} ms")
                        print(f"CH Query: {query_time*1000:.2f} ms")
                        print(f"CH Total: {(preprocess_time + query_time)*1000:.2f} ms")
                        
                        algorithm_generator = contraction_hierarchy_visual(graph, start_pos, end_pos)
                        
                    started = True
                    
                if event.key == pygame.K_c:
                    start = None
                    end = None
                    shortcuts_to_draw = []
                    grid.clear()
                    
                if event.key == pygame.K_r:
                    shortcuts_to_draw = []
                    grid.clear_path()
                    started = False
                    
                if event.key == pygame.K_1:
                    current_algo_name = "Dijkstra"
                    print("Selected: Dijkstra")
                    pygame.display.set_caption(f"Shortest Path Visualization - {current_algo_name}")
                    
                if event.key == pygame.K_2:
                    current_algo_name = "Bidirectional"
                    print("Selected: Bidirectional Dijkstra")
                    pygame.display.set_caption(f"Shortest Path Visualization - {current_algo_name}")
                    
                if event.key == pygame.K_3:
                    current_algo_name = "Contraction Hierarchy"
                    print("Selected: Contraction Hierarchy")
                    pygame.display.set_caption(f"Shortest Path Visualization - {current_algo_name}")
                
                if event.key == pygame.K_BACKQUOTE:  # Backtick key
                    grid.generate_random_walls(density=0.25)
                    print("Generated random walls")

    pygame.quit()

if __name__ == "__main__":
    main()
