from .tree import Tree


class SWC:
    r"""
    A representation of the ``.swc`` file, which can contain one or more
    tree-like structures (``Tree``\s), each containing some number of connected
    ``Node``\s.

    :param trees:
        a ``list`` of the ``Tree``\s belonging to this ``SWC``
    """

    def __init__(self, trees: list[Tree]):
        self.trees = trees

    def total_length(self):
        """
        Calculates and returns the sum of the Euclidean distances between each
        pair of connected nodes in each of the trees owned by this ``SWC``.

        :return:
            the sum of the distances between each pair of connected nodes in
            each tree
        """

        total_length = 0.0
        for tree in self.trees:
            total_length += tree.total_length()
        return total_length

    def condense_node_ids(self):
        r"""
        Modifies the IDs of the ``Node``\s contained by this ``SWC`` such that
        they form a contiguous series of natural numbers beginning at 1. The
        IDs will be contiguous for each tree, such that the least ID in the
        second tree will always be greater than the greatest ID in the first
        tree.
        """

        next_id = 1
        for tree in self.trees:
            new_nodes = {}
            for id in tree.nodes:
                new_nodes[next_id] = tree.nodes[id]
                next_id = next_id + 1
            tree.nodes = new_nodes
