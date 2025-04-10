class BSTNode:
    def __init__(self, key):
        self.key = key
        self.left = None
        self.right = None


class BST:
    def __init__(self):
        self.root = None

    def insert(self, key):
        self.root = self._insert(self.root, key)

    def _insert(self, node, key):
        if not node:
            return BSTNode(key)
        if key < node.key:
            node.left = self._insert(node.left, key)
        elif key > node.key:
            node.right = self._insert(node.right, key)
        return node

    def inorder(self):
        return self._inorder(self.root)

    def _inorder(self, node):
        return self._inorder(node.left) + [node.key] + self._inorder(node.right) if node else []

    def preorder(self):
        return self._preorder(self.root)

    def _preorder(self, node):
        return [node.key] + self._preorder(node.left) + self._preorder(node.right) if node else []

    def postorder(self):
        return self._postorder(self.root)

    def _postorder(self, node):
        return self._postorder(node.left) + self._postorder(node.right) + [node.key] if node else []
    
    def find_min(self):
        node = self.root
        if not node:
            return None
        while node.left:
            node = node.left
        return node.key

    def find_max(self):
        node = self.root
        if not node:
            return None
        while node.right:
            node = node.right
        return node.key
    
    def remove(self, key):
        self.root = self._remove(self.root, key)

    def _remove(self, node, key):
        if not node:
            return None
        if key < node.key:
            node.left = self._remove(node.left, key)
        elif key > node.key:
            node.right = self._remove(node.right, key)
        else:
            #a) liść
            if not node.left and not node.right:
                return None
            #b) jeden potomek
            if not node.left:
                return node.right
            if not node.right:
                return node.left
            #c) dwóch potomków
            successor = self._find_min_node(node.right)
            node.key = successor.key
            node.right = self._remove(node.right, successor.key)
        return node

    def _find_min_node(self, node):
        while node.left:
            node = node.left
        return node

    def delete(self):
        self._delete(self.root)
        self.root = None

    def _delete(self, node):
        if not node:
            return
        self._delete(node.left)
        self._delete(node.right)
        print(f"Deleting: {node.key}")
    
    def rebalance(self):
        # Tworzenie pseudo-korzenia
        pseudo_root = BSTNode(None)
        pseudo_root.right = self.root
        tail = pseudo_root
        rest = tail.right

        # Spłaszczanie drzewa
        while rest:
            if rest.left:
                temp = rest.left
                rest.left = temp.right
                temp.right = rest
                rest = temp
                tail.right = temp
            else:
                tail = rest
                rest = rest.right

        # Kompresowanie drzewa
        n = 0
        tmp = pseudo_root.right
        while tmp:
            n += 1
            tmp = tmp.right

        m = 2 ** (n.bit_length() - 1) - 1
        self._compress(pseudo_root, n - m)

        m //= 2
        while m > 0:
            self._compress(pseudo_root, m)
            m //= 2

        self.root = pseudo_root.right
        print("Tree rebalanced using DSW algorithm.")

    def _compress(self, root, count):
        scanner = root
        for i in range(count):
            child = scanner.right
            if not child:
                break
            grandchild = child.right
            if not grandchild:
                break
            scanner.right = grandchild
            child.right = grandchild.left
            grandchild.left = child
            scanner = scanner.right

    def export(self, node, indent=" ", is_first_node=True):
        if not node:
            return ""

        result = f"{indent}\\node {{{node.key}}}" if is_first_node else f"{indent}node {{{node.key}}}"

        if node.left and node.right:
            result += "\n" + indent + "    child { " + self.export(node.left, indent, False) + " }"
            result += "\n" + indent + "    child { " + self.export(node.right, indent, False) + " }"
        elif node.left:
            result += "\n" + indent + "    child { " + self.export(node.left, indent, False) + " }"
            result += "\n" + indent + "    child [missing]"
        elif node.right:
            result += "\n" + indent + "    child [missing]"
            result += "\n" + indent + "    child { " + self.export(node.right, indent + "", False) + " }"

        return result


    def save_to_tex(self, filename="tree.tex"):
        with open(filename, "w", encoding="utf-8") as f:
            f.write("\\documentclass{article}\n")
            f.write("\\usepackage{tikz}\n")
            f.write("\\usetikzlibrary{trees}\n\n")
            f.write("\\begin{document}\n\n")
            f.write("    \\begin{tikzpicture}[\n")
            f.write("        grow=down,\n")
            f.write("        level 1/.style = {sibling distance=4cm},")
            f.write("        level 2/.style = {sibling distance=2cm},")
            f.write("        level 3/.style = {sibling distance=1cm},")
            f.write("        level 4/.style = {sibling distance=0.5cm},")
            f.write("        level distance=1.5cm,\n")
            f.write("        every node/.style={circle, draw, minimum size=7mm, inner sep=2pt},\n")
            f.write("        edge from parent/.style={draw, -latex}\n")
            f.write("    ]\n")

            # Eksport drzewa
            tree_structure = self.export(self.root)
            if tree_structure:
                f.write(tree_structure + ";\n")
            else:
                f.write("        \\node {Empty Tree};\n")

            f.write("    \\end{tikzpicture}\n\n")
            f.write("\\end{document}\n")

        print(f"Export to {filename}")


