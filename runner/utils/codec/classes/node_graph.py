"""NodeGraph class definition (for graph clone problems like LC 133)."""


class NodeGraph:
    """Graph node with neighbors list."""
    def __init__(self, val: int = 0, neighbors: list = None):
        self.val = val
        self.neighbors = neighbors if neighbors is not None else []
    
    def __repr__(self) -> str:
        return f"NodeGraph({self.val})"

