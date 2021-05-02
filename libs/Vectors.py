class Vector2D:
    def __init__(self, x=0, y=0):
        self.x = x
        self.y = y

    def __len__(self):
        return (x**2 + y**2)**0.5

    def __mul__(self, other):
        if isinstance(other, int) or isinstance(other, float):
            return Vector2D(other*self.x, other*self.y)

    def __add__(self, other):
        return Vector2D(self.x + other.x, self.y + other.y)

    def __sub__(self, other):
        return Vector2D(self.x - other.x, self.y - other.y)

    @property
    def toTuple(self):
        return (self.x, self.y)
