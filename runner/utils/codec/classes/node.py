"""Node class definition (for random pointer problems)."""


class Node:
    """Linked list node with random pointer (for Copy List with Random Pointer)."""
    def __init__(self, val: int = 0, next: 'Node' = None, random: 'Node' = None):
        self.val = val
        self.next = next
        self.random = random
    
    def __repr__(self) -> str:
        return f"Node({self.val})"

