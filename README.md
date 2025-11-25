# Shortest Path Comparison

Final Project for COCS 520: Advanced Algorithms

Comprehensive analysis and comparison of **shortest-path** algorithms and priority queue data structures.

## Project Overview

This project implements and compares several variants of Dijkstra’s shortest path algorithm on large, randomly generated weighted graphs. The goal is to understand how different priority queue designs and search strategies affect runtime, scalability, and memory usage in practical settings.

We implement Dijkstra’s algorithm using three priority queue structures:

- **Binary Heap** — the standard baseline with \(O(\log n)\) operations.  
- **Fibonacci Heap** — an asymptotically optimal structure with amortized \(O(1)\) decrease-key.  
- **Radix Heap** — a monotone integer heap optimized for Dijkstra’s non-decreasing distance keys.

Beyond standard Dijkstra, we also implement:

- **Bidirectional Dijkstra with skewed expansion**, which searches from both the source and the target to reduce the explored space.  
- **Contraction Hierarchies (CH)**, a preprocessing-based speed-up technique widely used in road-network routing systems.

All data structures and algorithms are implemented **from scratch in Python**, and evaluated on large Erdős–Rényi (ER) graphs ranging from **10K to 2M nodes**. We measure both **runtime** and **peak memory usage** using controlled experiments.

The repository also includes an **interactive visualization tool** that demonstrates how each algorithm explores the search space in real time on a grid-based graph.

Overall, this project provides a unified, empirical comparison of priority queue designs, search strategies, and hierarchical routing techniques, illustrating how theoretical properties translate to real-world performance in Python.

## Supplemental Material

The final report with further analysis and implementation details can be found at [/latex/final_report.pdf](/latex/final_report.pdf).

A demo of the visualization tool can be found on YouTube at [https://youtu.be/A_zrF0KwM_s](https://youtu.be/A_zrF0KwM_s)

Our presentation can be found [here](https://docs.google.com/presentation/d/1kqYFEPA8z06mKvAEL735WVigTZRAgPyX3ZdeN_tEBCw/edit?usp=sharing)

## Repository Structure

```
shortest_path_comparison/
├── src/                               # Source code
│   ├── algorithms/                    # Algorithm implementations
│   │   ├── dijkstra.py                # Standard Dijkstra with interchangeable heap backends
│   │   ├── bidirectional_skewed.py    # Bidirectional Dijkstra with skewness parameter
│   │   └── contraction_hierarchy.py   # Contraction Hierarchies (Preprocessing + Query)
│   │
│   ├── data_structures/               # Priority queue implementations
│   │   ├── binary_heap.py
│   │   ├── fibonacci_heap.py
│   │   └── radix_heap.py
│   │
│   ├── utils/
│   │   ├── graph_generator.py         # Random directed graph generator
│   │   └── runtime_analysis.py        # Runtime analysis script for Dijkstra and Bidirectional Dijkstra algorithms for all 3 heaps
│   │   └── benchmark_ch.py            # Runtime analysis script for Contraction Hierarchies
│   │
│   └── visualization/                 # Interactive Pygame visualization
│       ├── main.py                    # Main visualization loop and event handling
│       ├── grid.py                    # Grid state management and rendering
│       ├── visual_algorithms.py       # Generator-based visual algorithm wrappers
│       └── presets.py                 # Preset grid configurations
│
├── unit_tests/                        # Unit tests for all implemented algorithms
│   ├── test_binary_heap.py
│   ├── test_fibonacci_heap.py
│   ├── test_radix_heap.py
│   ├── test_dijkstra.py
│   ├── test_bidirectional_dijkstra.py
│   ├── test_bidirectional_skewed.py
│   ├── test_contraction_hierarchy.py
│   └── test_graph_generator.py
│
├── latex/                              # Final report materials (tex files, compiled pdf)
│   └── plots/                          # Plots for final report
│
├── requirements.txt                    # Project dependencies
├── LICENSE                             # Project license
└── README.md                           # Project documentation
```

## Running the Code

### 1️⃣ Install Dependencies

```bash
pip install matplotlib tqdm
```

### 2️⃣ Run Unit Tests

**Run all tests at once:**
```bash
python -m unittest discover -s unit_tests -p "test_*.py" -v
```

**Run individual test files (optional):**
```bash
python -m unittest unit_tests/test_binary_heap.py -v
python -m unittest unit_tests/test_dijkstra.py -v
```
### 3️⃣ Run the Runtime Benchmark

**Run the benchmark:**
```bash
python src.utils.runtime_analysis.py
```

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
