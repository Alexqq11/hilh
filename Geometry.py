import math
class Point:
    def __init__(self, x, y):
        self.x = x
        self.y = y


class Rectangle:
    def __init__(self, x , y, width, height):
        self.top = y
        self.bottom = y + height
        self.left = x
        self.right = x + width

    def AreIntersected(self, r1, r2):
        return ((r1.Bottom >= r2.Top) and (r1.Right >= r2.Left) and (r1.Left <= r2.Right) and (r1.Top <= r2.Bottom))

    def Square(self, r1, r2):
        return (((r2.Bottom <= r1.Bottom) & & (r2.Top >= r1.Top)) & & (r2.Left >= r1.Left) & & (r2.Right <= r1.Right))
    def IntersectionSquare(self, r1, r2):
        intersected = self.AreIntersected(r1, r2)
        area = 0
        if (intersected):
            indexOfinner = self.IndexOfInnerRectangle(r1, r2)
            if (indexOfinner == 0):
                area = self.RectangleArea(r1)
            elif (indexOfinner == 1):
                area = self.RectangleArea(r2)
            else:
                x1 = max(r1.Left, r2.Left)
                x2 = min(r1.Right, r2.Right)
                y1 = max(r1.Top, r2.Top)
                y2 = min(r1.Bottom, r2.Bottom)
                area = (x1 - x2) * (y1 - y2)
        return area

    def RectangleArea(self, r1):
        return ((abs(r1.Top - r1.Bottom)) * (abs(r1.Right - r1.Left)))

    def IndexOfInnerRectangle(self, r1, r2):
        if (self.Square(r1, r2) and  (not (self.Square(r2, r1)))):
            return 1
        elif ((not (self.Square(r1, r2)) and self.Square(r2, r1))):
            return 0
        elif (self.Square(r1, r2) and self.Square(r2, r1)):
            return 0
        else:
            return -1
