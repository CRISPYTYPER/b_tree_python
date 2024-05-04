class BTreeNode:
    def __init__(self, t, leaf=False):
        self.t = t
        self.leaf = leaf
        self.keys = []
        self.children = []

def init_b_tree(t):
    return BTreeNode(t, leaf=True)

def b_tree_insert(root, key):
    if len(root.keys) == 2 * root.t - 1:
        new_root = BTreeNode(root.t, leaf=False)
        new_root.children.append(root)
        b_tree_split_child(new_root, 0)
        b_tree_insert_nonfull(new_root, key)
        return new_root
    else:
        b_tree_insert_nonfull(root, key)
        return root

def b_tree_insert_nonfull(node, key):
    i = len(node.keys) - 1
    if node.leaf:
        node.keys.append(None)
        while i >= 0 and key < node.keys[i]:
            node.keys[i + 1] = node.keys[i]
            i -= 1
        node.keys[i + 1] = key
    else:
        while i >= 0 and key < node.keys[i]:
            i -= 1
        i += 1
        if len(node.children[i].keys) == 2 * node.t - 1:
            b_tree_split_child(node, i)
            if key > node.keys[i]:
                i += 1
        b_tree_insert_nonfull(node.children[i], key)

def b_tree_split_child(parent, i):
    t = parent.t
    y = parent.children[i]
    z = BTreeNode(t, leaf=y.leaf)
    parent.keys.insert(i, y.keys[t-1])
    parent.children.insert(i+1, z)

    z.keys = y.keys[t:]
    y.keys = y.keys[:t-1]

    if not y.leaf:
        z.children = y.children[t:]
        y.children = y.children[:t]

def find_pred(node):
    while not node.leaf:
        node = node.children[-1]
    return node.keys[-1]

def find_succ(node):
    while not node.leaf:
        node = node.children[0]
    return node.keys[0]

def merge(parent, i):
    child1 = parent.children[i]
    child2 = parent.children[i+1]
    child1.keys.append(parent.keys[i])
    child1.keys.extend(child2.keys)
    if not child1.leaf:
        child1.children.extend(child2.children)
    parent.keys.pop(i)
    parent.children.pop(i+1)
    child1.n = len(child1.keys)

def fix_shortage(parent, i):
    if i != 0 and len(parent.children[i-1].keys) >= parent.t:
        borrow_from_left(parent, i)
    elif i < len(parent.keys) and len(parent.children[i+1].keys) >= parent.t:
        borrow_from_right(parent, i)
    else:
        merge(parent, i-1 if i == len(parent.keys) else i)

def borrow_from_left(parent, i):
    left_sibling = parent.children[i-1]
    current_child = parent.children[i]
    current_child.keys.insert(0, parent.keys[i-1])
    parent.keys[i-1] = left_sibling.keys.pop()
    if not current_child.leaf:
        current_child.children.insert(0, left_sibling.children.pop())

def borrow_from_right(parent, i):
    right_sibling = parent.children[i+1]
    current_child = parent.children[i]
    current_child.keys.append(parent.keys[i])
    parent.keys[i] = right_sibling.keys.pop(0)
    if not right_sibling.leaf:
        current_child.children.append(right_sibling.children.pop(0))

def b_tree_delete(root, key):
    if root is None:
        return None
    _b_tree_delete(root, key)
    if len(root.keys) == 0:
        if not root.leaf:
            root = root.children[0]
        else:
            root = None
    return root


def _b_tree_delete(node, key):
    i = 0
    while i < len(node.keys) and key > node.keys[i]:
        i += 1

    if i < len(node.keys) and node.keys[i] == key:
        if node.leaf:
            node.keys.pop(i)
        else:
            if len(node.children[i].keys) >= node.t:
                pred = find_pred(node.children[i])
                node.keys[i] = pred
                _b_tree_delete(node.children[i], pred)
            elif len(node.children[i + 1].keys) >= node.t:
                succ = find_succ(node.children[i + 1])
                node.keys[i] = succ
                _b_tree_delete(node.children[i + 1], succ)
            else:
                merge(node, i)
                _b_tree_delete(node.children[i], key)
    else:
        if node.leaf:
            return
        if len(node.children[i].keys) < node.t:
            fix_shortage(node, i)
        _b_tree_delete(node.children[i], key)

