import sys
import traceback


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
            return (x, i)
        elif x.is_leaf:
            return None
        else:
            return self.b_tree_search(x.children[i], k)



    def _b_tree_split_child(self, x, i):
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
        for j in range(self.t, 2 * self.t - 1):
            y.key_value_list.pop()
        if not y.is_leaf:
            z.children.extend(y.children[self.t: 2 * self.t])
            for j in range(self.t, 2 * self.t):
                y.children.pop()
        x.children.insert(i+1, z)
        x.key_value_list.insert(i, y.key_value_list[self.t - 1])
        y.key_value_list.pop()


    def b_tree_insert(self, k, v):
        """
        Insert a key k and value v into the B-tree in a single pass down the tree.
        The b_tree_insert procedure uses _b_tree_split_child to guarantee that the recursion never descends to a full node.
        :param k: A key to insert.
        :param v: A value to insert.
        :return: None. This function performs its operation without returning a value.
        """
        r = self.root
        if len(self.root.key_value_list) == 2 * self.t - 1:
            s = BTreeNode([], [], False)
            self.root = s
            s.children.insert(0, r)
            self._b_tree_split_child(s, 0)
            self._b_tree_insert_nonfull(s, k, v)
        else:
            self._b_tree_insert_nonfull(r, k, v)

    def _b_tree_insert_nonfull(self, x, k, v):
        """
        Insert key k and value v into the tree rooted at the nonfull root node.
        _b_tree_insert_nonfull recurses as necessary down the tree, at all times guaranteeing
        that the node to which it recurses is not full by calling _b_tree_split_child as necessary.

        :param x: A node to insert.
        :param k: A key to insert into node x.
        :param v: A value to insert into node x.
        :return: None. This function performs its operation without returning a value.
        """
        i = len(x.key_value_list) - 1
        if x.is_leaf:
            x.key_value_list.append((None, None))
            while i >= 0 and k < x.key_value_list[i][0]:
                x.key_value_list[i + 1] = x.key_value_list[i]
                i = i - 1
            x.key_value_list[i + 1] = (k, v)
        else:
            while i >= 0 and k < x.key_value_list[i][0]:
                i = i - 1
            i = i + 1
            if len(x.children[i].key_value_list) == 2 * self.t - 1:
                self._b_tree_split_child(x, i)
                if k > x.key_value_list[i][0]:
                    i = i + 1

            self._b_tree_insert_nonfull(x.children[i], k, v)

    def _pred(self, x):
        """
        Find the data having the biggest key in the subtree where root is x. (Moving to the left child is already implemented)
        Then, return the key and value of the found node
        :param x: root node of the subtree.
        :return: key and value of the found node
        """
        while not x.is_leaf:
            x = x.children[-1]
        return x.key_value_list[-1]

    def _succ(self, x):
        """
        Find the data having the smallest key in the subtree where root is x. (Moving to the right child is already implemented)
        Then, return the key and value of the found node
        :param x: root node of the subtree.
        :return: key and value of the found node
        """
        while not x.is_leaf:
            x = x.children[0]
        return x.key_value_list[0]

    def _merge(self, x, i):
        """
        Merge children nodes x.children[i] and x.children[i + 1] along with node x.key_value_list[i]
        :param x: A parent node of the subtree.
        :param i: Index of the node to merge.
        :return: None. This function performs its operation without returning a value.
        """
        if len(x.children) == 2 and x == self.root:
            left_children = x.children[0]
            right_children = x.children[1]
            root_node = x.key_value_list[0]

            left_children.key_value_list.append(root_node)
            left_children.key_value_list.extend(right_children.key_value_list)
            if not left_children.is_leaf:
                left_children.children.extend(right_children.children)
            self.root = left_children
        else:
            left_children = x.children[i]
            right_children = x.children[i + 1]
            mid_node = x.key_value_list.pop(i)
            left_children.key_value_list.append(mid_node)
            left_children.key_value_list.extend(right_children.key_value_list)
            if not left_children.is_leaf:
                left_children.children.extend(right_children.children)

            x.children.pop(i+1)  # remove the right children from the parent x
    def _borrow_from_left(self, parent, i):
        """
        Borrow from the left sibling (not from the parent's perspective)
        :param parent: Parent node of the node "me"
        :param i: Index of the child node that borrows from the left sibling
        :return: None. This function performs its operation without returning a value.
        """
        left_sibling = parent.children[i-1]  # not parent's sibling
        me = parent.children[i]  # node which needs to borrow from the left_sibling
        me.key_value_list.insert(0, parent.key_value_list[i-1])  # take parent's data
        parent.key_value_list[i-1] = left_sibling.key_value_list.pop()  # swap parent's data with the left sibling's biggest data
        if not me.is_leaf:
            me.children.insert(0, left_sibling.children.pop())

    def _borrow_from_right(self, parent, i):
        """
        Borrow from the right sibling (not from the parent's perspective)
        :param parent: Parent node of the node "me"
        :param i: Index of the child node("me") that borrows from the right sibling
        :return: None. This function performs its operation without returning a value.
        """
        right_sibling = parent.children[i+1]  # not parent's sibling
        me = parent.children[i]  # node which needs to borrow from the right_sibling
        me.key_value_list.append(parent.key_value_list[i])  # take parent's data
        parent.key_value_list[i] = right_sibling.key_value_list.pop(0)  # swap parent's data with the right sibling's smallest data
        if not me.is_leaf:
            me.children.append(right_sibling.children.pop(0))
    def _fix_shortage(self, x, i):
        """
        Reshape (fix shortage) if the number of data is below t-1 after deleting
        :param x: parent node
        :param i: index of the child node to fix
        :return: changed i value
        """
        if i < len(x.key_value_list) and len(x.children[i+1].key_value_list) >= self.t:
            self._borrow_from_right(x, i)
        elif i > 0 and len(x.children[i-1].key_value_list) >= self.t:
            self._borrow_from_left(x, i)
        else:
            if i == len(x.key_value_list):  # if the child to deal with is the right-most one
                self._merge(x, i-1)
                return i-1
            else:
                self._merge(x, i)
        return i

    def b_tree_delete(self, k):
        """
        Delete a key k and the corresponding value v from the B-tree.

        :param k: A key to delete.
        :return: None. This function performs its operation without returning a value.
        """
        if self.root is None:
            return None
        self._b_tree_delete(self.root, k)
        if len(self.root.key_value_list) == 0:
            if not self.root.is_leaf:
                """
                Consider a B-tree where the root node has a single key and two children. 
                If the only key in the root is deleted, and it was the median that allowed for merging its two children into one, 
                the root would be left with no keys
                """
                self.root = self.root.children[0]
        return

    def _b_tree_delete(self, x, k):
        """
        Helper function to delete a key k and the corresponding value v from the B-tree.

        :param x: A root of the subtree.
        :param k: A key to delete.
        :return: None. This function performs its operation without returning a value.
        """

        i = 0
        while i < len(x.key_value_list) and k > x.key_value_list[i][0]:
            i += 1
        if i < len(x.key_value_list) and x.key_value_list[i][0] == k:  # found a key to delete
            if x.is_leaf:
                x.key_value_list.pop(i)
            else:  # if x is not a leaf
                v = x.key_value_list[i][1]
                if len(x.children[i].key_value_list) >= self.t:
                    node_pred = self._pred(x.children[i])
                    x.key_value_list[i] = node_pred
                    # logically, the target node to delete is swapped with the predecessor
                    self._b_tree_delete(x.children[i], node_pred[0])
                elif len(x.children[i+1].key_value_list) >= self.t:
                    node_pred = self._succ(x.children[i+1])
                    x.key_value_list[i] = node_pred
                    self._b_tree_delete(x.children[i+1], node_pred[0])
                else:
                    self._merge(x, i)
                    self._b_tree_delete(x.children[i], k)
        else:  # if target key is not in the current node
            if x.is_leaf:  # if not found until leaf
                return
            if len(x.children[i].key_value_list) < self.t:
                i = self._fix_shortage(x, i)
            self._b_tree_delete(x.children[i], k)

    def print_tree(self, node, l=0):
        print("Level ", l, " ", end=":")
        for i in node.key_value_list:
            print(i, end=" ")
        print()
        l += 1
        if len(node.children) > 0:
            for i in node.children:
                self.print_tree(i, l)


