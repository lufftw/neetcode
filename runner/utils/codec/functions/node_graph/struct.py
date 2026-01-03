"""Tier-1: NodeGraph structure conversion functions."""

from typing import List, Optional
from ...classes.node_graph import NodeGraph


def adjacency_to_graph(adjacency: List[List[int]]) -> Optional[NodeGraph]:
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
    nodes = [NodeGraph(i + 1) for i in range(n)]
    
    for i, neighbors in enumerate(adjacency):
        nodes[i].neighbors = [nodes[j - 1] for j in neighbors]
    
    return nodes[0]


def graph_to_adjacency(node: Optional[NodeGraph]) -> List[List[int]]:
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
    
    result: List[List[int]] = [[] for _ in range(len(visited))]
    for val, n in visited.items():
        result[val - 1] = [neighbor.val for neighbor in n.neighbors]
    
    return result

