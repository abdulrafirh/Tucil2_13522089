from bezier_curve import BezierCurve
from point import Point
from visualization import BokehDrawer

Point1 = Point(0, 0)
Point2 = Point(2, 4)
Point3 = Point(4, 0)

curve = BezierCurve([Point1, Point2, Point3], 0)
curve.go_iterate(4)

BokehDrawer.drawBezierCurve(curve)