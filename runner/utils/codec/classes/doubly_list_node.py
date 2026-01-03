"""DoublyListNode class definition (for problems like LC 430, 146)."""


class DoublyListNode:
    """Doubly linked list node."""
    def __init__(self, val: int = 0, prev: 'DoublyListNode' = None, next: 'DoublyListNode' = None):
        self.val = val
        self.prev = prev
        self.next = next
    
    def __repr__(self) -> str:
        return f"DoublyListNode({self.val})"

