import copy
from cycler import cycler
from matplotlib import pyplot as plt
from matplotlib.axes import Axes
import numpy as np
from numpy.typing import ArrayLike, NDArray
from typing import Union

from .transform_to_2d_numpy import transform_to_2d_numpy
from .get_mpl_style_path import get_bar_graph_mpl_style_path
from .generate_items_for_focus import generate_items_for_focus


def plot_bar_graph(
    y: ArrayLike,
    x: Union[ArrayLike, None] = None,
    legends: Union[list[str], None] = None,
    bar_width: float = 0.75,
    title: str = "",
    x_label: str = "",
    y_label: str = "",
    focus_indexes: Union[int, list[int], None] = None,
    color: Union[str, None] = None,
    not_focus_color: str = "#c3c3c3",
    ax: Union[Axes, None] = None,
    fig_size: Union[tuple[float], None] = None,
    is_transparent: bool = False,
    savefig_filepath: Union[str, None] = None,
) -> Union[Axes, None]:
    """Plot bar graph.

    Parameters
    ----------
    y : ArrayLike
        Data you want to plot.
    x : Union[ArrayLike, None], optional
        x-axis data., by default None
    legends : Union[list[str], None], optional
        legends., by default None
    bar_width : float, optional
        Width of bar., by default 0.75
    title : str, optional
        Graph title., by default ""
    x_label : str, optional
        x-axis labels., by default ""
    y_label : str, optional
        y-axis labels., by default ""
    focus_indexes : Union[int, list[int], None], optional
        Indexes of data to be highlighted., by default None
    color : Union[str, None], optional
        Color of bars in graph., by default None
    not_focus_color : str, optional
        Color of bars in graphs without emphasis., by default "#c3c3c3"
    ax : Union[Axes, None], optional
        Axis of matplotlib., by default None
    fig_size : Union[tuple[float], None], optional
        Figure Size [inch]., by default None
    is_transparent : bool, optional
        Flag to make background transparent., by default False
    savefig_filepath : Union[str, None], optional
        Name for saving the figure., by default None

    Returns
    -------
    Union[Axes, None]
        Axis of matplotlib.

    Raises
    ------
    ValueError
        When y is not 1-dimensional data.
    ValueError
        When x is not 1-dimensional data.
    """
    # reshape data
    y_data: NDArray = transform_to_2d_numpy(copy.copy(y))
    if y_data.shape[0] != 1:
        raise ValueError('"y" must be 1-dimensional.')
    y_data = y_data[0, :]
    data_num = len(y_data)

    is_x: bool = False if x is None else True
    if is_x:
        x_data: NDArray = transform_to_2d_numpy(copy.copy(x))
        if x_data.shape[0] != 1:
            raise ValueError('"x" must be 1-dimensional.')
        x_data = x_data[0, :]
    else:
        x_data = np.arange(data_num)

    mpl_style_path: str = get_bar_graph_mpl_style_path()
    with plt.style.context(mpl_style_path):
        # for emphasis
        if color is None:
            color = plt.rcParams["axes.prop_cycle"].by_key()["color"][0]
        colors, z_orders, font_weights = generate_items_for_focus(
            data_num=data_num,
            default_colors=[color] * data_num,
            focus_indexes=focus_indexes,
            focus_color=color,
            not_focus_color=not_focus_color,
        )

        # generate axes
        is_ax: bool = False if (ax is None) else True
        if not is_ax:
            fig = plt.figure(figsize=fig_size)
            ax = fig.add_subplot(111)

        # plot
        ax.set_prop_cycle(cycler("color", colors))
        ax.bar(x_data, y_data, width=bar_width, color=colors)

        # labels
        ax.set_title(title)
        ax.set_xlabel(x_label)
        ax.set_ylabel(y_label)

        # legends
        if legends is not None:
            ax_legend = ax.legend(
                legends,
                bbox_to_anchor=(1.02, 1.0),
                loc="upper left",
            )
            if is_transparent:
                ax_legend.get_frame().set_alpha(0.0)

        y_max = np.max(y_data)
        for x, y, color in zip(x_data, y_data, colors):
            y_loc = y + y_max * 0.04
            ax.text(
                x,
                y_loc,
                f"{round(y,2)}",
                ha="center",
                va="bottom",
                fontsize=18,
                color=color,
            )

        # show
        if not is_ax:
            fig.show()
            if savefig_filepath is not None:
                fig.savefig(
                    savefig_filepath,
                    transparent=is_transparent,
                )
            return
    return ax
