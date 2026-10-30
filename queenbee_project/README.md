# QueenBee Project

## Dijkstra Algorithm Implementation

This project implements Dijkstra's algorithm for finding the shortest path from a single source for emergency response coordination in the QueenBee beehive monitoring system.

### Features
- Min-Heap implementation from scratch
- REST API endpoint for path calculation
- Benchmarking against naive O(n²) implementation
- Unit tests for normal and edge cases
- PDF report generation for submission

### Project Structure
```text
queenbee_project/
├── src/
│   ├── __init__.py
│   ├── dijkstra.py
│   ├── api.py
│   └── benchmark.py
├── tests/
│   ├── test_dijkstra.py
│   └── test_api.py
├── docs/
│   └── README.md
├── config/
│   └── settings.py
└── README.md
```

### Getting Started
```bash
python -m src.dijkstra --help
```