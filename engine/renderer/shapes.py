from abc import ABC, abstractmethod


#
#   P=Polygon(depth,width,color,parameters*)
#   R=Rect(d,w,c,(x,y),(x,y))
#   R=Rect(d,w,c,x,y,x,y)
#   C=Circle(d,w,c,(x,y),r)

class Shape(ABC):
    @abstractmethod
    def __init__(self):
        self.depth = None
        self.points = None
        self.width = None
        self.color = None

    @abstractmethod
    def get_type(self): ...

    def get_depth(self): return self.depth

    def get_parameters(self): return self.points

    def get_width(self): return self.width

    def get_color(self): return self.color


class Rect(Shape):
    def __init__(self, depth, width, color, a, b, c=None, d=None):
        self.depth = depth
        self.width = width
        self.color = color
        if c is None and d is None:
            self.points = [a, b]
        else:
            self.points = [(a, b), (c, d)]

    def get_type(self):
        return "rectangle"


class Polygon(Shape):
    def __init__(self, depth, width, color, *points):
        self.depth = depth
        self.width = width
        self.color = color
        self.points = points

    def get_type(self): return "polygon"


class Circle(Shape):
    def __init__(self, depth, width, color, *params):
        self.depth = depth
        self.width = width
        self.color = color
        self.points = params

    def get_type(self): return 'circle'
