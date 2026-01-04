"""NodeNary class definition (for N-ary tree problems like LC 429, 559)."""


class NodeNary:
    """N-ary tree node."""
    def __init__(self, val: int = None, children: list = None):
        self.val = val
        self.children = children if children is not None else []
    
    def __repr__(self) -> str:
        return f"NodeNary({self.val})"

