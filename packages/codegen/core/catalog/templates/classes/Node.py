"""Node class template (random pointer variant)."""


class Node:
    """Linked list node with random pointer (e.g., Copy List with Random Pointer)."""
    def __init__(self, val: int = 0, next: 'Node' = None, random: 'Node' = None):
        self.val = val
        self.next = next
        self.random = random

