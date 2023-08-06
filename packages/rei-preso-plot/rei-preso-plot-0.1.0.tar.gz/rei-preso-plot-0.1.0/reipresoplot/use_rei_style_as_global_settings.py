from matplotlib import pyplot as plt

from .get_mpl_style_path import (
    get_line_graph_mpl_style_path,
    get_bar_graph_mpl_style_path,
)


def use_line_graph_style_as_global_settings() -> None:
    mpl_style_path: str = get_line_graph_mpl_style_path()
    plt.style.use(mpl_style_path)


def use_bar_graph_style_as_global_settings() -> None:
    mpl_style_path: str = get_bar_graph_mpl_style_path()
    plt.style.use(mpl_style_path)
