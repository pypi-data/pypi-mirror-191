import os.path


def get_line_graph_mpl_style_path() -> str:
    """Get the path to the matplotlibrc file for line graphs.

    Returns
    -------
    str
        The path to the matplotlibrc file for line graphs.
    """
    return (
        os.path.dirname(os.path.abspath(__file__))
        + "/mplstyle/nakurei_line_graph.mplstyle"
    )


def get_bar_graph_mpl_style_path() -> str:
    """Get the path to the matplotlibrc file for bar graphs.

    Returns
    -------
    str
        The path to the matplotlibrc file for bar graphs.
    """
    return (
        os.path.dirname(os.path.abspath(__file__))
        + "/mplstyle/nakurei_bar_graph.mplstyle"
    )
