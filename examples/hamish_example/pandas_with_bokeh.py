import pandas_skeleton as ps
import tree_maker as tm
from pandas import DataFrame

from bokeh.layouts import column
from bokeh.models import ColumnDataSource, Slider, WheelZoomTool, BoxZoomTool, Button, PanTool
from bokeh.plotting import figure
from bokeh.themes import Theme
from bokeh.io import show, output_notebook
from bokeh.models import Select

def bkapp(doc, root, last_key, choose_color):
    """
    This creates an interactive plot showing a tree of jobs in a 'flower' shape.
    """
    global my_df
    global source
    global my_df_plot
    
    try:
        ps.create_tree(root)
    except:
        raise Exception('Sorry, I need a root of a tree!')
        
    x_values, y_values, path = ps.create_xypath(root)
    my_colors = ps.create_color(root)
    angles = ps.create_tree_cartesian(root)
    
    my_df = ps.create_df(root, path, x_values, y_values, my_colors)
    
    del my_df['handle']
    
    my_df_plot = my_df

        
    def callback(attr, _, index_list):
        global my_df
        global my_df_selected
        global my_df_plot
        source.data = ColumnDataSource.from_df(my_df_plot)
        my_df_selected = my_df_plot.loc[index_list]

    def initialise():
        global my_df_plot
        global my_df
        my_df_plot = ps.update(my_df_plot, last_key, choose_color)
        my_df = ps.update(my_df, last_key, choose_color)
    
    initialise()
    
    source = ColumnDataSource(data=my_df_plot)
    
    TOOLTIPS = [
    ('index', "@index"),
    ('status', "@status"),
    ('path', "@path")
]
    plot = figure(plot_width=400, plot_height=400, tools="lasso_select", title="Select Here", tooltips = TOOLTIPS)
    plot.circle('x', 'y', source=source, alpha=0.6, color = 'color')
    plot.add_tools(BoxZoomTool(), WheelZoomTool(), PanTool())

    source.selected.on_change('indices', callback)
    
    select = Select(title="Option:", value="plot", options=["full_df", f"{last_key}", f"not {last_key}"])

    def callback1(attr, old, new):
        global my_df_plot
        if new == "full_df":
            my_df_plot = my_df.copy()
        if new == f"{last_key}":
            my_df_plot = my_df[my_df.status == last_key].copy()
        if new == f"not {last_key}":
            my_df_plot = my_df[my_df.status != last_key].copy()
        my_df_plot.reset_index(drop=True, inplace=True)
        source.data = ColumnDataSource.from_df(my_df_plot)

    select.on_change('value', callback1)
    
    button = Button(label="Update", button_type="success")

    button.on_click(initialise)

    doc.add_root(column(plot, button, select))
    