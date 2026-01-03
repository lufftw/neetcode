def list_to_doubly_linked(lst: list) -> 'DoublyListNode':
    """
    Convert Python list to Doubly Linked List.
    
    Args:
        lst: List of values
        
    Returns:
        Head of the doubly linked list
    """
    if not lst:
        return None
    
    head = DoublyListNode(lst[0])
    current = head
    
    for val in lst[1:]:
        new_node = DoublyListNode(val)
        current.next = new_node
        new_node.prev = current
        current = new_node
    
    return head

