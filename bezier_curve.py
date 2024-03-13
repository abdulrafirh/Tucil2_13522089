import typing
import math
from point import Point

class BezierCurve :

    def __init__(self, points : list[Point], iteration = 0) :
        self.points = points
        self.current_iteration = iteration
        self.memo = []

    def merge_curve(curve1 : "BezierCurve", curve2 : "BezierCurve") -> "BezierCurve" :
        if (curve1.current_iteration == curve2.current_iteration) :
            points = curve1.points + curve2.points[1:]

            result = BezierCurve(points, curve1.current_iteration + 1)

            return result

    def go_next(self) :

        if (self.current_iteration == 0) :
            
            self.memo.append(self.copy_curve())
            midpoint_one = self.points[0].midpoint(self.points[1])
            midpoint_two = self.points[1].midpoint(self.points[2])
            midpoint_final = midpoint_one.midpoint(midpoint_two)

            self.points = (self.points[0], midpoint_one, midpoint_final, midpoint_two, self.points[2])
            self.current_iteration = 1
            self.memo.append(self.copy_curve())

        else :
            first_half_points = self.points[0:len(self.points)//2 + 1]
            second_half_points = self.points[len(self.points)//2:]

            first_half_curve = BezierCurve(first_half_points, math.log2(len(self.points)//2) - 1)
            second_half_curve = BezierCurve(second_half_points, math.log2(len(self.points)//2) - 1)

            first_half_curve.go_iterate(self.current_iteration)
            second_half_curve.go_iterate(self.current_iteration)

            result = BezierCurve.merge_curve(first_half_curve, second_half_curve)
            self.points = result.points
            self.current_iteration = result.current_iteration
            self.memo.append(self.copy_curve())
        
    def go_iterate(self, n : int) :
        
        while (self.current_iteration != n) :
            self.go_next()

    def copy_curve(self) :
        new_points = [self.points[i] for i in range(len(self.points))]
        return BezierCurve(new_points, self.current_iteration)

    def __str__(self) -> str:
        result = ""
        
        for i in range(0, len(self.points), 2) :
            result += str(self.points[i])
            if (i != len(self.points) - 1) :
                result += "\n"

        return result