class UserInterface:
    @classmethod
    def main(cls):
        while True:
            print("Select the number to run each operation")
            print("1. Insertion")
            print("2. Deletion")
            print("3. Quit")
            input_num = int(input())
            if input_num == 1:
                cls._insertion()
            elif input_num == 2:
                cls._deletion()
            elif input_num == 3:
                break
            else:
                print("Invalid input!")

    @classmethod
    def _get_new_file_name(cls, file_name):
        parts = file_name.rsplit('.', 1)

        if len(parts) == 2:
            name, extension = parts
            modified_name = f"{name}_created.{extension}"
        else:
            # If there's no extension, just append '_created' to the filename
            modified_name = f"{file_name}_created"
        return modified_name

    @classmethod
    def _compare_two_files(cls, file1_path, file2_path):
        with open(file1_path, 'r') as file1, open(file2_path, 'r') as file2:
            for line1, line2 in zip(file1, file2):
                if line1.strip() != line2.strip():
                    return False
            return next(file1, None) is None and next(file2, None) is None




    @classmethod
    def _insertion(cls):
        while True:
            global insert_file_path
            insert_file_path = input("Please enter the file path for insertion, or type 'exit' to quit: \n")
            if insert_file_path.lower() == "exit":
                print("Exiting the program.")
                sys.exit(0)
            try:
                with open(insert_file_path, 'r') as file:
                    for line in file:
                        key_val = line.strip().split('\t')
                        key = int(key_val[0])
                        value = int(key_val[1])
                        b_tree.b_tree_insert(key, value)
                        print(f"inserted ({key}, {value})")
                        # b_tree.print_tree(b_tree.root)
                        # input()

                    file.seek(0)
                    modified_file_name = cls._get_new_file_name(insert_file_path)
                    with open(modified_file_name, 'w') as file_to_write:
                        for line in file:
                            key_val = line.strip().split('\t')
                            key = int(key_val[0])
                            result = b_tree.b_tree_search(b_tree.root, key)
                            if result is not None:
                                x, i = result
                                file_to_write.write(f"{x.key_value_list[i][0]}\t{x.key_value_list[i][1]}\n")
                                print(f"(key: {x.key_value_list[i][0]}, value: {x.key_value_list[i][1]}) found!")                                # input()
                            else:
                                print(f"key: {key} not found.")
                                # b_tree.print_tree(b_tree.root)
                                # input()
                print()
                if cls._compare_two_files(insert_file_path, modified_file_name):
                    print("Created file is the same as the original file!\n")
                else:
                    print("Created file is different from the original file!\n")
                print()
                break

            except FileNotFoundError:
                print(f"The file '{insert_file_path}' was not found. Please try again.")
                continue
            except PermissionError:
                print(f"Permission denied: unable to read file '{insert_file_path}'. Please try again.")
                continue
            except Exception as e:
                traceback.print_exc()
                print(f"An error occurred: {e}. Please try again.")
                continue

    @classmethod
    def _deletion(cls):
        while True:
            delete_file_path = input("Please enter the file path for deletion, or type 'exit' to quit: \n")
            delete_compare_file_path = input("Please enter the file path for comparison, or type 'exit' to quit: \n")
            if delete_file_path.lower() == "exit":
                print("Exiting the program.")
                sys.exit(0)
            try:
                with open(delete_file_path, 'r') as file:
                    for line in file:
                        key_val = line.strip().split('\t')
                        key = int(key_val[0])
                        value = int(key_val[1])
                        b_tree.b_tree_delete(key)
                        print(f"deleted ({key}, {value})")
                        # b_tree.print_tree(b_tree.root)
                        # input()
                with open(insert_file_path, 'r') as file:
                    modified_file_name = cls._get_new_file_name(delete_file_path)
                    with open(modified_file_name, 'w') as file_to_write:
                        for line in file:
                            key_val = line.strip().split('\t')
                            key = int(key_val[0])
                            result = b_tree.b_tree_search(b_tree.root, key)
                            if result is not None:
                                x, i = result
                                file_to_write.write(f"{x.key_value_list[i][0]}\t{x.key_value_list[i][1]}\n")
                                print(
                                    f"(key: {x.key_value_list[i][0]}, value: {x.key_value_list[i][1]}) found!")  # input()
                            else:
                                file_to_write.write(f"{key}\tN/A\n")
                                print(f"key: {key} not found.")
                                # b_tree.print_tree(b_tree.root)
                                # input()
                print()
                if cls._compare_two_files(delete_compare_file_path, modified_file_name):
                    print("Created file is the same as the original file!\n")
                else:
                    print("Created file is different from the original file!\n")
                print()
                break

            except FileNotFoundError:
                print(f"The file '{delete_file_path}' was not found. Please try again.")
                continue
            except PermissionError:
                print(f"Permission denied: unable to read file '{delete_file_path}'. Please try again.")
                continue
            except Exception as e:
                traceback.print_exc()
                print(f"An error occurred: {e}. Please try again.")
                continue

def main():
    global b_tree
    b_tree = BTree(3)  # t = 3, order = 6

    UserInterface.main()
    sys.exit(0)


if __name__ == "__main__":
    main()
