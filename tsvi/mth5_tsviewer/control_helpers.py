"""
The Controller component is responsible for responding to user input and updating
the Model component accordingly. It typically does not have direct access to the
View components, but instead interacts with them through a well-defined interface.
"""

def list_h5s_to_plot(channels_list):
    """

    Parameters
    ----------
    channels_list: string representation of the data paths associated with channels

    Returns
    -------
    used_files: list
        Each element of the list is the name of an mth5 file that is associated with
        at least one channel in the list.

    """
    used_files = []
    for selected_channel in channels_list:
        file_name = selected_channel.split("/")[0]
        if file_name not in used_files:
            used_files.append(file_name)
    return used_files


def set_channel_paths(df, file_name, file_version):
    """
    ToDo: Consider making a class ChannelPathHandler
    That has set_channel_paths method,
    and also does the string unpacking in parse_channel_path below
    Parameters
    ----------
    df: pandas.core.frame.DataFrame from mth5 channel_summary

    Returns
    -------

    """
    df["file"] = file_name
    if file_version == "0.1.0":
        df["channel_path"] = (df["file"] + "/" +
                              df["station"] + "/" +
                              df["run"] + "/" +
                              df["component"])
    elif file_version == "0.2.0":
        df["channel_path"] = (df["file"] + "/" +
                              df["survey"] + "/" +
                              df["station"] + "/" +
                              df["run"] + "/" +
                              df["component"])
    df.set_index("channel_path", inplace = True)
    return

def parse_channel_path(selected_channel):
    try: # m.file_version == "0.1.0"
        selected_file, station, run, channel = selected_channel.split("/")
        survey = None
    except ValueError: # m.file_version == "0.2.0"
        selected_file, survey, station, run, channel = selected_channel.split("/")
    return selected_file, survey, station, run, channel





def invert(event, data):
    data = -1 * data
    return data
