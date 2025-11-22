import random
from tqdm import tqdm

def generate_er_graph(num_nodes, num_edges, weight_range=(1, 10), seed=None, show_progress=True):
    """
    Generate a random directed graph using Erdos-Renyi style.

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

def generate_ba_graph(num_nodes, m=3, weight_range=(1, 10), seed=None, show_progress=True):
    """
    Generate a directed, weighted graph using a Barabási–Albert-style preferential attachment model.

    Parameters
    ----------
    num_nodes : int
        Number of nodes (vertices). Must be >= m + 1.
    m : int
        Number of edges each new node creates to existing nodes (m >= 1).
    weight_range : tuple(int, int), optional
        Minimum and maximum weight for edges (inclusive).
    seed : int, optional
        Random seed for reproducibility.
    show_progress : bool, optional
        Whether to display tqdm progress bar.

    Returns
    -------
    dict
        Graph represented as {node: [(neighbor, weight), ...]}.
    """
    if num_nodes <= 0:
        return {}

    if seed is not None:
        random.seed(seed)

    if m < 1:
        raise ValueError("m must be at least 1")
    if num_nodes <= m:
        raise ValueError("num_nodes must be > m")

    # adjacency list
    graph = {i: [] for i in range(num_nodes)}

    # Start with a small seed network: a directed chain 0 -> 1 -> 2 -> ... -> m
    degrees = [0] * num_nodes  # track total degree (in+out) for preferential attachment
    for u in range(m):
        v = u + 1
        w = random.randint(weight_range[0], weight_range[1])
        graph[u].append((v, w))
        degrees[u] += 1  # out-degree
        degrees[v] += 1  # in-degree

    # List of existing nodes for convenience
    existing_nodes = list(range(m + 1))

    iterator = range(m + 1, num_nodes)
    if show_progress:
        iterator = tqdm(
            iterator,
            total=num_nodes - (m + 1),
            desc=f"Generating BA graph ({num_nodes} nodes)",
            ncols=80,
            leave=False,
        )

    for new_node in iterator:
        degree_sum = sum(degrees[i] for i in existing_nodes)

        # Pick exactly m distinct targets
        if degree_sum == 0:
            # fallback: uniform sampling without replacement
            k = min(m, len(existing_nodes))
            targets = random.sample(existing_nodes, k=k)
        else:
            targets = []
            chosen = set()
            # sample without replacement with probability ~ degree
            k = min(m, len(existing_nodes))
            while len(targets) < k:
                v = random.choices(
                    existing_nodes,
                    weights=[degrees[i] for i in existing_nodes],
                    k=1,
                )[0]
                if v not in chosen:
                    chosen.add(v)
                    targets.append(v)

        # Add directed edges new_node -> target
        for v in targets:
            w = random.randint(weight_range[0], weight_range[1])
            graph[new_node].append((v, w))
            degrees[new_node] += 1   # out-degree
            degrees[v] += 1          # in-degree

        existing_nodes.append(new_node)

    return graph