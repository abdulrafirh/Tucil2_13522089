import typing

class Point :

    def __init__(self, x : float, y : float) :
        self.x : float = x
        self.y : float = y

    def __eq__(self, other: any) -> bool :
        try :
            return self.x == other.x and self.y == other.y
        except :
            NotImplemented

    def __add__(self, other: any) -> 'Point' :
        try :
            return Point(self.x + other.x, self.y + other.y)
        except :
            NotImplemented

    def midpoint(self, other: 'Point') -> 'Point' :
        try :
            return Point((self.x + other.x)/2, (self.y + other.y)/2)
        except :
            NotImplemented

    def __str__(self) -> str:
        return f"({self.x}, {self.y})"
    
    def to_tuple(self) :
        return (self.x, self.y)
    
    def to_list(self) :
        return list(self.to_tuple())
    
    def make_line(point1, point2) :
        return [point1.to_list(), point2.to_list()]