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

    def b_tree_search(self, k, x=None):
        """
        b_tree_search takes as input an object of root node x of a subtree
        and a key k to be searched for in that subtree.
        :param x: A root node of a subtree
        :param k: A key to be searched for
        :return: A tuple (node, index) where 'node' is the node containing the key 'k', and its index is 'i'. Returns None if 'k' is not found.
        """
        if x is not None:
            i = 0
            while i < len(x.key_value_list) and k > x.key_value_list[i][0]:
                i = i + 1
            if i < len(x.key_value_list) and k == x.key_value_list[i][0]:
                return (x, i)
            elif x.is_leaf:
                return None
            else:
                return self.b_tree_search(k, x.children[i])
        else:
            return self.b_tree_search(k, self.root)


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
        Insert a key k and v pair(tuple) into the B-tree in a single pass down the tree.
        The b_tree_insert procedure uses b_tree_split_child to guarantee that the recursion never descends to a full node.
        :param k: A key, value pair to insert.
        :return: None. This function performs its operation without returning a value.
        """
        r = self.root
        if len(self.root.key_value_list) == 2 * self.t - 1:
            s = BTreeNode([], [], False)
            self.root = s
            s.children.insert(0, r)
            self.b_tree_split_child(s, 0)
            self.b_tree_insert_nonfull(s, k, v)
        else:
            self.b_tree_insert_nonfull(r, k, v)

    def b_tree_insert_nonfull(self, x, k, v):
        """
        Insert key_value pair k(tuple) into the tree rooted at the nonfull root node.
        b_tree_insert_nonfull recurses as necessary down the tree, at all times guaranteeing
        that the node to which it recurses is not full by calling b_tree_split_child as necessary.

        :param x: A node to insert.
        :param k: A key, value pair to insert into node x.
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
                self.b_tree_split_child(x, i)
                if k > x.key_value_list[i][0]:
                    i = i + 1

            self.b_tree_insert_nonfull(x.children[i], k, v)

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
                # TODO: deletion()
                pass
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
                if line1 != line2:
                    return False
            return next(file1, None) is None and next(file2, None) is None




    @classmethod
    def _insertion(cls):
        while True:
            file_path = input("Please enter the file path, or type 'exit' to quit: \n")
            if file_path.lower() == "exit":
                print("Exiting the program.")
                sys.exit(0)
            try:
                with open(file_path, 'r') as file:
                    for line in file:
                        key_val = line.strip().split('\t')
                        key = int(key_val[0])
                        value = int(key_val[1])
                        b_tree.b_tree_insert(key, value)
                        print(f"inserted ({key}, {value})")
                        # b_tree.print_tree(b_tree.root)
                        # input()

                    file.seek(0)
                    modified_file_name = cls._get_new_file_name(file_path)
                    with open(modified_file_name, 'w') as file_to_write:
                        for line in file:
                            key_val = line.strip().split('\t')
                            key = int(key_val[0])
                            result = b_tree.b_tree_search(key, b_tree.root)
                            if result is not None:
                                x, i = result
                                file_to_write.write(f"{x.key_value_list[i][0]}\t{x.key_value_list[i][1]}\n")
                                print(f"{x.key_value_list[i][0]}\t{x.key_value_list[i][1]}")
                                # input()
                            else:
                                print(f"key: {key} not found.")
                                # b_tree.print_tree(b_tree.root)
                                # input()
                print()
                if cls._compare_two_files(file_path, modified_file_name):
                    print("Created file is the same as the original file!\n")
                else:
                    print("Created file is different from the original file!\n")
                print()
                break

            except FileNotFoundError:
                print(f"The file '{file_path}' was not found. Please try again.")
                continue
            except PermissionError:
                print(f"Permission denied: unable to read file '{file_path}'. Please try again.")
                continue
            except Exception as e:
                traceback.print_exc()
                print(f"An error occurred: {e}. Please try again.")
                continue


def main():
    global b_tree
    b_tree = BTree(2)  # t = 2, order = 4

    UserInterface.main()
    sys.exit(0)


if __name__ == "__main__":
    main()
