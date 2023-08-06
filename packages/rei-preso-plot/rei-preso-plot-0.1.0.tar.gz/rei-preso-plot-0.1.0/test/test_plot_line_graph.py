from matplotlib import pyplot as plt
import os
from numpy.typing import ArrayLike

from reipresoplot import plot_line_graph, get_line_graph_mpl_style_path


def test_plot_line_graph():
    y_data: ArrayLike = [
        [80, 70, 60, 90, 70],
        [50, 60, 70, 80, 90],
        [90, 95, 90, 80, 100],
    ]
    x_data: list[str] = ["April", "May", "June", "July", "August"]
    legends: list[str] = ["AA", "BB", "CC"]
    title: str = "Test Scores"
    x_label: str = "Month held"
    y_label: str = "Score [points]"

    result_dir = "test/result/"
    os.makedirs(result_dir, exist_ok=True)

    plot_line_graph(
        y_data,
        x=x_data,
        legends=legends,
        title=title,
        x_label=x_label,
        y_label=y_label,
        focus_indexes=[1],
        focus_color="#00796B",
        savefig_filepath=os.path.join(result_dir, "line_graph_1.png"),
    )

    plot_line_graph(
        y_data,
        x=x_data,
        legends=legends,
        title=title,
        x_label=x_label,
        y_label=y_label,
        focus_indexes=[1, 2],
        savefig_filepath=os.path.join(result_dir, "line_graph_2.png"),
    )

    plot_line_graph(
        y_data,
        legends=legends,
        is_separete_legend=True,
        savefig_filepath=os.path.join(result_dir, "line_graph_3.png"),
    )

    mpl_style_path: str = get_line_graph_mpl_style_path()
    with plt.style.context(mpl_style_path):
        fig = plt.figure()
        ax = fig.add_subplot(111)
        ax = plot_line_graph(
            y_data,
            legends=legends,
            is_separete_legend=True,
            ax=ax,
            is_transparent=True,
        )
        ax.set_ylim([0.0, 100.0])
        fig.show()
        fig.savefig(
            os.path.join(result_dir, "line_graph_4.png"),
            transparent=True,
        )
