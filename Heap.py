class Node:
        def __init__(self, weight, point):
            self.weight = weight
            self.point = point
            self.left = None
            self.right = None

class Heap:
    def __init__(self,max_size):
        self.heap = [None]*(max_size+1)
        first = Node(-1 , None)
        self.heap[0] = first
        self.size = 0

    def parent(self, pos):
        return pos // 2

    def left_child(self, pos):
        return pos * 2

    def right_child(self, pos):
        return pos * 2 + 1
    def get_size(self):
        return self.size

    def insert(self, element):
        self.size += 1
        self.heap[self.size] = element
        current = self.size
        while self.heap[current].weight < self.heap[self.parent(current)].weight:
            self.swap(current, self.parent(current))
            current = self.parent(current)

    def min_heap(self):
        for pos in range(self.size // 2, 0, -1):
            self.min_heapify(pos)

    def remove(self):
        popped = self.heap[1]
        self.heap[1] = self.heap[self.size]
        self.size -= 1

        self.min_heapify(1)
        return popped

    def is_leaf(self, pos):
        return pos > self.size // 2

    def swap(self, fpos, spos):
        self.heap[fpos], self.heap[spos] = self.heap[spos], self.heap[fpos]

    def min_heapify(self, pos):
        if not self.is_leaf(pos):
            if (
                self.heap[pos].weight > self.heap[self.left_child(pos)].weight
                or self.heap[pos].weight > self.heap[self.right_child(pos)].weight
            ):
                if (
                    self.heap[self.left_child(pos)].weight
                    < self.heap[self.right_child(pos)].weight
                ):
                    self.swap(pos, self.left_child(pos))
                    self.min_heapify(self.left_child(pos))
                else:
                    self.swap(pos, self.right_child(pos))
                    self.min_heapify(self.right_child(pos))
