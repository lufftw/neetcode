def graph_to_adjacency(node: 'Node') -> list:
    """
    Convert graph nodes to adjacency list.
    
    Args:
        node: Starting node of the graph
        
    Returns:
        Adjacency list representation
    """
    if not node:
        return []
    
    visited = {}
    queue = [node]
    
    while queue:
        curr = queue.pop(0)
        if curr.val in visited:
            continue
        visited[curr.val] = curr
        for neighbor in curr.neighbors:
            if neighbor.val not in visited:
                queue.append(neighbor)
    
    result = [[] for _ in range(len(visited))]
    for val, n in visited.items():
        result[val - 1] = [neighbor.val for neighbor in n.neighbors]
    
    return result

