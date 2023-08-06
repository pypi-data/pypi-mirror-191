class Node:
    def __init__(self, index: int):
        self.index: int = index
        self.neighbors: list[Node] = []

    def add_neighbor(self, neighbor: "Node"):
        self.neighbors.append(neighbor)

    def __str__(self):
        return f"{self.__class__.__name__}(index = {self.index})"

    def __repr__(self):
        return str(self)


class Graph:
    def __init__(self, nodes: list[Node]):
        self.nodes = nodes

    def get_connected_components(
        self, nodes_order: list[Node] = None
    ) -> list[list[Node]]:
        if nodes_order is None:
            nodes_order = self.nodes
        visited = set()
        connected_components: list[list[Node]] = []
        for node in nodes_order:
            if node not in visited:
                connected_component = self.get_connected_component(node, visited)
                connected_components.append(connected_component)
        return connected_components

    def get_connected_component(self, node: Node, visited: set[Node]) -> list[Node]:
        stack = [node]
        connected_component = []
        while stack:
            current = stack.pop()
            if current not in visited:
                visited.add(current)
                connected_component.append(current)
                for neighbor in current.neighbors:
                    stack.append(neighbor)
        return connected_component
