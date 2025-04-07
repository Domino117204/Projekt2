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

    #export i save_to_tex nie dzialaja
    
    def export(self, node):
        if not node.left and not node.right:
            return f"node{node.key}"
        l_str = f"child{self.export(node.left)}" if node.left else "child[missing]"
        r_str = f"child{self.export(node.right)}" if node.right else "child[missing]"
        return f"node{node.key}{{{l_str}}}{{{r_str}}}"

def save_to_tex(tree, filename="tree.tex"):
    with open(filename, "w", encoding="utf-8") as f:
        f.write("\\documentclass{article}\n")
        f.write("\\usepackage{tikz}\n")
        f.write("\\usetikzlibrary{trees}\n")
        f.write("\\begin{document}\n\n")

        f.write("\\begin{tikzpicture}[\n")
        f.write("  grow=down,\n")
        f.write("  level distance=1.5cm,\n")
        f.write("  sibling distance=2.5cm,\n")
        f.write("  every node/.style={circle, draw, minimum size=7mm, inner sep=2pt},\n")
        f.write("  edge from parent/.style={draw, -latex}\n")
        f.write("]\n")

        f.write(tree.export(tree.root) + ";\n")

        f.write("\\end{tikzpicture}\n\n")
        f.write("\\end{document}\n")
    print(f"Tree exported to {filename}")

def print_menu():
    print("Help       Show this message")
    print("Print      Print the tree using In-order, Pre-order, Post-order")
    #print("Remove     Remove elements of the tree")
    #print("Delete     Delete whole tree")
    #print("Export     Export the tree to tikzpicture")
    #print("Rebalance  Rebalance the tree")
    print("Exit       Exits the program (same as Ctrl+D)")
    print()


def main():
    tree = BST()

    values = input("Enter space-separated integers to initialize the tree: ")
    try:
        for key in map(int, values.split()):
            tree.insert(key)
    except ValueError:
        print("Invalid input. Please enter only integers.")
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

            #Zapisywanie do latex poprzez tickzpicture ale cos nie dziala
            #nwm czy to cos z funkcja nie tak czy tutaj
            #trzeba popatrzec
            #if tree.root:
            #    print("\\begin{tikzpicture}")
            #    print(tree.export(tree.root) + ";")
            #    print("\\end{tikzpicture}")
        #
            #    filename = input("Enter filename (default: tree.tex): ").strip()
            #    if not filename:
            #        filename = "tree.tex"
            #    save_to_tex(tree, filename)
            #else:
            #    print("Tree is empty. Nothing to export.")



        #elif action == "remove":
        #
#
        #elif action == "delete":
        #
#
        #elif action == "export":
        #    if tree.root:
        #        print(f"\\{export(tree.root)}")
        #    else:
        #        print("Tree is empty. Nothing to export.")
#
        #elif action == "rebalance":
        #    
#
        #elif action == "exit":
        #    
#
        #else:
        #    print("Unknown action. Type 'Help' to see options.\n")


if __name__ == "__main__":
    main()