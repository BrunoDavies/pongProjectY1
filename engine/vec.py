import math
import random


class Vec:

    def __init__(self, x, y):
        self.x = float(x)
        self.y = float(y)

    def length(self):
        return (self.x**2 + self.y**2)**0.5

    def set_length(self, length):
        scalar = length / self.length()
        self.x *= scalar
        self.y *= scalar

    @staticmethod
    def intersection_scalars(a_origin, a_direction, b_origin, b_direction):
        # then a_origin + u * a_direction = b_origin + v * b_direction
        # ~ if 0 <= u <= 1 then the first and second line cross each other
        dx = b_origin.x - a_origin.x
        dy = b_origin.y - a_origin.y
        det = b_direction.x * a_direction.y - b_direction.y * a_direction.x
        if det == 0:
            return float("inf"), float("inf")
        u = (dy * b_direction.x - dx * b_direction.y) / det
        v = (dy * a_direction.x - dx * a_direction.y) / det
        return u, v

    @staticmethod
    def random(length):
        angle = random.random() * 2 * math.pi
        x = length * math.sin(angle)
        y = length * math.cos(angle)
        return Vec(x, y)

    def compwise_mult(self, other):
        if not isinstance(other, Vec):
            raise TypeError
        return Vec(self.x * other.x, self.y * other.y)

    def __add__(self, other):
        if not isinstance(other, Vec):
            raise TypeError
        return Vec(self.x + other.x, self.y + other.y)

    def __mul__(self, scalar):
        return Vec(self.x * scalar, self.y * scalar)

    def __str__(self):
        return "<%.3f|%.3f>" % (self.x, self.y)

    def __repr__(self):
        return self.__str__()
