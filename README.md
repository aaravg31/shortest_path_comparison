# Shortest Path Comparison

Cosc 520 Final Project - A comprehensive comparison of shortest path algorithms with a focus on performance analysis and algorithm variations.

## Overview

This project implements and compares various shortest path algorithms, including:

- **Bidirectional Dijkstra** - A two-way search algorithm that explores from both source and target simultaneously

## Project Structure

```
shortest_path_comparison/
├── src/
│   ├── algorithms/           # Shortest path algorithm implementations
│   │   ├── base.py          # Abstract base class for algorithms
│   │   └── bidirectional_dijkstra.py
│   ├── data_structures/     # Graph data structures
│   │   └── graph.py         # Graph class with adjacency list
│   └── utils/               # Utility functions
│       └── visualization.py # Text-based visualization helpers
├── tests/                   # Test suite
│   └── test_bidirectional_dijkstra.py
├── benchmarks/              # Performance benchmarking scripts (TBD)
├── requirements.txt         # Python dependencies
└── README.md

```

## Setup

1. Clone the repository:

```bash
git clone https://github.com/aaravg31/shortest_path_comparison.git
cd shortest_path_comparison
```

2. (Optional) Create a virtual environment:

```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install dependencies for testing and development:

```bash
pip install -r requirements.txt
```
