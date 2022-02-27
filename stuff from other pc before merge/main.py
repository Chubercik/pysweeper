from __future__ import annotations

from time import perf_counter

from datatypes import Graph


def main() -> None:
    start = perf_counter()
    graph = Graph(100, 100)
    graph.scatter_bombs()
    stop = perf_counter()
    print(graph.print_graph())
    print(f"Generated the graph in {stop - start:0.4f} seconds.")
    # It takes around 0.02s - 0.03s to generate
    # a 100x100 graph on my setup, which is acceptable.


if __name__ == "__main__":
    main()
