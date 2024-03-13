from bezier_curve import BezierCurve
from bokeh.plotting import figure, show
from bokeh.layouts import column, row
from bokeh.io import curdoc
from bokeh.models import ColumnDataSource, CustomJS, Slider

class BokehDrawer :

    def __init__(self) :
        pass

    def drawBezierCurve(Bezier) :

        pivot_point = Bezier.memo[0].points[1]
        xs = [[Bezier.memo[j].points[i].x for i in range(0, len(Bezier.memo[j].points), 2)] for j in range(len(Bezier.memo))]
        ys = [[Bezier.memo[j].points[i].y for i in range(0, len(Bezier.memo[j].points), 2)] for j in range(len(Bezier.memo))]

        mid_xs = [[Bezier.memo[j].points[i].x for i in range(1, len(Bezier.memo[j].points), 2)] for j in range(len(Bezier.memo))]
        mid_ys = [[Bezier.memo[j].points[i].y for i in range(1, len(Bezier.memo[j].points), 2)] for j in range(len(Bezier.memo))]

        source = ColumnDataSource(data=dict(
            x = xs[1], y = ys[1]
        ))

        pivot_source = ColumnDataSource(data=dict(
            x = [pivot_point.x],
            y = [pivot_point.y]
        ))

        midpoint_source = ColumnDataSource(data=dict(
            x = mid_xs[1],
            y = mid_ys[1]
        ))

        midpoint_source_available = ColumnDataSource(data=dict(x = mid_xs, y = mid_ys))
        source_available = ColumnDataSource(data=dict(x = xs, y = ys))

        curdoc().theme = 'dark_minimal'

        TOOLTIPS = [
            ("index", "$index"),
            ("(x,y)", "(@x, @y)"),
        ]

        iteration = Slider(start=1, end=Bezier.current_iteration, value=1, step=1, title="Iteration")

        callback = CustomJS(args=dict(source=source, source_available = source_available, midpoint_source = midpoint_source, midpoint_source_available = midpoint_source_available),
                    code="""
            var iter = cb_obj.value;

            var data_visible = source.data;
            var data_available = source_available.data
            data_visible.x = data_available.x[iter];
            data_visible.y = data_available.y[iter];

            var midpoint_data_source = midpoint_source.data;
            var midpoint_data_available = midpoint_source_available.data
            midpoint_data_source.x = midpoint_data_available.x[iter];
            midpoint_data_source.y = midpoint_data_available.y[iter];

            midpoint_source.change.emit();
            source.change.emit();
        """)

        graph = figure(width = 800, height = 600, toolbar_location = "below", tooltips = TOOLTIPS)

        # Draw Objects
        graph.circle('x', 'y', size=7.5, color="blue", alpha=1, source=source, legend_label = "Bezier Curve Nodes")
        graph.circle('x', 'y', size = 7.5, color = "red", alpha=1, source=pivot_source, legend_label = "Control Point")
        graph.line(source=source, line_width = 2, legend_label = "Bezier Curve")

        graph.circle('x', 'y', size=7.5, color="green", alpha=1, source=midpoint_source, legend_label = "Helper Points")
        graph.line(source=midpoint_source, line_width = 2, legend_label = "Helper Lines")

        # Style Graph
        graph.border_fill_color = "whitesmoke"
        graph.min_border_left = 40

        graph.legend.location = "top_left"
        graph.legend.click_policy="hide"

        iteration.js_on_change('value', callback)

        show(row(column(iteration), graph, sizing_mode="scale_both"))