class AVLNode:
    def __init__(self, key):
        self.key = key
        self.height = 1
        self.left = None
        self.right = None


class AVL:
    def __init__(self):
        self.root = None

    def build_from_sorted(self, values):
        def build(vals):
            if not vals:
                return None
            mid = len(vals) // 2 # mediana
            node = AVLNode(vals[mid])
            node.left = build(vals[:mid])
            node.right = build(vals[mid+1:])
            node.height = 1 + max(self.get_height(node.left), self.get_height(node.right))
            return node
        self.root = build(values)

    def get_height(self, node):
        return node.height if node else 0

    def get_balance(self, node):
        return self.get_height(node.left) - self.get_height(node.right) if node else 0

    def update_height(self, node):
        node.height = 1 + max(self.get_height(node.left), self.get_height(node.right))

    def rotate_right(self, y):
        x = y.left
        T2 = x.right
        x.right = y
        y.left = T2
        self.update_height(y)
        self.update_height(x)
        return x

    def rotate_left(self, x):
        y = x.right
        T2 = y.left
        y.left = x
        x.right = T2
        self.update_height(x)
        self.update_height(y)
        return y

    def insert(self, key):
        self.root = self._insert(self.root, key)

    def _insert(self, node, key):
        if not node:
            return AVLNode(key)
        if key < node.key:
            node.left = self._insert(node.left, key)
        elif key > node.key:
            node.right = self._insert(node.right, key)
        else:
            return node  # ignorujemy duplikaty

        self.update_height(node)
        balance = self.get_balance(node)

        if balance > 1 and key < node.left.key:
            return self.rotate_right(node)
        if balance < -1 and key > node.right.key:
            return self.rotate_left(node)
        if balance > 1 and key > node.left.key:
            node.left = self.rotate_left(node.left)
            return self.rotate_right(node)
        if balance < -1 and key < node.right.key:
            node.right = self.rotate_right(node.right)
            return self.rotate_left(node)

        return node

    def inorder(self):
        return self._inorder(self.root)

    def _inorder(self, node):
        return self._inorder(node.left) + [node.key] + self._inorder(node.right) if node else []

    def preorder(self):
        return self._preorder(self.root)

    def _preorder(self, node):
        return [node.key] + self._preorder(node.left) + self._preorder(node.right) if node else []

    def postorder(self):
        return self._postorder(self.root)

    def _postorder(self, node):
        return self._postorder(node.left) + self._postorder(node.right) + [node.key] if node else []

    def find_min(self):
        node = self.root
        if not node:
            return None
        while node.left:
            node = node.left
        return node.key

    def find_max(self):
        node = self.root
        if not node:
            return None
        while node.right:
            node = node.right
        return node.key

    def remove(self, key):
        self.root = self._remove(self.root, key)

    def _remove(self, node, key):
        if not node:
            return None
        if key < node.key:
            node.left = self._remove(node.left, key)
        elif key > node.key:
            node.right = self._remove(node.right, key)
        else:
            if not node.left:
                return node.right
            elif not node.right:
                return node.left
            temp = self._get_min_node(node.right)
            node.key = temp.key
            node.right = self._remove(node.right, temp.key)

        self.update_height(node)
        balance = self.get_balance(node)

        if balance > 1 and self.get_balance(node.left) >= 0:
            return self.rotate_right(node)
        if balance < -1 and self.get_balance(node.right) <= 0:
            return self.rotate_left(node)
        if balance > 1 and self.get_balance(node.left) < 0:
            node.left = self.rotate_left(node.left)
            return self.rotate_right(node)
        if balance < -1 and self.get_balance(node.right) > 0:
            node.right = self.rotate_right(node.right)
            return self.rotate_left(node)

        return node

    def _get_min_node(self, node):
        while node.left:
            node = node.left
        return node

    def delete(self):
        self._delete(self.root)
        self.root = None

    def _delete(self, node):
        if not node:
            return
        self._delete(node.left)
        self._delete(node.right)
        print(f"Deleting: {node.key}")
        
    def rebalance(self):
        pseudo_root = AVLNode(None)
        pseudo_root.right = self.root
        tail = pseudo_root
        rest = tail.right

        # Faza 1: Tworzenie "winoorośli" (vine)
        while rest:
            if rest.left:
                temp = rest.left
                rest.left = temp.right
                temp.right = rest
                rest = temp
                tail.right = temp
            else:
                tail = rest
                rest = rest.right

        # Faza 2: Kompresja winoorośli do zrównoważonego drzewa
        n = 0
        tmp = pseudo_root.right
        while tmp:
            n += 1
            tmp = tmp.right

        m = 2 ** (n.bit_length()) - 1
        self._compress(pseudo_root, n - m)

        m //= 2
        while m > 0:
            self._compress(pseudo_root, m)
            m //= 2

        self.root = pseudo_root.right
        print("Tree rebalanced using DSW algorithm.")

    def _compress(self, root, count):
        scanner = root
        for _ in range(count):
            child = scanner.right
            if child is None or child.right is None:
                break
            grandchild = child.right
            child.right = grandchild.left
            grandchild.left = child
            scanner.right = grandchild
            scanner = grandchild

    def export(self, node, indent=" ", is_first_node=True):
        if not node:
            return ""
        
        result = f"{indent}\\node {{{node.key}}}" if is_first_node else f"{indent}node {{{node.key}}}"

        if node.left and node.right:
            result += "\n" + indent + "    child { " + self.export(node.left, indent, False) + " }"
            result += "\n" + indent + "    child { " + self.export(node.right, indent, False) + " }"
        elif node.left:
            result += "\n" + indent + "    child { " + self.export(node.left, indent, False) + " }"
            result += "\n" + indent + "    child [missing]"
        elif node.right:
            result += "\n" + indent + "    child [missing]"
            result += "\n" + indent + "    child { " + self.export(node.right, indent + "", False) + " }"
        return result

    def save_to_tex(self, filename="avltree.tex"):
        with open(filename, "w", encoding="utf-8") as f:
            f.write("\\documentclass{article}\n")
            f.write("\\usepackage{tikz}\n")
            f.write("\\usetikzlibrary{trees}\n\n")
            f.write("\\begin{document}\n\n")
            f.write("    \\begin{tikzpicture}[\n")
            f.write("        grow=down,\n")
            f.write("        level 1/.style = {sibling distance=4cm},")
            f.write("        level 2/.style = {sibling distance=2cm},")
            f.write("        level 3/.style = {sibling distance=1cm},")
            f.write("        level 4/.style = {sibling distance=0.5cm},")
            f.write("        level distance=1.5cm,\n")
            f.write("        every node/.style={circle, draw, minimum size=7mm, inner sep=2pt},\n")
            f.write("        edge from parent/.style={draw, -latex}\n")
            f.write("    ]\n")
            tree_structure = self.export(self.root)
            if tree_structure:
                f.write(tree_structure + ";\n")
            else:
                f.write("        \\node {Empty Tree};\n")
            f.write("    \\end{tikzpicture}\n\n")
            f.write("\\end{document}\n")
        print(f"Export to {filename}")

