__author__ = 'dmitriy'


import operator
import sys


class Heap(object):
    def __init__(self, nodes = None):
        self.__nodes = [] if nodes is None else nodes
        if nodes is not None:
            for i in range(len(nodes) / 2, -1, -1):
                self.maintain_heap_property(i)

    def count(self):
        return len(self.__nodes)

    @property
    def nodes(self):
        return self.__nodes

    def root(self):
        return float("inf") if self.is_empty() else self.__nodes[0]

    def insert(self, item, comparator):
        def shift_up(current):
            parent = self.parent(current)
            if comparator(self.__nodes[parent], self.__nodes[current]):
                self.swap(parent, current)
                shift_up(parent)
        self.__nodes.append(item)
        shift_up(len(self.__nodes)-1)

    def remove_root(self):
        x = self.__nodes.pop(0)
        self.maintain_heap_property(0)
        return x

    def is_empty(self):
        return len(self.__nodes) == 0

    def __str__(self):
        return str(self.__nodes)

    def parent(self, x):
        return x >> 1

    def left(self, x):
        return ((x+1) << 1) - 1 if (x+1) << 1 < len(self.__nodes) else x

    def right(self, x):
        return ((x+1) << 1)  if ((x+1) << 1) < len(self.__nodes) else x

    def swap(self, first, second):
        self.__nodes[first], self.__nodes[second] = self.__nodes[second], self.__nodes[first]

    def maintain_heap_property(self, x, subtree_root=lambda x: x[0]):
        subtree = { i : self.nodes[i] for i in [self.left(x), self.right(x), x] }
        minor = subtree_root(subtree.items(), key=operator.itemgetter(1))
        if minor[0] != x:
            self.swap(x, minor[0])
            self.maintain_heap_property(minor[0])


class MaxHeap(Heap):
    def insert(self, item):
        Heap.insert(self, item, operator.lt)

    def maintain_heap_property(self, x):
        Heap.maintain_heap_property(self, x, max)


class MinHeap(Heap):
    def insert(self, item):
        Heap.insert(self, item, operator.gt)

    def maintain_heap_property(self, x):
        Heap.maintain_heap_property(self, x, min)


minor_part = MaxHeap()
major_part = MinHeap()


def stream_median(file):
    writeFile = open('is21_kalpakchi_04_output.txt', 'w')
    with file as f:
        for index, value in enumerate(f):
            value = int(value)
            if index > 2:
                minor_part.insert(value) if value < major_part.root() else major_part.insert(value)
                if major_part.count() - minor_part.count() > 1:
                    minor_part.insert(major_part.remove_root())
                elif minor_part.count() - major_part.count() > 1:
                    major_part.insert(minor_part.remove_root())
                if index % 2 == 0:
                    writeFile.writelines("%d %d\n" % (minor_part.root(), major_part.root()))
                elif major_part.count() > minor_part.count():
                    writeFile.writelines("%d\n" % major_part.root())
                else:
                    writeFile.writelines("%d\n" % minor_part.root())
            elif index > 0:
                minor_part.insert(value) if minor_part.is_empty() else major_part.insert(value)
                if minor_part.root() > major_part.root():
                    minor_part.nodes[0], major_part.nodes[0] = major_part.nodes[0], minor_part.nodes[0]
                    writeFile.writelines("%d %d\n" % (minor_part.root(), major_part.root()))
                else:
                    if major_part.is_empty():
                        writeFile.writelines("%d\n" % min(minor_part.root(), major_part.root()))
                    else:
                        writeFile.writelines("%d %d\n" % (minor_part.root(), major_part.root()))
    writeFile.close()

if __name__ == '__main__':
    file = open(sys.argv[1])
    stream_median(file)
    file.close()