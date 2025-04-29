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

    def insert(self, key):
        self.root = self._insert(self.root, key)

    def _insert(self, node, key):
        if not node:
            return AVLNode(key)
        if key < node.key:
            node.left = self._insert(node.left, key)
        else:
            node.right = self._insert(node.right, key)

        node.height = 1 + max(self.get_height(node.left), self.get_height(node.right))
        balance = self.get_balance(node)

        if balance > 1 and key < node.left.key:
            return self.right_rotate(node)
        if balance < -1 and key > node.right.key:
            return self.left_rotate(node)
        if balance > 1 and key > node.left.key:
            node.left = self.left_rotate(node.left)
            return self.right_rotate(node)
        if balance < -1 and key < node.right.key:
            node.right = self.right_rotate(node.right)
            return self.left_rotate(node)

        return node

    def left_rotate(self, z):
        y = z.right
        T2 = y.left
        y.left = z
        z.right = T2
        z.height = 1 + max(self.get_height(z.left), self.get_height(z.right))
        y.height = 1 + max(self.get_height(y.left), self.get_height(y.right))
        return y

    def right_rotate(self, y):
        x = y.left
        T2 = x.right
        x.right = y
        y.left = T2
        y.height = 1 + max(self.get_height(y.left), self.get_height(y.right))
        x.height = 1 + max(self.get_height(x.left), self.get_height(x.right))
        return x

    def get_height(self, node):
        return node.height if node else 0

    def get_balance(self, node):
        return self.get_height(node.left) - self.get_height(node.right) if node else 0

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
    for _ in range(repeats):
        bst = BST()
        t1 = time.perf_counter()
        for v in values:
            bst.insert(v)
        bst_insert_times.append(time.perf_counter() - t1)
    avg_bst_insert = sum(bst_insert_times) / repeats

    bst = BST()
    for v in values:
        bst.insert(v)

    bst_find_times = []
    for _ in range(repeats):
        t1 = time.perf_counter()
        bst.find_min()
        bst.find_max()
        bst_find_times.append(time.perf_counter() - t1)
    avg_bst_find = sum(bst_find_times) / repeats

    bst_inorder_times = []
    for _ in range(repeats):
        t1 = time.perf_counter()
        bst.inorder()
        bst_inorder_times.append(time.perf_counter() - t1)
    avg_bst_inorder = sum(bst_inorder_times) / repeats

    bst_balance_times = []
    for _ in range(repeats):
        t1 = time.perf_counter()
        bst.balance()
        bst_balance_times.append(time.perf_counter() - t1)
    avg_bst_balance = sum(bst_balance_times) / repeats

    avl_insert_times = []
    for _ in range(repeats):
        avl = AVL()
        t1 = time.perf_counter()
        for v in values:
            avl.insert(v)
        avl_insert_times.append(time.perf_counter() - t1)
    avg_avl_insert = sum(avl_insert_times) / repeats

    avl = AVL()
    for v in values:
        avl.insert(v)

    avl_find_times = []
    for _ in range(repeats):
        t1 = time.perf_counter()
        avl.find_min()
        avl.find_max()
        avl_find_times.append(time.perf_counter() - t1)
    avg_avl_find = sum(avl_find_times) / repeats

    avl_inorder_times = []
    for _ in range(repeats):
        t1 = time.perf_counter()
        avl.inorder()
        avl_inorder_times.append(time.perf_counter() - t1)
    avg_avl_inorder = sum(avl_inorder_times) / repeats

    return (
        avg_bst_insert,
        avg_avl_insert,
        avg_bst_find,
        avg_avl_find,
        avg_bst_inorder,
        avg_avl_inorder,
        avg_bst_balance
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
    znajdz_bst, znajdz_avl = [], []
    inorder_bst, inorder_avl = [], []
    balans_bst = []

    for n in Ns:
        print(f"Benchmark dla n = {n}")
        b_ins, a_ins, b_find, a_find, b_inor, a_inor, b_bal = benchmark(n)
        tworz_bst.append(b_ins)
        tworz_avl.append(a_ins)
        znajdz_bst.append(b_find)
        znajdz_avl.append(a_find)
        inorder_bst.append(b_inor)
        inorder_avl.append(a_inor)
        balans_bst.append(b_bal)

    save_csv("czas_tworzenia_bst.csv", "BST", Ns, tworz_bst)
    save_csv("czas_szukania_bst.csv", "BST", Ns, znajdz_bst)
    save_csv("czas_inorder_bst.csv", "BST", Ns, inorder_bst)
    save_csv("czas_balansowania_bst.csv", "BST", Ns, balans_bst)

    save_csv("czas_tworzenia_avl.csv", "AVL", Ns, tworz_avl)
    save_csv("czas_szukania_avl.csv", "AVL", Ns, znajdz_avl)
    save_csv("czas_inorder_avl.csv", "AVL", Ns, inorder_avl)

if __name__ == "__main__":
    main()