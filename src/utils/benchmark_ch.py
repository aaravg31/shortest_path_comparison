
import time
import tracemalloc
import random
from src.algorithms.contraction_hierarchy import ContractionHierarchy
from src.utils.graph_generator import generate_er_graph

def benchmark_ch():
    sizes = [
        (100, 4),
        (500, 6),
        (1_000, 8),
        (2_000, 10),
    ]
    
    results = []

    for num_nodes, avg_edges in sizes:
        approx_edges = avg_edges * num_nodes
        print(f"Generating graph with {num_nodes} nodes...")
        graph = generate_er_graph(num_nodes, approx_edges, seed=42, show_progress=False)
        
        print(f"Initializing CH for {num_nodes} nodes...")
        ch = ContractionHierarchy(graph)
        
        # Measure Preprocessing
        print("Starting Preprocessing...")
        start_pre = time.perf_counter()
        ch.preprocess()
        end_pre = time.perf_counter()
        preprocess_time = end_pre - start_pre
        print(f"Preprocessing done in {preprocess_time:.4f}s")
        
        # Measure Query
        print("Starting Queries...")
        query_times = []
        num_queries = 10
        random.seed(42)
        
        for _ in range(num_queries):
            s = random.randint(0, num_nodes - 1)
            t = random.randint(0, num_nodes - 1)
            
            start_q = time.perf_counter()
            dist = ch.query(s, t)
            end_q = time.perf_counter()
            query_times.append(end_q - start_q)
            
        avg_query_time = sum(query_times) / len(query_times)
        print(f"Avg Query time: {avg_query_time:.6f}s")
        
        results.append({
            "nodes": num_nodes,
            "preprocess_time": preprocess_time,
            "query_time": avg_query_time
        })
        
    print("\nFinal Results:")
    for res in results:
        print(res)

if __name__ == "__main__":
    benchmark_ch()
