"""NodeGraph class template."""


class Node:
    """Graph node with neighbors list (e.g., Clone Graph)."""
    def __init__(self, val: int = 0, neighbors: list = None):
        self.val = val
        self.neighbors = neighbors if neighbors is not None else []

