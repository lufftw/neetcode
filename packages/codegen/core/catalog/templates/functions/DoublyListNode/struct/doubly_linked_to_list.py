def doubly_linked_to_list(head: 'DoublyListNode') -> list:
    """
    Convert Doubly Linked List to Python list.
    
    Args:
        head: Head of the doubly linked list
        
    Returns:
        List of values
    """
    result = []
    current = head
    while current:
        result.append(current.val)
        current = current.next
    return result

