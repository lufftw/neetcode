def linkedlist_to_list(node: 'ListNode') -> list:
    """Convert LinkedList to Python list."""
    result = []
    while node:
        result.append(node.val)
        node = node.next
    return result
