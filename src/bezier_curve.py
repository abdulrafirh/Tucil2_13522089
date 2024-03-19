import typing
import math
from point import Point
import streamlit as st
import matplotlib.pyplot as plt
import time

class BezierCurve :

    # Drawn Points : Points in order of finding out
    # Points : All Points in order from start to finish

    def __init__(self, points : list[Point], iteration = 0, degree = None) :
        self.points = points
        self.original_points = self.points
        self.current_iteration = iteration
        self.drawn_points = []
        self.memo = []
        if (degree) :
            self.degree = degree
        else :
            self.degree = len(points) - 1

    def merge_curve(curve1 : "BezierCurve", curve2 : "BezierCurve") -> "BezierCurve" :
        if (curve1.current_iteration == curve2.current_iteration and curve1.degree == curve2.degree) :
            points = curve1.points + curve2.points[1:]

            result = BezierCurve(points, curve1.current_iteration + 1, curve1.degree)
            result.drawn_points = []
            for i in range(len(curve1.drawn_points)) :
                if (i == 0) :
                    result.drawn_points.append(curve1.drawn_points[i] + curve2.drawn_points[i][1:])
                else :
                    result.drawn_points.append(curve1.drawn_points[i] + curve2.drawn_points[i])

            return result

    def go_next(self) :
        if (self.current_iteration == 0) :
            self.base_case()
        else :
            first_half_points = self.points[0:len(self.points)//2 + 1]
            second_half_points = self.points[len(self.points)//2:]

            first_half_curve = BezierCurve(first_half_points, self.current_iteration - 1, self.degree)
            second_half_curve = BezierCurve(second_half_points, self.current_iteration - 1, self.degree)

            first_half_curve.go_iterate(self.current_iteration)
            second_half_curve.go_iterate(self.current_iteration)

            result = BezierCurve.merge_curve(first_half_curve, second_half_curve)
            self.points = result.points
            self.current_iteration = result.current_iteration
            self.drawn_points = result.drawn_points
        self.memo.append(self.copy_curve())

    def base_case(self) :
        self.drawn_points = [self.points]
        self.memo.append(self.copy_curve())

        self.drawn_points = []
        current_points = self.points
        temp = [self.points[i] for i in range(len(self.points))]
        self.points = temp
        self.drawn_points.append([temp[i] for i in range(len(temp))])
        for i in range(self.degree) :
            new_points = []
            for j in range(len(current_points) - 1) :
                new_points.append(Point.midpoint(current_points[j], current_points[j + 1]))
            self.drawn_points.append(new_points)
            current_points = new_points
        self.points = BezierCurve.get_points_from_drawn_points(self.drawn_points)
        self.current_iteration = 1

    def get_points_from_drawn_points(drawn_points) :
        points = []
        for i in range(len(drawn_points)) :
            points.append(drawn_points[i][0])
        for i in range(len(drawn_points) - 2, -1, -1) :
            points.append(drawn_points[i][-1])
        return points
    
    def go_iterate(self, n : int) :
        
        start = time.time_ns()
        while (self.current_iteration != n) :
            self.go_next()
        self.time_taken = (time.time_ns() - start)/1000000

    def copy_curve(self) :
        new_points = [self.points[i] for i in range(len(self.points))]
        new_drawn_points = []
        for points in self.drawn_points :
            new_drawn_points.append([point for point in points])

        result = BezierCurve(new_points, self.current_iteration, self.degree)
        result.drawn_points = new_drawn_points

        return result

    def __str__(self) -> str:
        result = ""
        
        curve_points = self.curve_points()
        for point in curve_points :
            result += str(point)
            if (point != curve_points[-1]) :
                result += "\n"

        return result

    def curve_points(self) :
        return [self.points[i] for i in range(0, len(self.points), self.degree)]
    
    def curve_lines(self) :
        curvePoints = self.curve_points()
        return [Point.make_line(curvePoints[i], curvePoints[i + 1]) for i in range(0, len(curvePoints) - 1)]
    
    def current_iteration_helper_points(self) :
        if (self.current_iteration == 0) :
            return []
        curve_points = self.curve_points()

        result = []
        
        for points in self.drawn_points :
            for point in points :
                if point not in curve_points :
                    result.append(point)
        return result
    
    def cumulative_helper_points(self, iteration) :
        points = []
        for i in range(1, iteration + 1) :
            curr_helper_points = self.memo[i].current_iteration_helper_points()
            for point in curr_helper_points :
                if (point not in points) :
                    points.append(point)
        return points
    
    def current_iteration_helper_lines(self) :

        if self.current_iteration == 0 :
            return []
        else :
            lines = []
            curve_lines = self.curve_lines()

            for points in self.drawn_points[:-1] :
                for i in range(len(points) - 1) :
                    line = Point.make_line(points[i], points[i + 1])
                    if line not in curve_lines :
                        lines.append(line)
            
            return lines
        
    def cumulative_helper_lines(self, iteration) :
        lines = []
        for i in range(1, iteration + 1) :
            curr_helper_lines = self.memo[i].current_iteration_helper_lines()
            for line in curr_helper_lines :
                if (line not in lines) :
                    lines.append(line)

        return lines
    
    def solve_by_bruteforce(self, iteration) :

        start_time = time.time_ns()
        incrementor = 1/(2**iteration)
        t = 0

        self.bruteforce_points = []
        n = len(self.original_points) - 1

        while (t <= 1) :
            new_x = 0
            new_y = 0
            for i in range(n + 1) :
                new_x += math.comb(n, i) * ((1-t)**(n - i)) * (t ** i) * self.original_points[i].x
                new_y += math.comb(n, i) * ((1-t)**(n - i)) * (t ** i) * self.original_points[i].y
            self.bruteforce_points.append(Point(new_x, new_y))
            t += incrementor

        self.bruteforce_time = (time.time_ns() - start_time)/1000000
        return self.bruteforce_points