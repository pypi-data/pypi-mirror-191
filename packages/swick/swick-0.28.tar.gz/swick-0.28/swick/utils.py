from .node import Node
from .tree import Tree
from .swc import SWC


def split_swc(swc: SWC):
    """
    Splits an ``SWC`` object into one or more ``SWC`` objects, each containing
    a single tree. Node IDs are not modified by this process.

    :parameter swc:
        the ``SWC`` object to be split

    :return:
        a list of ``SWC`` objects each containing one tree
    """

    result = []
    for tree in swc.trees:
        result.append(SWC([tree]))
    return result


def combine_swcs(swcs: list[SWC]):
    r"""
    Combines each of the ``SWC`` objects in the list into a single ``SWC``.
    Node IDs for all but the first ``SWC`` in the list may be modified by
    this process in order to avoid collisions between node IDs: for each
    ``SWC`` in the list, the node IDs it contains will be offset by the
    greatest node ID in the previous ``SWC``.

    :parameter swcs:
        a list of ``SWC`` objects to be combined

    :return:
        a single ``SWC`` object containing all ``Tree``\s from the input
    """

    trees = []
    id_offset = 0
    highest_id = 0
    for swc in swcs:
        for tree in swc.trees:
            old_id_to_new_id = {}
            new_tree_nodes = {}

            # first pass to create mapping from old to new IDs
            for id in tree.nodes:
                new_id = id + id_offset
                old_id_to_new_id[id] = new_id
                if new_id > highest_id:
                    highest_id = new_id

            # second pass to create modified copies of existing nodes
            for id in tree.nodes:
                new_id = old_id_to_new_id[id]
                if tree.nodes[id].parent_id != -1:
                    new_parent_id = old_id_to_new_id[tree.nodes[id].parent_id]
                    tree.nodes[id].parent_id = new_parent_id
                new_tree_nodes[new_id] = tree.nodes[id]

            trees.append(Tree(new_tree_nodes))
        id_offset = highest_id
    result = SWC(trees)
    return result
