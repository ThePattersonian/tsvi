"""
The Model component represents the underlying data and business logic of the
application. It is responsible for storing and manipulating data, and for
providing an interface for the View and Controller components to interact with that data.
"""
import panel as pn

from tsvi.mth5_tsviewer.control_helpers import list_h5s_to_plot
from tsvi.mth5_tsviewer.control_helpers import parse_channel_path

from mth5.mth5 import MTH5

def get_templates_dict():
    """
     Make template choice dictionary
     More information about template choices and functionality is here:
     https://panel.holoviz.org/user_guide/Templates.html
     Returns
     templates: dict

    -------

    """
    templates = {}
    templates["bootstrap"] = pn.template.BootstrapTemplate
    templates["fast"] = pn.template.FastListTemplate
    templates["golden"] = pn.template.GoldenTemplate
    templates["grid"] = pn.template.FastGridTemplate
    return templates


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




def get_mth5_data_as_xarrays(selected_channels, file_paths):
    """
    ToDo:
    - This can be modified in future to support chunking read in
    - interaction with the intake package belongs here.
    - This function works on multiple mth5 files in sequence. Another way to do this
    would to be to invert the two for loops so that the outer loop iterates over
    selected_channels first and then a one-line function accesses the data for that
    channel.

    Parameters
    ----------
    selected_channels: list
    file_paths
    kwargs

    Returns
    -------
    out_dict: dictionary
        Keyed by channel name, value is xarray associated with that channel
    """
    out_dict = {}
    used_files = list_h5s_to_plot(selected_channels)
    for file in used_files:
        m = MTH5()
        m.open_mth5(file_paths[file], mode = "r")
        for selected_channel in selected_channels:
            selected_file, survey, station, run, channel = parse_channel_path(selected_channel)
            if selected_file == file:
                data = m.get_channel(station, run, channel, survey=survey).to_channel_ts().to_xarray()
                # data = data.rename(data.attrs["mth5_type"]): "ex"--> "Electric"
                #self.xarrays.append(data)
                out_dict[selected_channel] = data
        m.close_mth5()
    return out_dict

# def get_card_controls():
# THe idea here is to track the buttons /widgets that we want beside the plot
#     annotate_button = pn.widgets.Button(name = "Annotate", button_type = "primary", width = 100)
#     invert_button = pn.widgets.Button(name = "Invert", button_type = "primary", width = 100)
#     # def invert(self, *args, **params):
#     #   data = -1 * data
#     # invert_button.on_click(invert(event, data))
#     controls = pn.Column(annotate_button,
#                          invert_button,
#                          sizing_mode = "fixed", width = 200,)
#     return controls