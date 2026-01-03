def adjacency_to_graph(adjacency: list) -> 'Node':
    """
    Convert adjacency list to graph nodes.
    
    Args:
        adjacency: List of neighbor indices for each node
                   e.g., [[2,4],[1,3],[2,4],[1,3],[1,3]]
        
    Returns:
        First node of the graph (node with val=1)
    """
    if not adjacency:
        return None
    
    n = len(adjacency)
    nodes = [Node(i + 1) for i in range(n)]
    
    for i, neighbors in enumerate(adjacency):
        nodes[i].neighbors = [nodes[j - 1] for j in neighbors]
    
    return nodes[0]

