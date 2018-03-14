#!/usr/bin/env python3
"""Plot binary tree.

Example:

    $ echo $'tesa\nterm' | python . | dot -Tpng | display
"""
import itertools
import sys
from collections.abc import MutableSet
from dataclasses import dataclass


@dataclass
class Node:
    value: str
    left: 'Node' = None
    right: 'Node' = None

    def to_dot(self, file, null_count=itertools.count()):
        p = lambda *args: print(*args, file=file)

        def name(node):
            return 'n' + str(id(node)) if node else 'null' + str(next(null_count))

        def print_node(node):
            node_name = name(node)
            if not node:
                p(node_name + ' [shape=point];')
            p('%s -> %s;' % (name(self), node_name))

        # n678_1 [label="678"];
        p('%s [label="%s"];' % (name(self), self.value))
        # n678_1 -> n383_1;
        print_node(self.left)
        print_node(self.right)
        if self.left:
            self.left.to_dot(file)
        if self.right:
            self.right.to_dot(file)


def extend_node(node, chars):
    for char in chars:
        node.left = Node(char)
        node = node.left


class BinaryTree(MutableSet):
    def __init__(self, words=()):
        self.__tree = None
        for word in words:
            self.add(word)

    def add(self, word):
        """

        Каждый узел дерева представляет собой объект, содержащий
        определенный символ, и ссылки на две ветви Left и
        Right. переход по ветви Left осуществляется если текущий
        символ строке распознаваемого совпадает с символом хранящейся
        в данном узле дерева. если символы не совпали осуществляется
        переход по ветке Right.

        """
        if not word:
            return  # do nothing
        chars = iter(word)
        if not self.__tree:  # first word
            node = self.__tree = Node(next(chars))
            extend_node(node, chars)
        else:
            parent = node = self.__tree
            assert node
            for char in chars:
                while True:
                    if not node:
                        node = Node(char)
                        setattr(parent, child, node)
                        extend_node(node, chars)
                        break
                    elif node.value == char:
                        parent, node, child = node, node.left, 'left'
                        break
                    else:
                        parent, node, child = node, node.right, 'right'

    def __contains__(self, word):
        """
        >>> tree = BinaryTree(['test', 'term', 'tell', 'tested'])
        >>> 'tell' in tree
        True
        >>> 'test' in tree
        True
        >>> 'term' in tree
        True
        >>> 'text' in tree
        False
        >>> 'team' in tree
        False
        >>> 'te' in tree
        True
        >>> 'tested' in tree
        True
        >>> 'testing' in tree
        False
        """
        if word and not self.__tree:
            return False  # empty tree, non-empty word
        node = self.__tree
        for char in word:
            while node:
                if node.value == char:
                    node = node.left
                    break
                else:  # not found
                    node = node.right
            else:  # not found (no break)
                return False
        return True

    __iter__, __len__, discard = [None]*3

    def to_dot(self, file):
        file.write("digraph {\n")
        if self.__tree:
            self.__tree.to_dot(file)
        file.write("}")


if __name__ == '__main__':
    if '--test' in sys.argv:
        import doctest
        doctest.testmod()
    else:
        tree = BinaryTree(map(str.strip, sys.stdin))
        tree.to_dot(sys.stdout)