def print_menu(tree_type):
    print()
    if tree_type=="bst":
        print("BST")
    elif tree_type=="avl":
        print("AVL")
    print("Help       Show this message")
    print("Print      Print the tree using In-order, Pre-order, Post-order")
    print("Min_Max    Print minimum and maximum value")
    print("Remove     Remove elements of the tree")
    print("Delete     Delete whole tree")
    print("Export     Export the tree to tikzpicture")
    print("Rebalance  Rebalance the tree")
    print("Exit       Exits the program (same as Ctrl+D)")
    print()

def load_from_file(tree, tree_type, filename):
    if tree_type=="bst":
        try:
            with open(filename, 'r') as file:
                values = file.read().strip().split()
                for key in map(int, values):
                    tree.insert(key)
            print(f"Values successfully loaded from {filename}")
        except FileNotFoundError:
            print(f"File {filename} not found.")
        except ValueError:
            print(f"Invalid data in file {filename}. Please ensure it contains integers.")
    
    elif tree_type=="avl":
        try:
            with open(filename, 'r') as file:
                values = list(map(int, file.read().strip().split()))
                tree.build_from_sorted(sorted(values))  # budowanie metodą połowienia
            print(f"Values successfully loaded from {filename}")
        except FileNotFoundError:
            print(f"File {filename} not found.")
        except ValueError:
            print(f"Invalid data in file {filename}. Please ensure it contains integers.")

