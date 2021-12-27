NO_ITEM = -1
OK = 0


class Node:
    """
    BST Node
    """

    def __init__(self, key, value=None, left=None, right=None):
        """
        Constructor for BST Node
        :param key: int
        :param value: anything
        :param left: Left son - Node or None
        :param right: Right son - Node or None
        """
        self.key = key
        self.value = value
        self.left = left
        self.right = right

    def __repr__(self):
        return 'Node: key,value=(' + str(self.key) + ',' + str(self.value) + ')'


class BST:
    """
    BST Data Structure
    """

    def __init__(self, root=None):
        """
        Constructor for BST
        :param root: root of another BST
        """
        self.root = root

    def __repr__(self):
        """
        :return: a string represent the tree
        """
        s = '--------------------------------------'
        next = True
        level_arr = []
        cur_arr = [self.root]
        while next:
            next_arr = []
            for node in cur_arr:
                if node is not None:
                    next_arr.append(node.left)
                    next_arr.append(node.right)
                else:
                    next_arr.append(None)
                    next_arr.append(None)
            level_arr.append(cur_arr)
            for tmp in next_arr:
                if tmp is not None:
                    next = True
                    break
                else:
                    next = False
            cur_arr = next_arr
        d_arr = []
        d = 0
        for i in range(len(level_arr)):
            d_arr.append(d)
            d = 2 * d + 1
        d_arr.reverse()
        for i in range(len(level_arr)):
            s += '\n' + self.__level_repr(level_arr[i], d_arr[i])
        return s

    def __level_repr(self, arr, d):
        """
        helper for repr
        """
        s = ' ' * d
        for node in arr:
            if node is None:
                s = s + '!'
            else:
                s = s + str(node.key)
            s = s + ' ' * (2 * d + 1)
        return s

    def insert(self, key, value):
        """
        Inserts a new (key,value) pair to the BST.
        In case key already exists in the BST update the node's value
        :param key: int
        :returns None
        """
        # try to find if the key already exists in the BST - if exists update value and return
        if self.find(key):
            cur = self.find(key)
            cur.value = value
            return

        # if the key doesn't exist - insert
        else:
            if self.root:
                self._insert(key, value, self.root)
            else:
                self.root = Node(key, value)

    def _insert(self, key, value, cur):
        """
        helper for insert

        Description
        -----------
        * if the key is bigger/smaller than the current node's key -> go right/left
        * then check if a node exists - if yes then apply the function recursively until reach to an empty leaf

        Args
        ----
        key = The desired key to insert
        value = The desired value to insert
        cur = The current node
        """
        if key > cur.key:
            if cur.right:
                self._insert(key, value, cur.right)
            else:
                cur.right = Node(key, value)
        elif key < cur.key:
            if cur.left:
                self._insert(key, value, cur.left)
            else:
                cur.left = Node(key, value)

    def delete(self, key):
        """
        Remove the node associated with key from the BST.
        If key not in BST don't do anything.
        :param key: int
        :return: OK if deleted successfully or NO_ITEM if key not in the BST
        """
        # search for key in the BST - if it is not found return NO_ITEM
        if not self.find(key):
            return NO_ITEM

        # find the node by the key and its parent
        cur = self.root
        parent = None
        while cur:
            if key > cur.key:
                parent = cur
                cur = cur.right
            elif key < cur.key:
                parent = cur
                cur = cur.left
            else:
                break

        # now there are 3 possible cases - the node has 0/1/2 children
        # if there is only one child, and it is a left child
        if cur.left and not cur.right:

            # check if the node is the root, and it is the only node in the tree
            if cur == self.root:
                self.root = None
                return OK
            if cur.key > parent.key:
                parent.right = cur.left
            else:
                parent.left = cur.left
            return OK

        # if there is only one child, and it is a right child
        elif cur.right and not cur.left:

            # check if the node is the root, and it is the only node in the tree
            if cur == self.root:
                self.root = None
                return OK
            if cur.key > parent.key:
                parent.right = cur.right
            else:
                parent.left = cur.left
            return OK

        # if there are no children to this node
        elif not cur.right and not cur.left:

            # check if the node is the root, and it is the only node in the tree
            if cur == self.root:
                self.root = None
                return OK
            if cur.key > parent.key:
                parent.right = None
            else:
                parent.left = None
            return OK

        # if there are 2 children to the node
        else:
            # find the node with the smallest key in the right subtree and its parent
            min_cur, min_parent = self.find_min(cur.right)

            # if the node that we want to delete is the root
            if self.root == cur:
                cur.key = min_cur.key
                cur.value = min_cur.value
                try:
                    min_parent.left = None
                except AttributeError:
                    if cur.right.right:
                        cur.right = cur.right.right
                    else:
                        cur.right = None

            # if the node is bigger than its parent
            elif cur.key > parent.key:
                parent.right.key = min_cur.key
                parent.right.value = min_cur.value
                try:
                    min_parent.left = None
                except AttributeError:
                    if cur.right.right:
                        cur.right = cur.right.right
                    else:
                        cur.right = None

            # if the node is smaller than its parent
            else:
                parent.left.key = min_cur.key
                parent.left.value = min_cur.value
                try:
                    min_parent.left = None
                except AttributeError:
                    if cur.right.right:
                        cur.right = cur.right.right
                    else:
                        cur.right = None
            return OK

    @staticmethod
    def find_min(cur):
        """
        Description
        -----------
        This function takes a node as an input and refers to it as root.
        Then, it finds the node with the smallest key in the tree and returns it

        Args
        ----
        cur = Tree's node

        Returns
        -------
        The node with the smallest value in the cur's subtree and its parent
        """
        parent = None
        while cur.left:
            parent = cur
            cur = cur.left
        return cur, parent

    def find(self, key):
        """
        If key is in the BST find the Node associated with key
        otherwise return None
        :param key: int
        :return: Node if key is in BST or None o.w.
        """
        cur = self.root
        while cur is not None:
            if key > cur.key:
                cur = cur.right
            elif key < cur.key:
                cur = cur.left
            else:
                return cur
        return cur

    def inorder_traversal(self):
        """
        :return: an array (Python list) of keys sorted according to the inorder traversal of self
        """
        i_o_t  = []

        if self.root:
            if self.root.left:
                left_sub = BST(self.root.left)
                i_o_t += left_sub.inorder_traversal()

            i_o_t.append(self.root.key)

            if self.root.right:
                right_sub = BST(self.root.right)
                i_o_t += right_sub.inorder_traversal()
            return i_o_t

        else:
            return []

    def preorder_traversal(self):
        """
        :return: an array (Python list) of keys sorted according to the preorder traversal of self
        """
        pr_o_t = []

        if self.root:
            pr_o_t.append(self.root.key)

            if self.root.left:
                left_sub = BST(self.root.left)
                pr_o_t += left_sub.preorder_traversal()
            if self.root.right:
                right_sub = BST(self.root.right)
                pr_o_t += right_sub.preorder_traversal()
            return pr_o_t
        else:
            return []

    def postorder_traversal(self):
        """
        :return: an array (Python list) of keys sorted according to the postorder traversal of self
        """
        po_o_t = []

        if self.root:
            if self.root.left:
                left_sub = BST(self.root.left)
                po_o_t += left_sub.postorder_traversal()
            if self.root.right:
                right_sub = BST(self.root.right)
                po_o_t += right_sub.postorder_traversal()
            po_o_t.append(self.root.key)
            return po_o_t
        else:
            return []

    @staticmethod
    def create_BST_from_sorted_arr(arr):
        """
        Creates a balanced BST from a sorted array of keys according to the algorithm from class.
        The values of each key should be None.
        :param arr: sorted array as Python list
        :return: an object of type BST representing the balanced BST
        """
        # validate that the array exists
        if not arr:
            return None

        # if the array has only one key
        if len(arr) == 1:
            return BST(Node(arr[0]))

        mid = int((len(arr)//2))
        root = Node(arr[mid], value=None)

        try:
            root.left = BST.create_BST_from_sorted_arr(arr[:mid]).root
            root.right = BST.create_BST_from_sorted_arr(arr[mid+1:]).root
        except AttributeError:
            pass

        return BST(root)


# -------------------------------------------------------------------------------------------------------------------- #


class AVLNode(Node):
    """
    Node of AVL
    """

    def __init__(self, key, value=None, left=None, right=None):
        """
        Constructor for AVL Node
        :param key: int
        :param value: anything
        :param left: Left son - Node or None
        :param right: Right son - Node or None
        """
        super(AVLNode, self).__init__(key, value, left, right)
        self.height = 0

    def __repr__(self):
        return super(AVLNode, self).__repr__() + ',' + 'height=' + str(self.height)

    def get_balance(self):
        """
        :return: The balance of the tree rooted at self: self.left.height-self.right.height
        """
        h_left, h_right = -1, -1
        if self.left:
            h_left = self.left.height
        if self.right:
            h_right = self.right.height
        return h_left-h_right


class AVL(BST):
    """
    AVL Data Structure
    """

    def __init__(self, root=None):
        """
        Constructor for a new AVL
        :param root: root of another AVL
        """
        super(AVL, self).__init__(root)

    def insert(self, key, value):
        """
        Inserts a new (key,value) pair to the AVL.
        In case key already exists in the AVL update the node's value
        :param key: int
        """

        # check if the key already exists in the AVL
        if self.find(key):
            cur = self.find(key)
            cur.value = value
            print(f'{key} already exists in the BST')
            return

        # if there is no root to the tree
        if not self.root:
            self.root = AVLNode(key, value)

        # if the key is smaller than the root's key go left
        elif key < self.root.key:
            left_sub = AVL(self.root.left)
            left_sub.insert(key, value)
            self.root.left = left_sub.root
            self.root.height = max(self.get_height(self.root.left), self.get_height(self.root.right)) + 1
            self.inner_balance(self.root.left)  # keep the tree balanced

        # if the key is higher than the root's key go right
        else:
            right_sub = AVL(self.root.right)
            right_sub.insert(key, value)
            self.root.right = right_sub.root
            self.root.height = max(self.get_height(self.root.left), self.get_height(self.root.right)) + 1
            self.inner_balance(self.root.right)  # keep the tree balanced

    def delete(self, key):
        """
        Remove the node associated with key from the BST.
        If key not in BST don't do anything.
        :param key: int
        :return: OK if deleted successfully or NO_ITEM if key not in the BST
        """
        # if there is no such node with the specified key return NO_ITEM
        if not self.find(key):
            return NO_ITEM

        # find the node and its parent
        cur = self.root
        parent = None
        while cur:
            if key > cur.key:
                parent = cur
                cur = cur.right
            elif key < cur.key:
                parent = cur
                cur = cur.left
            else:
                break

        # similar to BST there are 3 possible cases - 0/1/2 children to the node
        # if there is only one child, and it is the left one
        if cur.left and not cur.right:

            # check if the node is the root, and it is the only node
            if cur == self.root:
                self.root = None
                return OK
            if cur.key > parent.key:
                parent.right = cur.left
            else:
                parent.left = cur.left
            self.update_heights(parent)  # update the heights
            self.inner_balance(parent)  # keep the tree balanced
            deleted = OK

        # if there is only one child, and it is the right one
        elif cur.right and not cur.left:

            # check if the node is the root, and it is the only node
            if cur == self.root:
                self.root = None
                return OK
            if cur.key > parent.key:
                parent.right = cur.right
            else:
                parent.left = cur.left
            self.update_heights(parent)  # update the heights
            self.inner_balance(parent)  # keep the tree balanced
            deleted = OK

        # if there are no children
        elif not cur.right and not cur.left:

            # check if the node is the root, and it is the only node
            if cur == self.root:
                self.root = None
                return OK
            elif cur.key > parent.key:
                parent.right = None
            else:
                parent.left = None
            self.update_heights(parent)  # update the heights
            self.inner_balance(parent)  # keep the tree balanced
            deleted = OK

        # if there are two children
        else:

            # find the key with the smallest key and its parent
            min_cur, min_parent = self.find_min(cur.right)

            # if the node is the root
            if self.root == cur:
                cur.key = min_cur.key
                cur.value = min_cur.value
                try:
                    min_parent.left = None
                    self.update_heights(min_parent)
                except AttributeError:
                    if cur.right.right:
                        cur.right = cur.right.right
                    else:
                        cur.right = None
                self.update_heights(cur)  # update the heights
                self.inner_balance(cur)  # keep the tree balanced
                deleted = OK

            # if the node is bigger than its parent go right
            elif cur.key > parent.key:
                parent.right.key = min_cur.key
                parent.right.value = min_cur.value
                try:
                    min_parent.left = None
                    self.update_heights(min_parent)
                except AttributeError:
                    if cur.right.right:
                        cur.right = cur.right.right
                    else:
                        cur.right = None
                self.update_heights(cur)  # update the heights
                self.inner_balance(cur)  # keep the tree balanced
                deleted = OK

            # if the node is smaller than its parent go left
            else:
                parent.left.key = min_cur.key
                parent.left.value = min_cur.value
                try:
                    min_parent.left = None
                except AttributeError:
                    if cur.right.right:
                        cur.right = cur.right.right
                    else:
                        cur.right = None
                self.update_heights(cur)  # update the heights
                self.inner_balance(cur)  # keep the tree balanced
                deleted = OK

        return deleted

    def update_heights(self, cur):
        """
        Description
        -----------
        update the heights of the nodes and its parents

        Args
        ----
        cur = Tree's node
        """
        if cur != self.root:
            while cur != self.root:
                cur.height = max(self.get_height(cur.right), self.get_height(cur.left)) + 1
                cur = self.find_parent(cur)
        else:
            cur.height = max(self.get_height(cur.right), self.get_height(cur.left)) + 1

    def find_parent(self, cur):
        """
        Description
        -----------
        This function takes a node as an input and returns its parent

        Args
        ----
        cur = Tree's node

        Returns
        --------
        The node's parent
        """
        root = self.root
        parent = None
        while root != cur and root:
            if cur.key < root.key:
                parent = root
                root = root.left
            else:
                parent = root
                root = root.right
        return parent

    @staticmethod
    def get_height(cur):
        """
        Description
        -----------
        This function gets the height of a specific node

        Args
        ----
        cur = Tree's node

        Returns
        -------
        The node's height
        """
        if cur:
            return cur.height
        else:
            return -1

    def balance_factor(self, cur):
        """
        Description
        -----------
        This function gets the balance factor of a node

        Args
        ----
        cur = Tree's node

        Returns
        -------
        The node's balance factor
        """
        if cur:
            return self.get_height(cur.left)-self.get_height(cur.right)
        else:
            return 0

    def left_rotate(self, cur, parent):
        """
        Description
        -----------
        This function performs a left rotation to keep the AVL tree balanced

        Args
        ----
        cur = The unbalanced node
        parent = The unbalanced node's parent
        """
        pivot = cur.right
        gc = pivot.left

        pivot.left = cur
        cur.right = gc

        if not parent:
            self.root = pivot
        elif parent.key < cur.key:
            parent.right = pivot
        else:
            parent.left = pivot

        self.update_heights(cur)
        self.update_heights(pivot)
        if parent:
            self.update_heights(parent)

    def right_rotate(self, cur, parent):
        """
        Description
        -----------
        This function performs a right rotation to keep the AVL tree balanced

        Args
        ----
        cur = The unbalanced node
        parent = The unbalanced node's parent
        """
        pivot = cur.left
        gc = pivot.right

        pivot.right = cur
        cur.left = gc

        self.update_heights(cur)
        self.update_heights(pivot)

        if not parent:
            self.root = pivot
        elif parent.key < cur.key:
            parent.right = pivot
        else:
            parent.left = pivot

        if parent:
            self.update_heights(parent)

    def inner_balance(self, cur):
        """
        Description
        -----------
        This function gets a node as an input and keeps it balanced

        Args
        ----
        cur = Tree's node
        """
        if cur:

            while cur:

                # get the node's balance factor and if it has a parent - find it
                balance_factor = self.balance_factor(cur)
                try:
                    parent = self.find_parent(cur)
                except ArithmeticError:
                    parent = None

                # as long as |balance factor| > 1 the tree is not balanced
                while balance_factor < -1 or balance_factor > 1:

                    if balance_factor < -1 and self.balance_factor(cur.right) <= 0:
                        self.left_rotate(cur, parent)
                        balance_factor = self.balance_factor(cur)

                    if balance_factor > 1 and self.balance_factor(cur.left) >= 0:
                        self.right_rotate(cur, parent)
                        balance_factor = self.balance_factor(cur)

                    if balance_factor < -1 and self.balance_factor(cur.right) > 0:
                        self.right_rotate(cur.right, cur)
                        self.left_rotate(cur, parent)
                        balance_factor = self.balance_factor(cur)

                    if balance_factor > 1 and self.balance_factor(cur.left) < 0:
                        self.left_rotate(cur.left, cur)
                        self.right_rotate(cur, parent)
                        balance_factor = self.balance_factor(cur)
                cur = parent