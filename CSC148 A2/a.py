"""
Read over the very-abbreviated LinkedListNode and LinkedList class declarations
below.  Then implement the body of delete_after (look for the TODO),
which must run with only the code below.

If you are writing this on paper, please provide your:

Name:

utorid:
"""
from typing import Union


class LinkedListNode:
    """
    Node to be used in linked list

    next_ - successor to this LinkedListNode
    value - data this LinkedListNode represents
    """
    next_: Union["LinkedListNode", None]
    value: object

    def __init__(self, value: object,
                 next_: Union["LinkedListNode", None]=None) -> None:
        """
        Create LinkedListNode self with data value and successor next_.
        """
        self.value, self.next_ = value, next_

    def __str__(self) -> str:
        """
        Return a user-friendly representation of this LinkedListNode.

        >>> n = LinkedListNode(5, LinkedListNode(7))
        >>> print(n)
        5 -> 7 ->|
        """
        s = "{} ->".format(self.value)
        current_node = self.next_
        while current_node is not None:
            s += " {} ->".format(current_node.value)
            current_node = current_node.next_
        return s + "|"


class LinkedList:
    """
    Collection of LinkedListNodes

    front - first node of this LinkedList
    size - number of nodes in this LinkedList, >= 0
    """
    front: Union[LinkedListNode, None]
    size: int

    def __init__(self) -> None:
        """
        Create an empty linked list.
        """
        self.front, self.size = None, 0

    def delete_after(self, value: object) -> None:
        """
        Remove the node following the first occurrence of value, if
        possible, otherwise leave self unchanged.

        >>> lnk = LinkedList()
        >>> lnk.front = LinkedListNode(3, None) # Insert in reverse
        >>> lnk.front = LinkedListNode(2, lnk.front)
        >>> lnk.front = LinkedListNode(1, lnk.front) # lnk.front has value 1 now
        >>> print(lnk.front) # note that lnk.front contains 1
        1 -> 2 -> 3 ->|
        >>> lnk.delete_after(2)
        >>> print(lnk.front)
        1 -> 2 ->|
        """

        curr = self.front
        i = 0
        while curr.next_ != None:
            if i == 0 and curr.value == value:
                curr.next_ = curr.next_.next_
                i += 1
                self.size -= 1
            curr = curr.next_
        # TODO: implement the body of this method.
        # You need not touch any other code than the body of this method
        # You need not add comments or docstrings.
        # You need not add any assertions or preconditions.


if __name__ == '__main__':
    """Optional: uncomment the lines import doctest and doctest.testmod() to 
    have your docstring examples run when you run cipher_functions.py
    NOTE: your docstrings MUST be properly formatted for this to work!
    """

    import doctest
    doctest.testmod()
