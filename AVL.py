# method in AVL add(data) , inorder() ,remove(data)


class Node:
    def __init__(self, data, left=None, right=None):
        self.data = data
        self.left = left
        self.right = right
        self.height = self.setHeight()

    def setHeight(self):
        a = self.getHeight(self.left)
        b = self.getHeight(self.right)
        self.height = 1 + max(a, b)
        return self.height

    def getHeight(self, node):
        return -1 if node is None else node.height

    def balanceValue(self):
        return self.getHeight(self.left) - self.getHeight(self.right)


class AVL:
    def __init__(self):
        self.root = None

    def add(self, data):
        self.root = self._add(self.root, data)

    def _add(self, root, data):
        if root is None:
            return Node(data)
        if data < root.data:
            root.left = self._add(root.left, data)
        else:
            root.right = self._add(root.right, data)

        root = self.rebalance(root)
        root.setHeight()
        return root

    def leftRotate(self, x):
        y = x.right
        x.right = y.left
        y.left = x
        x.setHeight()
        y.setHeight()
        return y

    def rightRotate(self, x):
        y = x.left
        x.left = y.right
        y.right = x
        x.setHeight()
        y.setHeight()
        return y

    def rebalance(self, x):
        if x is None:
            return x

        balance = x.balanceValue()
        if balance < -1:
            if x.right.balanceValue() > 0:  
                x.right = self.rightRotate(x.right)
            x = self.leftRotate(x)
        elif balance > 1:
            if x.left.balanceValue() < 0:  
                x.left = self.leftRotate(x.left)
            x = self.rightRotate(x)

        x.setHeight()
        return x

    def inorder(self):
        self._inorder(self.root)

    def _inorder(self, root):
        if root is not None:
            self._inorder(root.left)
            print(root.data, end=" ")
            self._inorder(root.right)
        
    def delete_node(self,target):
        self._delete_node(self.root,target)
    
    def _delete_node(self, root, target):
        if not root:
            return root
        
        if root.data == target:
            if not root.left and not root.right:
                return None
            if not root.left:
                return root.right
            if not root.right:
                return root.left
            succ = self.min_value(root.right)
            root.data = succ.data
            root.right = self._delete_node(root.right, succ.data)
            return root
        
        elif target < root.data:  
            root.left = self._delete_node(root.left, target)
        else:
            root.right = self._delete_node(root.right, target)
        
        root = self.rebalance(root)
        root.setHeight()
        return root  

    def min_value(self, node):
        while node.left:
            node = node.left
        return node