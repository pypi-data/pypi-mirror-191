from .node import Node

import math


class Tree:
    """
    A group of connected nodes which form a tree structure. For each root node
    in a given ``.swc`` file, there will be one ``Tree``.

    :param nodes:
        a ``dict`` mapping a unique ID to each ``Node`` in the ``Tree``
    """

    def __init__(self, nodes: dict[int, Node]):
        self.nodes = nodes

    def total_length(self):
        """
        Calculates and returns the sum of the Euclidean distances between each
        pair of connected nodes.

        :return:
            the sum of the distances between each pair of connected nodes
        """

        total_length = 0.0
        for node in self.nodes.values():
            if node.parent_id == -1:
                continue
            parent = self.nodes[node.parent_id]
            node_position = [node.x, node.y, node.z]
            parent_position = [parent.x, parent.y, parent.z]
            total_length += math.dist(node_position, parent_position)
        return total_length
