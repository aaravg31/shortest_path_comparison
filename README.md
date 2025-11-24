# Shortest Path Comparison

Final Project for COCS 520: Advanced Algorithms

Comprehensive analysis and comparison of **shortest-path** algorithms and priority queue data structures.

## Project Overview

This project investigates the performance characteristics of **Dijkstra’s shortest path algorithm** using different underlying heap / priority-queue data structures, as well as advanced variants like **Bidirectional Dijkstra** and **Contraction Hierarchies**.

The primary objectives are:

1.  **Heap Comparison**: Implement and compare Binary Heap, Fibonacci Heap, and Radix Heap backends for Dijkstra's algorithm.
2.  **Algorithmic Variants**: Implement and evaluate Bidirectional Dijkstra (with skewness) and Contraction Hierarchies as speed-up techniques.
3.  **Benchmarking**: Measure runtime performance on large, randomly generated graphs to validate theoretical complexity differences.

## Supplemental Material

The final report with further analysis and implementation details can be found at [/latex/final_report.pdf](/latex/final_report.pdf).

Our presentation can be found at ???

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
│   ├── utils/
│   │   ├── graph_generator.py         # Random directed graph generator
│   │   └── benchmark_dijkstra.py      # Runtime analysis script
│   └── visualization/                 # Interactive Pygame visualization
│       ├── main.py                    # Main visualization loop and event handling
│       ├── grid.py                    # Grid state management and rendering
│       ├── visual_algorithms.py       # Generator-based visual algorithm wrappers
│       └── presets.py                 # Preset grid configurations
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
├── LICENSE
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

## Visualization

An interactive Pygame-based visualization is included to demonstrate the algorithms on a grid. The user is able to create a grid of nodes (potential paths) and walls, and then run each algorithm to find the shortest path between the start and end nodes. The red nodes represent those that have been visited by the algorithm once it has run.

_Note:_ the Contraction Hierarchies approach must preprocess the graph before running the query to find the shortest path. In this case, the red nodes will appear very sparse, as the algorithm only visits a small number of nodes to find the shortest path once the preprocessing has determined the shortcuts. The gold lines represent the shortcuts that were used to find the final shortest path.

### Setup

1. Install the visualization dependencies:
   ```bash
   pip install -r requirements.txt
   ```

### Running

Run the visualization module:

```bash
python -m src.visualization.main
```

**Optional Arguments:**

- `--rows N`: Set grid size to NxN (default: 30)
  - Example: `python -m src.visualization.main --rows 50` for a 50x50 grid
  - Larger grids provide more detail but may slow down the visualization
  - The 50x50 grid is preset with a maze structure for ease of use
- `--heap TYPE`: Set heap/priority queue type (default: binary)
  - Choices: `binary`, `fibonacci`, `radix`
  - Example: `python -m src.visualization.main --heap fibonacci`
  - Affects all algorithms (Dijkstra, Bidirectional, Contraction Hierarchies)
  - Use to compare heap performance characteristics

### Controls

- **Left Click**: Place Start (Orange), End (Turquoise), or Walls (Black).
- **Right Click**: Remove items.
- **1**: Select Dijkstra's Algorithm.
- **2**: Select Bidirectional Dijkstra.
- **3**: Select Contraction Hierarchies.
- **`** (Backtick): Generate random walls.
- **SPACE**: Run the selected algorithm.
- **R**: Reset path (keep walls).
- **C**: Clear board.

## License

This project is licensed under the MIT License.
