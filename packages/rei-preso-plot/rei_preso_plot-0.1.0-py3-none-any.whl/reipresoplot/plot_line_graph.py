import copy
from cycler import cycler
from matplotlib import pyplot as plt
from matplotlib.axes import Axes
import numpy as np
from numpy.typing import ArrayLike, NDArray
from typing import Union

from .transform_to_2d_numpy import transform_to_2d_numpy
from .get_mpl_style_path import get_line_graph_mpl_style_path
from .generate_items_for_focus import generate_items_for_focus


def plot_line_graph(
    y: ArrayLike,
    x: Union[ArrayLike, None] = None,
    legends: Union[list[str], None] = None,
    is_separete_legend: bool = False,
    title: str = "",
    x_label: str = "",
    y_label: str = "",
    focus_indexes: Union[int, list[int], None] = None,
    focus_color: Union[str, None] = None,
    not_focus_color: str = "#c3c3c3",
    ax: Union[Axes, None] = None,
    fig_size: Union[tuple[float], None] = None,
    is_transparent: bool = False,
    savefig_filepath: Union[str, None] = None,
) -> Union[Axes, None]:
    """Plot line graph.

    Parameters
    ----------
    y : ArrayLike
        Data you want to plot.
    x : Union[ArrayLike, None], optional
        x-axis data., by default None
    legends : Union[list[str], None], optional
        legends., by default None
    is_separete_legend : bool, optional
        Flags that do not embed the legend in the figure., by default False
    title : str, optional
        Graph title., by default ""
    x_label : str, optional
        x-axis labels., by default ""
    y_label : str, optional
        y-axis labels., by default ""
    focus_indexes : Union[int, list[int], None], optional
        Indexes of data to be highlighted., by default None
    focus_color : Union[str, None], optional
        Color for emphasis., by default None
    not_focus_color : str, optional
        Color of lines in graphs without emphasis., by default "#c3c3c3"
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
    """
    # reshape data
    y_data: NDArray = transform_to_2d_numpy(copy.copy(y))
    is_x: bool = False if x is None else True
    if is_x:
        x_data: NDArray = transform_to_2d_numpy(copy.copy(x))

    y_data_num: int = y_data.shape[0]
    if is_x:
        x_data_num: int = x_data.shape[0]
        if x_data_num < y_data_num:
            while x_data.shape[0] < y_data_num:
                x_data = np.concatenate([x_data, x_data[-1, :].reshape(1, -1)])
        assert x_data.shape[0] == y_data.shape[0]
        x_data_num: int = x_data.shape[0]

    mpl_style_path: str = get_line_graph_mpl_style_path()
    with plt.style.context(mpl_style_path):
        # for emphasis
        colors, z_orders, font_weights = generate_items_for_focus(
            data_num=y_data_num,
            default_colors=plt.rcParams["axes.prop_cycle"].by_key()["color"],
            focus_indexes=focus_indexes,
            focus_color=focus_color,
            not_focus_color=not_focus_color,
        )

        # generate axes
        is_ax: bool = False if (ax is None) else True
        if not is_ax:
            fig = plt.figure(figsize=fig_size)
            ax = fig.add_subplot(111)

        # plot
        ax.set_prop_cycle(cycler("color", colors))
        if is_x:
            for index, (x, y) in enumerate(zip(x_data, y_data)):
                ax.plot(
                    x,
                    y,
                    marker="o",
                    zorder=z_orders[index],
                )
        else:
            for index, y in enumerate(y_data):
                ax.plot(
                    y,
                    marker="o",
                    zorder=z_orders[index],
                )

        # labels
        ax.set_title(title)
        ax.set_xlabel(x_label)
        ax.set_ylabel(y_label)

        # legends
        if legends is not None:
            if is_separete_legend:
                ax_legend = ax.legend(
                    legends,
                    bbox_to_anchor=(1.02, 1.0),
                    loc="upper left",
                )
                if is_transparent:
                    ax_legend.get_frame().set_alpha(0.0)
            else:
                # colors = np.take(colors, np.arange(len(legends)), mode="wrap")
                for index, legend in enumerate(legends):
                    loc_base: float = y_data.shape[1]
                    x_loc: float = (loc_base - 1.0) + loc_base * 0.025
                    ax.text(
                        x_loc,
                        ax.lines[index].get_data()[1][-1],
                        legend,
                        color=colors[index],
                        va="center",
                        fontsize=18,
                        fontweight=font_weights[index],
                        zorder=z_orders[index],
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
