from ..text_block import Paragraph
import logging


def paragraph_comparator(first: Paragraph, second: Paragraph) -> int:
    """
    Returns 1 if the first paragraph is before the second paragraph.
    Returns -1 if the second paragraph is before the first paragraph.
    Returns 0 if there is no constraint.
    """
    first_bb = first.bounding_box
    second_bb = second.bounding_box

    "1 first < other. -1 first > other. 0 first intersect other."
    horizontal_relation = first_bb.get_horizontal_segment().relation(
        second_bb.get_horizontal_segment()
    )
    vertical_relation = -first_bb.get_vertical_segment().relation(
        second_bb.get_vertical_segment()
    )

    #! In case of intersection between the two paragraphs, there is no constraint between them.
    if horizontal_relation == 0 and vertical_relation == 0:
        return 0

    #! Temporary.
    if horizontal_relation == 1 and vertical_relation == -1:
        return 0

    #! Temporary.
    if horizontal_relation == -1 and vertical_relation == 1:
        return 0

    # At this point the horizontal and vertical agree up to intersection
    if abs(horizontal_relation) == 1:
        return horizontal_relation
    if abs(vertical_relation) == 1:
        return vertical_relation
    logging.error("Should not reach this line in the paragraph_comparator function")


def generate_paragraphs_graph(paragraphs: list[Paragraph]) -> list[list[int]]:
    """
    Returns the adjacency list of the paragraphs graph.
    There is a directed edge between first paragraph to second paragraph if the first paragraph is before the second paragraph.
    """
    num_nodes = len(paragraphs)
    adjacency_list = [[] for _ in range(num_nodes)]
    for i in range(num_nodes):
        for j in range(i + 1, num_nodes):
            relation = paragraph_comparator(paragraphs[i], paragraphs[j])
            if relation == 1:
                adjacency_list[i].append(j)
            elif relation == -1:
                adjacency_list[j].append(i)
    return adjacency_list


def topological_sort(adjacency_list: list[list[int]]) -> list[int]:
    num_nodes = len(adjacency_list)
    in_degree = [0 for _ in range(num_nodes)]
    for node in range(num_nodes):
        for neighbor in adjacency_list[node]:
            in_degree[neighbor] += 1
    queue = []
    for node in range(num_nodes):
        if in_degree[node] == 0:
            queue.append(node)
    sorted_nodes = []
    while queue:
        node = queue.pop(0)
        sorted_nodes.append(node)
        for neighbor in adjacency_list[node]:
            in_degree[neighbor] -= 1
            if in_degree[neighbor] == 0:
                queue.append(neighbor)
    return sorted_nodes


def sort_paragraphs(paragraphs: list[Paragraph]) -> list[Paragraph]:
    """
    Sorts the paragraphs according to their order in the page.
    """
    adjacency_list = generate_paragraphs_graph(paragraphs)
    sorted_nodes = topological_sort(adjacency_list)
    sorted_paragraphs = [paragraphs[i] for i in sorted_nodes]
    return sorted_paragraphs
