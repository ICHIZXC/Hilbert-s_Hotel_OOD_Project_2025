import random

class Treap:
    class Node:
        def __init__(self, data):
            self.data = data
            self.priority = random.random()
            self.left = None
            self.right = None

        def __str__(self):
            return f"{self.data}({self.priority:.3f})"

    def __init__(self):
        self.root = None

    # Add method for compatibility with main.py
    def add(self, data):
        self.root = self._add(self.root, data)
        return self.root

    def _add(self, root, data):
        if root is None:
            return self.Node(data)
        if data < root.data:
            root.left = self._add(root.left, data)
            if root.left.priority > root.priority:
                root = self._rotateRight(root)
        elif data > root.data:
            root.right = self._add(root.right, data)
            if root.right.priority > root.priority:
                root = self._rotateLeft(root)
        return root

    def delete(self, data):
        self.root, deleted = self._delete(self.root, data)
        return deleted
    
    # Alias for compatibility with main.py
    def delete_node(self, data):
        return self.delete(data)

    def _delete(self, root, data):
        if root is None:
            return None, False

        deleted = False
        if data < root.data:
            root.left, deleted = self._delete(root.left, data)
        elif data > root.data:
            root.right, deleted = self._delete(root.right, data)
        else:
            deleted = True
            if root.left is None and root.right is None:
                return None, True
            elif root.left is None:
                root = self._rotateLeft(root)
                root.left, _ = self._delete(root.left, data)
            elif root.right is None:
                root = self._rotateRight(root)
                root.right, _ = self._delete(root.right, data)
            else:
                if root.left.priority > root.right.priority:
                    root = self._rotateRight(root)
                    root.right, _ = self._delete(root.right, data)
                else:
                    root = self._rotateLeft(root)
                    root.left, _ = self._delete(root.left, data)
        return root, deleted

    def _rotateRight(self, y):
        x = y.left
        y.left = x.right
        x.right = y
        return x

    def _rotateLeft(self, x):
        y = x.right
        x.right = y.left
        y.left = x
        return y

    def InOrder(self):
        result = []
        self._inorder(self.root, result)
        return result
    
    # Alias for compatibility with main.py
    def inorder(self):
        result = []
        self._inorder(self.root, result)
        print(result)  # Print the sorted rooms
        return result

    def _inorder(self, node, result):
        if node:
            self._inorder(node.left, result)
            result.append(node.data)  # Append the data (room number), not the node
            self._inorder(node.right, result)