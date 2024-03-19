import streamlit as st
from matplotlib import collections as mc
import matplotlib.pyplot as plt, mpld3
from mpld3 import plugins
import streamlit.components.v1 as components

import time

from bezier_curve import BezierCurve
from point import Point
import bokehVisualization as bv

@st.cache_data
def get_curve(xy, iteration) :
    curve = BezierCurve([Point(xy[i][0], xy[i][1]) for i in range(len(xy))])
    curve.go_iterate(iteration)
    return curve

st.title(":cyclone: Bezier Curve With Divide and Conquer :cyclone:")
st.subheader(":flying_disc::flying_disc: Input data in the sidebar to start creating Bezier Curve :croissant::croissant:")
num_points = st.sidebar.number_input("Number of Points", 3, 100)

col1, col2 = st.sidebar.columns(2)

xy = [(
    col1.number_input(f"x{i + 1}", value=None), 
    col2.number_input(f"y{i + 1}", value=None)
    ) for i in range(num_points)]

iteration = 1

if (not any(map(lambda x : x[0] == None, xy)) and not any(map(lambda x : x[1] == None, xy))) :
    
    total_iteration = st.sidebar.slider("Number Of Iterations", 1, 50, value=2)

    if (total_iteration > 1) :
        iteration = st.sidebar.slider("Which Iteration to show?", 1, total_iteration, value=total_iteration)

    curve = get_curve(xy, iteration)

    helperMode = st.sidebar.radio("Show Helper Line for :", ["Current Iteration", "All Iteration"], index=None, horizontal=True)

    status = (helperMode == "All Iteration")

    bv.BokehDrawer.drawBezierCurve(curve, iteration, status)
    curve.solve_by_bruteforce(iteration)

    st.sidebar.write(f"Time Taken : {curve.time_taken} ms")
    st.sidebar.write(f"Bruteforce time : {curve.bruteforce_time} ms")
    st.sidebar.write(f"Is brute force and divide and conquer result equals? : :green[{curve.curve_points() == curve.bruteforce_points}]")
    st.caption("Click the labels to the left of the graph to enable/disable certain components!")