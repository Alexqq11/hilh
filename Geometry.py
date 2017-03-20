import math
class Point:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.top = y
        self.bottom = y
        self.left = x
        self.right = x

class Rectangle:
    def __init__(self, x , y, width, height):
        self.top = y
        self.bottom = y + height
        self.left = x
        self.right = x + width

    def are_intersected(self, r1, r2):
        return ((r1.bottom >= r2.top) and (r1.right >= r2.left) and (r1.left <= r2.right) and (r1.top <= r2.bottom))

    def check_inside(self, r1, r2):
        return (((r2.bottom <= r1.bottom) and (r2.top >= r1.top)) and (r2.left >= r1.left) and (r2.right <= r1.right))

    def intersection_area(self, r1, r2):
        intersected = self.are_intersected(r1, r2)
        area = 0
        if (intersected):
            index_of_inner = self.index_of_inner_rectangle(r1, r2)
            if (index_of_inner == 0):
                area = self.rectangle_area(r1)
            elif (index_of_inner == 1):
                area = self.rectangle_area(r2)
            else:
                x1 = max(r1.left, r2.left)
                x2 = min(r1.right, r2.right)
                y1 = max(r1.top, r2.top)
                y2 = min(r1.bottom, r2.bottom)
                area = (x1 - x2) * (y1 - y2)
        return area

    def rectangle_area(self, r1):
        return ((abs(r1.top - r1.bottom)) * (abs(r1.right - r1.left)))

    def index_of_inner_rectangle(self, r1, r2):
        if (self.check_inside(r1, r2) and  (not (self.check_inside(r2, r1)))):
            return 1
        elif ((not (self.check_inside(r1, r2)) and self.check_inside(r2, r1))):
            return 0
        elif (self.check_inside(r1, r2) and self.check_inside(r2, r1)):
            return 0
        else:
            return -1