def choose_tree():
    while True:
        tree_type = input("Which tree do you want to use? (BST/AVL): ").strip().lower()
        if tree_type == "avl":
            return AVL(), tree_type
        elif tree_type == "bst":
            return BST(), tree_type
        else:
            print("Invalid tree type. Please enter 'BST' or 'AVL'.")

def main():
    tree, tree_type = choose_tree()

    file_input = input("Do you want to load tree values from a file? (y/n): ").strip().lower()
    if file_input == 'y':
        filename = input("Enter the filename: ").strip()
        load_from_file(tree, tree_type, filename)
    else:
        values = input("Enter space separated integers to initialize the tree: ")
        values = (values.split())
        try:
            for key in map(int, values):
                tree.insert(key)
        except ValueError:
            print("Invalid input.")
            return

    print_menu(tree_type)

    while True:
        action = input("action> ").strip().lower()

        if action == "help":
            print_menu(tree_type)

        elif action == "print":
            print("In-order:  ", tree.inorder())
            print("Pre-order: ", tree.preorder())
            print("Post-order:", tree.postorder())

        elif action=="min_max":
            if tree.root:
                print("Minimum value:", tree.find_min())
                print("Maximum value:", tree.find_max())
            else:
                print("Tree is empty.")

        elif action == "remove":
            vals = input("remove> ")
            try:
                for val in map(int, vals.split()):
                    tree.remove(val)
                    print(f"remove {val}")
            except ValueError:
                print("Invalid input.")

        elif action == "delete":
            tree.delete()
            print("Tree succesfully removed")

        elif action == "export":
            if tree.root:
                filename = input("Enter filename (default: tree.tex): ").strip()
                if not filename:
                    filename = "tree.tex"
                tree.save_to_tex(filename)
            else:
                print("Tree is empty. Nothing to export.")

        elif action == "rebalance":
            if tree.root:
                tree.rebalance()
            else:
                print("Tree is empty. Nothing to rebalance.")    
            
        elif action == "exit":
            break  

        else:
            print("Unknown action. Type 'Help' to see options.\n")


if __name__ == "__main__":
    main()