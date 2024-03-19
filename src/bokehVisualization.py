from bezier_curve import BezierCurve
from bokeh.plotting import figure
from bokeh.models import ColumnDataSource
import streamlit as st

class BokehDrawer :

    def __init__(self) :
        pass

    def drawBezierCurve(Bezier: BezierCurve, iteration, all_iteration_helper = False) :

        xs = list(map(lambda x : x.x, Bezier.memo[iteration].curve_points()))
        ys = list(map(lambda x : x.y, Bezier.memo[iteration].curve_points()))

        source = ColumnDataSource(data=dict(
            x = xs, y = ys
        ))

        pivot_points = Bezier.memo[0].points[1:-1]
        pivot_source = ColumnDataSource(data=dict(
            x = list(map(lambda x : x.x, pivot_points)),
            y = list(map(lambda x : x.y, pivot_points))
        ))


        TOOLTIPS = [
            ("index", "$index"),
            ("(x,y)", "(@x, @y)"),
        ]

        graph = figure(width = 800, height = 600, toolbar_location = "below", tooltips = TOOLTIPS)

        # Draw Objects
        graph.line(source=source, line_width = 2, legend_label = "Bezier Curve", color = "#83c9ff")
        graph.circle('x', 'y', size = 7.5, color = "red", alpha=1, source=pivot_source, legend_label = "Control Points")

        #7DEFA1

        if (iteration <= 10) :

            if all_iteration_helper :
                helper_lines = Bezier.cumulative_helper_lines(iteration)
                helper_points = Bezier.cumulative_helper_points(iteration)
            else :
                helper_lines = Bezier.memo[iteration].current_iteration_helper_lines()
                helper_points = Bezier.memo[iteration].current_iteration_helper_points()

            helper_points_source = ColumnDataSource(data=dict(
                x = list(map(lambda x : x.x, helper_points)),
                y = list(map(lambda x : x.y, helper_points))
            ))

            graph.segment(
                x0=list(map(lambda x: x[0][0], helper_lines)), y0=list(map(lambda x: x[0][1], helper_lines)), 
                x1=list(map(lambda x: x[1][0], helper_lines)), y1=list(map(lambda x: x[1][1], helper_lines)), 
                color="#7DEFA1", line_width=3, legend_label = "Helper Lines"
            )
        
            graph.circle('x', 'y', size=7.5, color="#ffabab", alpha=1, source=source, legend_label = "Bezier Curve Points")
            graph.circle('x', 'y', size = 7.5, color = "#FFD16A", alpha=1, source=helper_points_source, legend_label = "Helper Points")

        # Style Graph
        graph.add_layout(graph.legend[0], 'left')
        graph.legend.click_policy="hide"
        graph.legend.background_fill_color = "gray"
        graph.legend.background_fill_alpha = 0.2
        graph.legend.border_line_color = "black"
        graph.legend.label_text_color = "whitesmoke"

        graph.yaxis.major_label_text_color = "#c7ccd2"
        graph.xaxis.major_label_text_color = "#c7ccd2"
        graph.background_fill_color = "#0e1117"
        graph.border_fill_color = "#0e1117"

        st.bokeh_chart(graph)        

