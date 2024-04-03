class BTreeNode:
    def __init__(self, key_value_list, children, is_leaf):
        """
        Initialize a BTreeNode.

        :param key_value_list: A list of tuples(key, value).
        :param children: A list of children(BTreeNode).
        :param is_leaf: A boolean value representing whether it is a leaf node.
        """
        self.key_value_list = key_value_list
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
        while i < len(x.key_value_list) and k > x.key_value_list[i][0]:
            i = i + 1
        if i < len(x.key_value_list) and k == x.key_value_list[i][0]:
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
        z.key_value_list.extend(y.key_value_list[self.t: 2 * self.t - 1])
        if not y.is_leaf:
            z.children.extend(y.children[self.t: 2 * self.t])
        x.children.insert(i + 1, z)
        x.key_value_list.insert(i, y.key_value_list[self.t])

    def b_tree_insert(self, k, v):
        """
        Insert a key k and v pair(tuple) into the B-tree in a single pass down the tree.
        The b_tree_insert procedure uses b_tree_split_child to guarantee that the recursion never descends to a full node.
        :param k: A key to insert.
        :param v: A value to insert.
        :return: None. This function performs its operation without returning a value.
        """
        r = self.root
        if len(self.root.key_value_list) == 2 * self.t - 1:
            s = BTreeNode([], [], False)
            self.root = s
            s.children[0] = r
            self.b_tree_split_child(s, 0)
            self.b_tree_insert_nonfull(s, k, v)
        else:
            self.b_tree_insert_nonfull(r, k, v)

    def b_tree_insert_nonfull(self, x, k, v):
        """
        Insert key k and v pair(tuple) into the tree rooted at the nonfull root node.
        b_tree_insert_nonfull recurses as necessary down the tree, at all times guaranteeing
        that the node to which it recurses is not full by calling b_tree_split_child as necessary.

        :param x: A node to insert.
        :param k: A key to insert into node x.
        :param v: A value to insert into node x.
        :return: None. This function performs its operation without returning a value.
        """
        i = len(x.key_value_list) - 1
        if x.is_leaf:
            while i >= 0 and k < x.key_value_list[i][0]:
                x.key_value_list[i + 1] = x.key_value_list[i]
                i = i - 1
            x.key_value_list[i + 1] = k, v
        else:
            while i >= 0 and k < x.key_value_list[i][0]:
                i = i - 1
            if len(x.children[i].key_value_list) == 2 * self.t - 1:
                self.b_tree_split_child(x, i)
                if k > x.key_value_list[i][0]:
                    i = i + 1
            self.b_tree_insert_nonfull(x.children[i], k, v)
