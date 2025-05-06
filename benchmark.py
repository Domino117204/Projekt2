import time
import os
import random

class BSTNode:
    def __init__(self, key):
        self.key = key
        self.left = None
        self.right = None

class BST:
    def __init__(self):
        self.root = None

    def insert(self, key):
        if not self.root:
            self.root = BSTNode(key)
        else:
            self._insert(self.root, key)

    def _insert(self, node, key):
        if key < node.key:
            if node.left:
                self._insert(node.left, key)
            else:
                node.left = BSTNode(key)
        else:
            if node.right:
                self._insert(node.right, key)
            else:
                node.right = BSTNode(key)

    def find_min(self):
        node = self.root
        while node.left:
            node = node.left
        return node.key

    def find_max(self):
        node = self.root
        while node.right:
            node = node.right
        return node.key

    def inorder(self):
        result = []
        self._inorder(self.root, result)
        return result

    def _inorder(self, node, result):
        if node:
            self._inorder(node.left, result)
            result.append(node.key)
            self._inorder(node.right, result)

    def balance(self):
        nodes = self.inorder()
        self.root = self._build_balanced(nodes)

    def _build_balanced(self, nodes):
        if not nodes:
            return None
        mid = len(nodes) // 2
        node = BSTNode(nodes[mid])
        node.left = self._build_balanced(nodes[:mid])
        node.right = self._build_balanced(nodes[mid+1:])
        return node


class AVLNode:
    def __init__(self, key):
        self.key = key
        self.left = None
        self.right = None
        self.height = 1

class AVL:
    def __init__(self):
        self.root = None

    def build_from_sorted(self, values):
        def build(l, r):
            if l > r:
                return None
            mid = (l + r) // 2
            node = AVLNode(values[mid])
            node.left = build(l, mid - 1)
            node.right = build(mid + 1, r)
            node.height = 1 + max(self.get_height(node.left), self.get_height(node.right))
            return node
        self.root = build(0, len(values) - 1)

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

    def find_min(self):
        node = self.root
        while node.left:
            node = node.left
        return node.key

    def find_max(self):
        node = self.root
        while node.right:
            node = node.right
        return node.key

    def inorder(self):
        result = []
        self._inorder(self.root, result)
        return result

    def _inorder(self, node, result):
        if node:
            self._inorder(node.left, result)
            result.append(node.key)
            self._inorder(node.right, result)

def benchmark(n, repeats=4):
    values = list(range(n))
    random.shuffle(values)

    bst_insert_times = []
    avl_build_times = []
    inorder_bst_times = []
    inorder_avl_times = []
    balance_bst_times = []
    minmax_bst_times = []
    minmax_avl_times = []

    for _ in range(repeats):
        bst = BST()
        sorted_values = sorted(values)

        t1 = time.perf_counter()
        for v in values:
            bst.insert(v)
        bst_insert_times.append(time.perf_counter() - t1)

        avl = AVL()
        t2 = time.perf_counter()
        avl.build_from_sorted(sorted_values)
        avl_build_times.append(time.perf_counter() - t2)

    bst = BST()
    for v in values:
        bst.insert(v)

    sorted_values = sorted(values)
    avl = AVL()
    avl.build_from_sorted(sorted_values)

    for _ in range(repeats):
        t1 = time.perf_counter() * 1000  
        bst.find_min()
        bst.find_max()
        t2 = time.perf_counter() * 1000
        minmax_bst_times.append((t2 - t1))

        t3 = time.perf_counter() * 1000
        avl.find_min()
        avl.find_max()
        t4 = time.perf_counter() * 1000
        minmax_avl_times.append((t4 - t3))

        t5 = time.perf_counter()
        bst.inorder()
        inorder_bst_times.append((time.perf_counter() - t5))

        t6 = time.perf_counter()
        avl.inorder()
        inorder_avl_times.append((time.perf_counter() - t6))

        t7 = time.perf_counter()
        bst.balance()
        balance_bst_times.append((time.perf_counter() - t7))

    return (
        sum(bst_insert_times) / repeats,
        sum(avl_build_times) / repeats,
        sum(minmax_bst_times) / repeats,  
        sum(minmax_avl_times) / repeats,  
        sum(inorder_bst_times) / repeats,  
        sum(inorder_avl_times) / repeats, 
        sum(balance_bst_times) / repeats
    )



def save_csv(filename, algorithm, n_list, times):
    folder = "Sprawozdanie/results"
    os.makedirs(folder, exist_ok=True)
    filepath = os.path.join(folder, filename)

    with open(filepath, 'w') as f:
        f.write("Algorithm,InputSize,Time\n")
        for n, t in zip(n_list, times):
            f.write(f"{algorithm},{n},{t:.5f}\n")

def main():
    Ns = [2**11, 2**12, 2**13, 2**14, 2**15, 2**16, 2**17, 2**18, 2**19]
    tworz_bst, tworz_avl = [], []
    minmax_bst, minmax_avl = [], []
    inorder_bst, inorder_avl = [], []
    balans_bst = []

    for n in Ns:
        print(f"Benchmark dla n = {n}")
        b_ins, a_ins, b_minmax, a_minmax, b_inor, a_inor, b_bal = benchmark(n)
        tworz_bst.append(b_ins)
        tworz_avl.append(a_ins)
        minmax_bst.append(b_minmax)
        minmax_avl.append(a_minmax)
        inorder_bst.append(b_inor)
        inorder_avl.append(a_inor)
        balans_bst.append(b_bal)

    save_csv("czas_tworzenia_bst.csv", "BST", Ns, tworz_bst)
    save_csv("czas_minmax_bst.csv", "BST", Ns, minmax_bst)
    save_csv("czas_inorder_bst.csv", "BST", Ns, inorder_bst)
    save_csv("czas_balansowania_bst.csv", "BST", Ns, balans_bst)

    save_csv("czas_tworzenia_avl.csv", "AVL", Ns, tworz_avl)
    save_csv("czas_minmax_avl.csv", "AVL", Ns, minmax_avl)
    save_csv("czas_inorder_avl.csv", "AVL", Ns, inorder_avl)

if __name__ == "__main__":
    main()