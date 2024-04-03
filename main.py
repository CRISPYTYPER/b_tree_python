class BTreeNode:
    def __init__(self, keys, children, is_leaf):
        self.keys = keys
        self.children = children
        self.is_leaf = is_leaf


class BTree:
    def __init__(self, t):
        """
        create an empty root node.

        :param t: The minimum degree of the B-tree. Every node other than the root must have at least t-1 keys.
                Every internal node other than the root thus has at least t children.
                Every node may contain at most 2t-1 keys. Therefore, internal node may have at most 2t children.

        """
        self.root = BTreeNode([], [], True)
        self.t = t

    def b_tree_search(self, x, k):
        """
        b_tree_search takes as input an object of root node x of a subtree
        and a key k to be searched for in that subtree.
        :param x: A root node of a subtree
        :param k: A key to be searched for
        :return: A tuple (node, index) where 'node' is the node containing the key 'k', and its index is 'i'. Returns None if 'k' is not found.
        """
        i = 0
        while i < len(x.keys) and k > x.keys[i]:
            i = i + 1
        if i < len(x.keys) and k == x.keys[i]:
            return x, i
        elif x.is_leaf:
            return None
        else:
            return self.b_tree_search(x.children[i], k)

    def b_tree_split_child(self, x, i):
        """
        The procedure splits the child(x.c[i]) in two and adjusts x so that it has an additional child.
        parent: x
        left-child: y
        right_child(new): z

        Node y originally has 2t children(2t - 1 keys) but is reduced to t children (t - 1 keys) by this operation.

        :param x: A non-full internal node x
        :param i: An index i such that x.c[i] is a full child of x.
        :return: None. This function performs its operation without returning a value.
        """
        y = x.children[i]
        z = BTreeNode([], [], y.is_leaf)
        z.keys.extend(y.keys[self.t: 2 * self.t - 1])
        if not y.is_leaf:
            z.children.extend(y.children[self.t: 2 * self.t])
        x.children.insert(i+1, z)
        x.keys.insert(i, y.keys[self.t])

    def b_tree_insert(self, k):
        r = self.root
        if len(self.root.keys) == 2 * self.t - 1:
            s = BTreeNode([], [], False)
            self.root = s
            s.children[0] = r
            self.b_tree_split_child(s, 0)
            self.b_tree_insert_nonfull(s, k)
        else:
            self.b_tree_insert_nonfull(r, k)

    # TODO: make b_tree_insert_nonfull()