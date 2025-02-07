class Position:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def to_tuple(self):
        return self.x, self.y

    def __eq__(self, other):
        return self.x == other.x and self.y == other.y

    def __str__(self):
        return f"({self.x}, {self.y})"

    def __add__(self, other):
        return Position(self.x + other.x, self.y + other.y)

    def __sub__(self, other):
        return Position(self.x - other.x, self.y - other.y)

    def __mul__(self, other):
        return Position(self.x * other, self.y * other)

    def __truediv__(self, other):
        return Position(self.x / other, self.y / other)

    def __floordiv__(self, other):
        return Position(self.x // other, self.y // other)

    def __mod__(self, other):
        return Position(self.x % other, self.y % other)

    def __neg__(self):
        return Position(-self.x, -self.y)
