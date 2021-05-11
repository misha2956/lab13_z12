"""
File: linkedbst.py
Author: Ken Lambert
"""

import sys
import random
from math import log
from time import time

from bstnode import BSTNode
from linkedstack import LinkedStack
from abstractcollection import AbstractCollection

class LinkedBST(AbstractCollection):
    """An link-based binary search tree implementation."""

    def __init__(self, sourceCollection=None):
        """Sets the initial state of self, which includes the
        contents of sourceCollection, if it's present."""
        self._root = None
        self._rightmost_node = None
        self._leftmost_node = None
        AbstractCollection.__init__(self, sourceCollection)

    # Accessor methods
    def __str__(self):
        """Returns a string representation with the tree rotated
        90 degrees counterclockwise."""

        def recursion(node, level):
            string = ""
            if node != None:
                string += recursion(node.right, level + 1)
                string += "| " * level
                string += str(node.data) + "\n"
                string += recursion(node.left, level + 1)
            return string

        return recursion(self._root, 0)

    def __iter__(self):
        """Supports a preorder traversal on a view of self."""
        if not self.isEmpty():
            stack = LinkedStack()
            stack.push(self._root)
            while not stack.isEmpty():
                node = stack.pop()
                yield node.data
                if node.right != None:
                    stack.push(node.right)
                if node.left != None:
                    stack.push(node.left)

    def preorder(self):
        """Supports a preorder traversal on a view of self."""
        return None

    def inorder(self):
        """Supports an inorder traversal on a view of self."""
        ret = list()

        def recurse(node):
            if node != None:
                recurse(node.left)
                ret.append(node.data)
                recurse(node.right)

        recurse(self._root)
        return iter(ret)

    def postorder(self):
        """Supports a postorder traversal on a view of self."""
        return None

    def levelorder(self):
        """Supports a levelorder traversal on a view of self."""
        return None

    def __contains__(self, item):
        """Returns True if target is found or False otherwise."""
        return self.find(item) != None

    def find(self, item):
        """If item matches an item in self, returns the
        matched item, or None otherwise."""

        node = self._root

        while True:
            if node is None:
                return None
            elif item == node.data:
                return node.data
            elif item < node.data:
                node = node.left
            else:
                node = node.right

    # Mutator methods
    def clear(self):
        """Makes self become empty."""
        self._root = None
        self._size = 0

    def add(self, item):
        """Adds item to the tree."""

        if (
            self._leftmost_node is not None and
            item < self._leftmost_node.data
        ):
            self._leftmost_node.left = BSTNode(item)
            self._leftmost_node = self._leftmost_node.left
            return

        if (
            self._rightmost_node is not None and
            item > self._rightmost_node.data
        ):
            self._rightmost_node.right = BSTNode(item)
            self._rightmost_node = self._rightmost_node.right
            return

        # Tree is empty, so new item goes at the root
        if self.isEmpty():
            self._root = BSTNode(item)
        # Otherwise, search for the item's spot
        else:
            node = self._root
            while True:
                # New item is less, go left until spot is found
                if item < node.data:
                    if node.left == None:
                        node.left = BSTNode(item)
                        if (
                            self._leftmost_node is None or
                            node.right.data < self._leftmost_node.data
                        ):
                            self._leftmost_node = node.left
                        break
                    else:
                        node = node.left
                        continue
                # New item is greater or equal,
                # go right until spot is found
                elif node.right == None:
                    node.right = BSTNode(item)
                    if (
                        self._rightmost_node is None or
                        node.right.data > self._rightmost_node.data
                    ):
                        self._rightmost_node = node.right
                    break
                else:
                    node = node.right

        self._size += 1

    def remove(self, item):
        """Precondition: item is in self.
        Raises: KeyError if item is not in self.
        postcondition: item is removed from self."""
        if not item in self:
            raise KeyError("Item not in tree.""")

        # Helper function to adjust placement of an item
        def lift_max_in_left_subtree_to_top(top):
            # Replace top's datum with the maximum datum in the left subtree
            # Pre:  top has a left child
            # Post: the maximum node in top's left subtree
            #       has been removed
            # Post: top.data = maximum value in top's left subtree
            parent = top
            current_node = top.left
            while not current_node.right == None:
                parent = current_node
                current_node = current_node.right
            top.data = current_node.data
            if parent == top:
                top.left = current_node.left
            else:
                parent.right = current_node.left

        # Begin main part of the method
        if self.isEmpty(): return None

        # Attempt to locate the node containing the item
        item_removed = None
        pre_root = BSTNode(None)
        pre_root.left = self._root
        parent = pre_root
        direction = 'L'
        current_node = self._root
        while not current_node == None:
            if current_node.data == item:
                item_removed = current_node.data
                break
            parent = current_node
            if current_node.data > item:
                direction = 'L'
                current_node = current_node.left
            else:
                direction = 'R'
                current_node = current_node.right

        # Return None if the item is absent
        if item_removed == None: return None

        # The item is present, so remove its node

        # Case 1: The node has a left and a right child
        #         Replace the node's value with the maximum value in the
        #         left subtree
        #         Delete the maximium node in the left subtree
        if not current_node.left == None \
                and not current_node.right == None:
            lift_max_in_left_subtree_to_top(current_node)
        else:

            # Case 2: The node has no left child
            if current_node.left == None:
                new_child = current_node.right

                # Case 3: The node has no right child
            else:
                new_child = current_node.left

                # Case 2 & 3: Tie the parent to the new child
            if direction == 'L':
                parent.left = new_child
            else:
                parent.right = new_child

        # All cases: Reset the root (if it hasn't changed no harm done)
        #            Decrement the collection's size counter
        #            Return the item
        self._size -= 1
        if self.isEmpty():
            self._root = None
        else:
            self._root = pre_root.left
        return item_removed

    def replace(self, item, new_item):
        """
        If item is in self, replaces it with new_item and
        returns the old item, or returns None otherwise."""
        probe = self._root
        while probe != None:
            if probe.data == item:
                old_data = probe.data
                probe.data = new_item
                return old_data
            elif probe.data > item:
                probe = probe.left
            else:
                probe = probe.right
        return None

    def height(self):
        """
        Return the height of tree
        :return: int
        """

        def height_recursive(node):
            """
            Returns the height of a subtree with root in node
            :param node:
            :return:
            """
            if node is None:
                return -1
            return max(
                height_recursive(node.left), height_recursive(node.right)
            ) + 1

        return height_recursive(self._root)

    def is_balanced(self):
        """
        Return True if tree is balanced
        :return:
        """
        return self.height() < (2 * log(self._size + 1, 2) - 1)

    def rebalance(self):
        """
        Rebalances the tree.
        :return:
        """
        sorted_list = list(self.inorder())

        def get_node_recursive(leftp, rightp):
            if (rightp - leftp) == 1:
                return BSTNode(sorted_list[leftp])
            if (rightp - leftp) == 0:
                return None
            middle = int((leftp + rightp) / 2)
            node = BSTNode(sorted_list[middle])
            node.left = get_node_recursive(leftp, middle)
            node.right = get_node_recursive(middle + 1, rightp)
            return node

        self._root = get_node_recursive(0, len(sorted_list))

    def successor(self, item):
        """
        Returns the smallest item that is larger than
        item, or None if there is no such item.
        :param item:
        :type item:
        :return:
        :rtype:
        """

        for elem in self.inorder():
            if elem > item:
                return elem
        return None

    def predecessor(self, item):
        """
        Returns the largest item that is smaller than
        item, or None if there is no such item.
        :param item:
        :type item:
        :return:
        :rtype:
        """

        ret = None
        for elem in self.inorder():
            if elem < item:
                ret = elem
        return ret

    def range_find(self, from_data, to_data):
        """
        find elements in specified range
        """
        ret_list = []
        for elem in self.inorder():
            if elem > to_data:
                return ret_list
            if elem >= from_data:
                ret_list.append(elem)
        return ret_list

    def demo_bst(self, path='words.txt'):
        """
        Demonstration of efficiency binary search tree for the search tasks.
        :param path:
        :type path:
        :return:
        :rtype:
        """
        # alphabet = "".join(chr(chi) for chi in range(ord('a'), 1 + ord('z')))
        # random_word = lambda x: "".join(random.sample(alphabet, x))
        # words_list = [random_word(8) for _ in range(10000)]

        words_list = list(
            map(lambda x: x.strip(), open(path, 'r').readlines())
        )
        words_list_sh = words_list[:]
        random.shuffle(words_list_sh)
        linBST_s = LinkedBST()
        for word in words_list:
            linBST_s.add(word)
        linBST_sh = LinkedBST()
        for word in words_list_sh:
            linBST_sh.add(word)
        linBST_sh_bal = LinkedBST(linBST_sh)
        linBST_sh_bal.rebalance()
        list_time = 0
        linBST_s_time = 0
        linBST_sh_time = 0
        linBST_sh_bal_time = 0

        for _ in range(10000):
            word = random.choice(words_list)

            t_rec = time()
            words_list.index(word)
            list_time += time() - t_rec

            t_rec = time()
            linBST_s.find(word)
            linBST_s_time += time() - t_rec

            t_rec = time()
            linBST_sh.find(word)
            linBST_sh_time += time() - t_rec

            t_rec = time()
            linBST_sh_bal.find(word)
            linBST_sh_bal_time += time() - t_rec

        print("Tested on 10000 samples:")
        print(f"list.index() time: {list_time:.5f}s")
        print(f"binary tree, sorted adding method time: {linBST_s_time:.5f}s")
        print(
            f"binary tree, shuffled adding method time: {linBST_sh_time:.5f}s"
        )
        print(
            "binary tree, shuffled adding method, balanced time:",
            f"{linBST_sh_bal_time:.5f}s"
        )
