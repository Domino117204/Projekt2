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
        # Faza 1: Tworzenie winoorośli
        pseudo_root = BSTNode(None)
        pseudo_root.right = self.root
        tail = pseudo_root
        rest = tail.right

        # Spłaszczanie drzewa (right-only chain)
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

        # Faza 2: Kompresowanie winoorośli do drzewa
        n = 0
        tmp = pseudo_root.right
        while tmp:
            n += 1
            tmp = tmp.right

        m = 2 ** (n.bit_length()) - 1  # Najbliższa potęga 2 minus 1
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
            if not child:
                break
            grandchild = child.right
            scanner.right = grandchild
            child.right = grandchild.left if grandchild else None
            if grandchild:
                grandchild.left = child
            scanner = scanner.right



    #trzeba dodac aby 1 node mial \node bo wstawia bez i trzeba recznie dopisac a tak juz smiga
    #i czasami nachodza na siebie wartosci
    def export(self, node, indent=" "):
        if not node:
            return ""

        result = f"{indent}node {{{node.key}}}"

        # Obsługa dzieci w TikZ
        if node.left and node.right:
            result += "\n" + indent + "    child { " + self.export(node.left, indent) + " }"
            result += "\n" + indent + "    child { " + self.export(node.right, indent) + " }"
        elif node.left:
            result += "\n" + indent + "    child { " + self.export(node.left, indent) + " }"
            result += "\n" + indent + "    child [missing]"
        elif node.right:
            result += "\n" + indent + "    child [missing]"
            result += "\n" + indent + "    child { " + self.export(node.right, indent + "        ") + " }"

        return result



    def save_to_tex(self, filename="tree.tex"):
        with open(filename, "w", encoding="utf-8") as f:
            f.write("\\documentclass{article}\n")
            f.write("\\usepackage{tikz}\n")
            f.write("\\usetikzlibrary{trees}\n\n")
            f.write("\\begin{document}\n\n")
            f.write("    \\begin{tikzpicture}[\n")
            f.write("        grow=down,\n")
            f.write("        level distance=1.5cm,\n")
            f.write("        sibling distance=2.5cm,\n")
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

        print(f"Drzewo zostało wyeksportowane do pliku {filename}")

def print_menu():
    print("Help       Show this message")
    print("Print      Print the tree using In-order, Pre-order, Post-order")
    print("Min_Max    Print minimum and maximum value")
    print("Remove     Remove elements of the tree")
    print("Delete     Delete whole tree")
    print("Export     Export the tree to tikzpicture")
    print("Rebalance  Rebalance the tree")
    print("Exit       Exits the program (same as Ctrl+D)")
    print()


def main():
    tree = BST()

    values = input("Enter space separated integers to initialize the tree: ")
    try:
        for key in map(int, values.split()):
            tree.insert(key)
    except ValueError:
        print("Invalid input.")
        return

    print_menu()

    while True:
        action = input("action> ").strip().lower()

        if action == "help":
            print_menu()

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
                    print(f"remove {val} (if it existed).")
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