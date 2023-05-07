"""
The View component is responsible for presenting data to the user. The View component is
 also responsible for capturing user input and passing it to the Controller component
 for further processing.
"""
import holoviews as hv
import hvplot
import panel as pn

from tsvi.mth5_tsviewer.control_helpers import list_h5s_to_plot
from tsvi.mth5_tsviewer.control_helpers import parse_channel_path
from tsvi.mth5_tsviewer.model_helpers import get_mth5_data_as_xarrays

def cpu_usage_widget():
    cpu_usage = pn.indicators.Number(
        name="CPU",
        value=0,
        format="{value}%",
        colors=[(50, "green"), (75, "orange"), (100, "red")],
        font_size="13pt",
        title_size="8pt",
        width=50,
    )
    return cpu_usage

def memory_usage_widget():
    memory_usage= pn.indicators.Number(
        name="Memory",
        value=0,
        format="{value}%",
        colors=[(50, "green"), (75, "orange"), (100, "red")],
        font_size="13pt",
        title_size="8pt",
        width=50,
    )
    return memory_usage


def channel_summary_columns_to_display():
    # Configure the displayed columns in the Channels Tab
    displayed_columns = ["survey", "station", "run",
                         #"latitude", "longitude", "elevation",
                         "component",
                         "start", "end", "n_samples", "sample_rate",
                         "measurement_type",
                         #"azimuth", "tilt",
                         #"units"
                         ]
    return displayed_columns


# def plot_bokeh(xarray, shaded = False, shared = False):
#     plot = xarray.hvplot(
#                           width = 900,
#                           height = 450,
#                           datashade = shaded,
#                           shared_axes = shared
#                          )
#     return plot


def make_plots(obj):
    """
    Gets the data and plots it.

    ToDo: Factor into
    - get data
    - preprocess
    - plot data

    takes a list of mth5 files and then it converts that list to channels,
    it needs to know what channels were used (self.cahnnels


    Parameters
    ----------
    obj: __main__.Tsvi object


    """
    hv.output(backend = obj.plotting_library.value)
    new_cards  = []
    used_files = list_h5s_to_plot(obj.channels.value)

    # data_dict = preprocess(data_dict, obj.subtract_mean_checkbox.value)
    # plot_cards = make_plots(data_dict)

    # Keyed with the selected_channel from below
    data_dict = get_mth5_data_as_xarrays(obj.channels.value, obj.file_paths)
    # data_dict = preprocess(data_dict, obj.subtract_mean_checkbox.value)
    # plot_cards = make_plots(data_dict)
    # from holoviews.operation.datashader import datashade
    for selected_channel,data in data_dict.items():
        selected_file, survey, station, run, channel = parse_channel_path(selected_channel)
        ylabel = data.type
        if obj.subtract_mean_checkbox.value == True:
            data = data - data.mean()
            plot = hvplot.hvPlot(data,
                                 width = obj.plot_width,
                                 height = obj.plot_height,
                                 cmap = obj.colormap,
                                 ylabel = ylabel)
            #plot = datashade(hv.Curve(data))
            obj.plots[selected_channel] = plot
            if obj.plotting_library.value == "bokeh":
                bound_plot = pn.bind(plot,
                                     datashade = obj.datashade_checkbox,
                                     shared_axes = obj.shared_axes_checkbox)

            elif obj.plotting_library.value == "matplotlib":
                fig = Figure(figsize = (8,6))

            invert_button = pn.widgets.Button(name="Invert", button_type="primary", width=100)

            # invert_button.on_click(invert(event, data))
            controls = pn.Column(
                invert_button,
                sizing_mode = "fixed", width = 200,)
            plot_pane = pn.Pane(bound_plot)
            plot_tab = pn.Row(plot_pane,
                              controls,
                              name = run + "/" + channel)
            if obj.annotatable:
                obj.annotators[selected_channel] = hv.annotate.instance()
                note_tab = pn.Pane(obj.annotators[selected_channel].compose(plot.line(datashade=False).opts(width = 700, height = 200),
                                                                            obj.annotators[selected_channel](
                                                                                hv.Rectangles(data= []).opts(alpha=0.5),
                                                                                annotations = ["Label"],
                                                                                name = "Notes")),
                                   name = "Notes")

                tabs = pn.Tabs(plot_tab,
                               note_tab)
            else:
                tabs = pn.Tabs(plot_tab)
            new_card = pn.Card(tabs,
                               title = selected_channel)

            new_cards.append(new_card)


    obj.plot_cards = new_cards
    return


