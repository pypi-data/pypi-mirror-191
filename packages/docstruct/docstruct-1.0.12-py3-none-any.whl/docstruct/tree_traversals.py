from typing import Generator, Optional
from abc import ABC


class Node(ABC):
    def __init__(self):
        self.children = []


def pre_order_traversal(root: Optional[Node]) -> Generator:
    """
    Pre-order traversal is a depth-first traversal where the root is visited first, then the children.
    """
    if root is None:
        return
    yield root
    for child in root.children:
        yield from pre_order_traversal(child)


def post_order_traversal(root: Optional[Node]) -> Generator:
    """
    Post-order traversal is a depth-first traversal where the root is visited last, after the children.
    """
    if root is None:
        return
    for child in root.children:
        yield from post_order_traversal(child)

    yield root
