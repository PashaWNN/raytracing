from numpy import sqrt
from copy import copy


x, y, z, w = 0, 1, 2, 3


class Vector:
    size = 0
    t = float
    __slots__ = 'arr',

    def __getattr__(self, item):
        if item == 'x':
            return self[x]
        elif item == 'y':
            return self[y]
        elif item == 'z':
            return self[z]
        elif item == 'w':
            return self[w]
        super().__getattribute__(item)

    def __setattr__(self, item, value):
        if item == 'x':
            self[x] = value
            return
        elif item == 'y':
            self[y] = value
            return
        elif item == 'z':
            self[z] = value
            return
        elif item == 'w':
            self[w] = value
            return
        super().__setattr__(item, value)

    def normalize(self):
        return self.__class__(*[i/self.norm() for i in self.arr])

    def norm(self):
        sum = 0
        for i in self.arr:
            sum += i ** 2
        return sqrt(sum)

    def __init__(self, *args):
        if len(args) == 1:
            if isinstance(args[0], self.__class__):
                self.arr = copy(args[0].arr)
                return
            if type(args[0]) in (list, tuple):
                assert len(args[0]) == self.size
                self.arr = list(args[0])
                return
        self.arr = [0] * self.size
        assert len(args) <= self.size
        for i, arg in enumerate(args):
            self.arr[i] = arg

    def __getitem__(self, item: int):
        assert 0 <= item < self.size
        return self.arr[item]

    def __setitem__(self, item: int, value):
        assert 0 <= item < self.size
        #assert isinstance(value, self.t)
        self.arr[item] = value

    def __mul__(self, other):
        if isinstance(other, self.__class__):
            new = 0
            for i in range(self.size):
                new += self[i] * other[i]
            return new
        else:
            new = self.__class__()
            for i in range(self.size):
                new[i] = self[i] * other
            return new

    def __sub__(self, other):
        assert isinstance(other, self.__class__)
        new = self.__class__()
        for i in range(self.size):
            new[i] = self[i] - other[i]
        return new

    def __add__(self, other):
        assert isinstance(other, self.__class__)
        new = self.__class__()
        for i in range(self.size):
            new[i] = self[i] + other[i]
        return new

    def __neg__(self):
        return self*-1

    def cross(self, v1, v2):
        return self.__class__(v1.y*v2.z - v1.z * v2.y, v1.z * v2.x - v1.x * v2.z, v1.x * v2.y - v1.y * v2.x)


class Vec2f(Vector):
    size = 2
    t = float


class Vec3f(Vector):
    size = 3
    t = float


class Vec3i(Vector):
    size = 3
    t = int


class Vec4f(Vector):
    size = 4
    t = float
