from bezier_curve import BezierCurve
from bokeh.plotting import figure, show
from bokeh.layouts import column, row
from bokeh.io import curdoc
from bokeh.models import ColumnDataSource, CustomJS, Slider

class BokehDrawer :

    def __init__(self) :
        pass

    def drawBezierCurve(Bezier) :
        xs = [[Bezier.memo[j].points[i].x for i in range(0, len(Bezier.memo[j].points), 2)] for j in range(len(Bezier.memo))]
        ys = [[Bezier.memo[j].points[i].y for i in range(0, len(Bezier.memo[j].points), 2)] for j in range(len(Bezier.memo))]

        source = ColumnDataSource(data=dict(
            x = xs[-1], y = ys[-1]
        ))

        source_available = ColumnDataSource(data=dict(x = xs, y = ys))

        curdoc().theme = 'dark_minimal'

        TOOLTIPS = [
            ("index", "$index"),
            ("(x,y)", "(@x, @y)"),
        ]

        iteration = Slider(start=1, end=Bezier.current_iteration, value=1, step=1, title="Iteration")

        callback = CustomJS(args=dict(source=source, source_available = source_available),
                    code="""
            var iter = cb_obj.value;
            var data_visible = source.data;
            var data_available = source_available.data
            data_visible.x = data_available.x[iter];
            data_visible.y = data_available.y[iter];
            source.change.emit();
        """)

        graph = figure(width = 800, height = 600, toolbar_location = "below", tooltips = TOOLTIPS)
        graph.circle('x', 'y', size=7.5, color="blue", alpha=1, source=source)
        graph.line(source=source, line_width = 2)

        iteration.js_on_change('value', callback)

        show(row(graph, column(iteration)))

