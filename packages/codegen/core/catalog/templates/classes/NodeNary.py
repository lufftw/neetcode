class Node:
    """N-ary tree node."""
    def __init__(self, val: int = None, children: list = None):
        self.val = val
        self.children = children if children is not None else []
