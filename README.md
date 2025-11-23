# Shortest Path Comparison
Cosc 520 — Advanced Algorithms
Final Project: Performance comparison of shortest-path algorithms and priority queue data structures

## Project Overview

This project investigates the performance characteristics of **Dijkstra’s shortest path algorithm** using different underlying heap / priority-queue data structures, as well as advanced variants like **Bidirectional Dijkstra** and **Contraction Hierarchies**.

The primary objectives are:
1.  **Heap Comparison**: Implement and compare Binary Heap, Fibonacci Heap, and Radix Heap backends for Dijkstra's algorithm.
2.  **Algorithmic Variants**: Implement and evaluate Bidirectional Dijkstra (with skewness) and Contraction Hierarchies as speed-up techniques.
3.  **Benchmarking**: Measure runtime performance on large, randomly generated graphs to validate theoretical complexity differences.

## Repository Structure

```
shortest_path_comparison/
├── src/
│   ├── algorithms/
│   │   ├── dijkstra.py                # Standard Dijkstra with interchangeable heap backends
│   │   ├── bidirectional_dijkstra.py  # Bidirectional Dijkstra implementation
│   │   ├── bidirectional_skewed.py    # Bidirectional Dijkstra with skewness parameter
│   │   └── contraction_hierarchy.py   # Contraction Hierarchies (Preprocessing + Query)
│   ├── data_structures/               # Priority queue implementations
│   │   ├── binary_heap.py
│   │   ├── fibonacci_heap.py
│   │   └── radix_heap.py
│   └── utils/
│       ├── graph_generator.py         # Random directed graph generator
│       └── benchmark_dijkstra.py      # Runtime analysis script
│
├── unit_tests/
│   ├── test_binary_heap.py
│   ├── test_fibonacci_heap.py
│   ├── test_radix_heap.py
│   ├── test_dijkstra.py
│   ├── test_bidirectional_dijkstra.py
│   ├── test_bidirectional_skewed.py
│   ├── test_contraction_hierarchy.py
│   └── test_graph_generator.py
│
├── latex/                              # Final report materials (plots, tex files)
│   └── plots/
│
├── requirements.txt
└── README.md
```

## Implementation Status

### Core Algorithms & Data Structures
- **Heaps**: BinaryHeap, FibonacciHeap, and RadixHeap are fully implemented and tested.
- **Dijkstra**: Standard implementation supporting all heap backends.
- **Bidirectional Dijkstra**: Implemented with support for skewness to control search balance.
- **Contraction Hierarchies**: Implemented with node contraction preprocessing and bidirectional query.

### Benchmarking & Utilities
- **Graph Generation**: Basic random graph generator included.
- **Benchmarking**: Initial pipeline established for comparing heap performance.

## Future Work

- **Optimization**: Further optimize Radix Heap for large-scale graphs.
- **Advanced Generation**: Implement scale-free and geometric graph generators for more realistic benchmarks.
- **Analysis**: Conduct comprehensive performance analysis comparing all algorithms and data structures for the final report.
