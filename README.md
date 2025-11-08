# Shortest Path Comparison  
Cosc 520 — Advanced Algorithms  
Final Project: Performance comparison of shortest-path algorithms and priority queue data structures

## 📌 Project Overview

This project investigates the performance characteristics of **Dijkstra’s shortest path algorithm** using different underlying heap / priority-queue data structures, as well as **bidirectional variants** of Dijkstra that incorporate skewness to accelerate search.

The main goals of this project are:

- ✅ Implement and compare **three heap structures** used inside Dijkstra:
  - **Binary Heap**  
  - **Fibonacci Heap**  
  - **Radix Heap** (functional but not yet optimized)

- ✅ Implement and test **standard Dijkstra's algorithm** using each heap backend.

- 🔜 Implement **Bidirectional Dijkstra with skewness**, and compare its performance across the three heap structures.

- ✅ Provide initial benchmarking tools to measure algorithmic performance on large, randomly generated graphs.

This work is part of the final project for **Cosc 520: Advanced Algorithms**, focusing on real-world performance differences between theoretical data structures and algorithms.

---

## 📁 Updated Repository Structure

```
shortest_path_comparison/
├── src/
│   ├── algorithms/
│   │   ├── dijkstra.py                # Standard Dijkstra with interchangeable heap backends
│   │   └── bidirectional_skewed.py    # (TBD) Bidirectional Dijkstra with skewness
│   ├── data_structures/               # Priority queue implementations
│   │   ├── binary_heap.py
│   │   ├── fibonacci_heap.py
│   │   ├── radix_heap.py
│   │   └── pairing_heap.py (optional future)
│   └── utils/
│       ├── graph_generator.py         # Random directed graph generator (baseline version)
│       └── benchmark_dijkstra.py      # Runtime analysis script comparing heaps
│
├── unit_tests/
│   ├── test_binary_heap.py
│   ├── test_fibonacci_heap.py
│   ├── test_radix_heap.py
│   ├── test_graph_generator.py
│   └── test_dijkstra.py
│
├── latex/                              # Final report materials (plots, tex files)
│   └── plots/
│
├── requirements.txt
└── README.md
```

---

## ✅ Work Completed So Far

### ✅ 1. **Heaps and Priority Queues**
- Implemented **BinaryHeap**, **FibonacciHeap**, and **RadixHeap**.
- Added full unit test coverage for all three.
- Ensured all support: `insert`, `extract_min`, `decrease_key`, `is_empty`.

### ✅ 2. **Dijkstra’s Algorithm**
- Implemented standard Dijkstra with support for switching between the three heap types.
- Verified correctness with small deterministic graphs.
- Added unit tests for cross-heap correctness.

### ✅ 3. **Graph Generator**
- Added a baseline `graph_generator.py` for randomized graph creation.
- Tests for reproducibility, weight ranges, and no self-loops.

*(Note: generator is functional but simplistic — a more sophisticated or scalable generator may be needed for very large benchmarks.)*

### ✅ 4. **Runtime Benchmarking**
- Built an initial benchmarking pipeline comparing:
  - Binary Heap
  - Fibonacci Heap
  - Radix Heap
- Generates runtime plots and stores them in `latex/plots`.

---

## 🔜 Work To Be Done Next

### 🚧 1. Optimize Radix Heap
- Current implementation is correct but not fully optimized for large graphs.
- Needs improved bucket-bound recomputation and reduced overhead for redistributions.

### 🚧 2. Implement **Bidirectional Dijkstra with Skewness**
- Add forward & backward search.
- Incorporate skew factor for heuristic-based expansion imbalance.

### 🚧 3. Improve Graph Generation
- Current generator uses uniform random edges.
- For more realistic benchmarks, consider:
  - Degree-controlled graphs  
  - Scale-free graphs  
  - Grid or geometric random graphs  
  - Road-network-like sparse graphs  

### 🚧 4. Advanced Benchmarking
- Add:
  - Memory usage metrics
  - Operation counts (insert, decrease-key, extract-min)
  - Multiple weight distributions
  - Log-scale plots and CSV export

### 🚧 5. Final Report
- Compare theoretical complexities vs empirical results.
- Document performance differences between heaps.
- Include bidirectional + skewness evaluation.

---

## 📝 Notes

This README will continue evolving as the project progresses. Integrating optimized RadixHeap and implementing the bidirectional skewed version are the next major milestones.

