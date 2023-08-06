class Node:
    """
    A single node in an SWC structure, which is represented by a single line in
    the ``.swc`` file.

    :param type:
        an enumeration describing the structure being represented by the node
    :param x:
        the ``x`` component of the node's 3D position
    :param y:
        the ``y`` component of the node's 3D position
    :param z:
        the ``z`` component of the node's 3D position
    :param radius:
        the radius of the sphere used to represent the volume of the node
    :param parent_id:
        the unique ID of another node that is the "parent"  of this node: a
        connected node that is one step closer to the root node of the tree
        (a root node has no parent, and will use a value ``-1`` for this field)
    """

    def __init__(self, type: int, x: float, y: float, z: float, radius: float,
                 parent_id: int):
        self.type = type
        self.x = x
        self.y = y
        self.z = z
        self.radius = radius
        self.parent_id = parent_id
