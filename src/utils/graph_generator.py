import random
from tqdm import tqdm

def generate_graph(num_nodes, num_edges, weight_range=(1, 10), seed=None, show_progress=True):
    """
    Generate a random directed graph.

    Parameters
    ----------
    num_nodes : int
        Number of nodes (vertices)
    num_edges : int
        Number of edges
    weight_range : tuple(int, int), optional
        Minimum and maximum weight for edges
    seed : int, optional
        Random seed for reproducibility
    show_progress : bool, optional
        Whether to display tqdm progress bar (default: True)

    Returns
    -------
    dict
        Graph represented as {node: [(neighbor, weight), ...]}
    """
    if seed is not None:
        random.seed(seed)

    graph = {i: [] for i in range(num_nodes)}

    iterator = range(num_edges)
    if show_progress:
        iterator = tqdm(iterator, total=num_edges, desc=f"Generating graph ({num_nodes} nodes)", ncols=80, leave=False)

    for _ in iterator:
        u = random.randint(0, num_nodes - 1)
        v = random.randint(0, num_nodes - 1)
        if u == v:
            continue  # skip self-loops
        w = random.randint(weight_range[0], weight_range[1])
        graph[u].append((v, w))

    return graph
