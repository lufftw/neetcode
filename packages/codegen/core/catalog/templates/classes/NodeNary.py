"""NodeNary class template."""


class Node:
    """N-ary tree node (e.g., N-ary Tree Traversal)."""
    def __init__(self, val: int = None, children: list = None):
        self.val = val
        self.children = children if children is not None else []

