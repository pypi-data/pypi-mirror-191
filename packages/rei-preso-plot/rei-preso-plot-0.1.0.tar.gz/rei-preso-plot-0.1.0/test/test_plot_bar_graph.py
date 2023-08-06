from matplotlib import pyplot as plt
import os
from numpy.typing import ArrayLike

from reipresoplot import plot_bar_graph, get_bar_graph_mpl_style_path


def test_plot_bar_graph():
    y_data: ArrayLike = [80, 70, 60, 90, 70]
    x_data: list[str] = ["April", "May", "June", "July", "August"]
    legends: list[str] = ["AA", "BB", "CC"]
    title: str = "Test Scores"
    x_label: str = "Month held"
    y_label: str = "Score [points]"

    result_dir = "test/result/"
    os.makedirs(result_dir, exist_ok=True)

    plot_bar_graph(
        y_data,
        x=x_data,
        legends=legends,
        title=title,
        x_label=x_label,
        y_label=y_label,
        focus_indexes=[1],
        color="#AFB42B",
        savefig_filepath=os.path.join(result_dir, "bar_graph_1.png"),
    )

    plot_bar_graph(
        y_data,
        x=x_data,
        legends=legends,
        title=title,
        x_label=x_label,
        y_label=y_label,
        focus_indexes=[1, 2],
        savefig_filepath=os.path.join(result_dir, "bar_graph_2.png"),
    )

    plot_bar_graph(
        y_data,
        legends=legends,
        savefig_filepath=os.path.join(result_dir, "bar_graph_3.png"),
    )

    mpl_style_path: str = get_bar_graph_mpl_style_path()
    with plt.style.context(mpl_style_path):
        fig = plt.figure()
        ax = fig.add_subplot(111)
        ax = plot_bar_graph(
            y_data,
            legends=legends,
            ax=ax,
            is_transparent=True,
        )
        ax.set_ylim([0.0, 100.0])
        fig.show()
        fig.savefig(
            os.path.join(result_dir, "bar_graph_4.png"),
            transparent=True,
        )
