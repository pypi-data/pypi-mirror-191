# rei-preso-plot

[![Publish Python distributions to PyPI](https://github.com/NakuRei/rei-preso-plot/actions/workflows/publish-to-test-pypi.yml/badge.svg)](https://github.com/NakuRei/rei-preso-plot/actions/workflows/publish-to-test-pypi.yml)
![License](https://img.shields.io/github/license/NakuRei/rei-preso-plot)

Python package for drawing graphs for presentation materials with `matplotlib`.

## Description

A package for creating graphs suitable for presentation materials with `matplotlib`.
The created graph can be directly placed on a presentation slide with a nice design.

## Requirement

- Python 3.11.1
- matplotlib 3.6.3

## Installation

```shell
pip install rei-preso-plot
```

## Usage

### Using graph functions

Graph functions.
Can emphasize parts by adding color or embedding legends in line graphs.
When passing `matplotlib.axes.Axes` to the argument ax, it returns the `matplotlib.axes.Axes`. Therefore, using the functions of `matplotlib`, you can specify the drawing range, etc., after these functions.

| Function                       | Description                 |
| :----------------------------- | :-------------------------- |
| `reipresoplot.plot_line_graph` | Line graph drawing function |
| `reipresoplot.plot_bar_graph`  | Bar graph drawing function  |

| Code                                      | Graph                          |
| :---------------------------------------- | :----------------------------- |
| [for_line_graph.py][line_graph_code_link] | ![Line graph][line_graph_link] |
| [for_bar_graph.py][bar_graph_code_link]   | ![Bar graph][bar_graph_link]   |

[line_graph_link]: https://github.com/NakuRei/rei-preso-plot/raw/main/examples/using_graph_functions/result/plot_line_graph.png
[line_graph_code_link]: https://github.com/NakuRei/rei-preso-plot/blob/main/examples/using_graph_functions/for_line_graph.py
[bar_graph_code_link]: https://github.com/NakuRei/rei-preso-plot/blob/main/examples/using_graph_functions/for_bar_graph.py
[bar_graph_link]: https://github.com/NakuRei/rei-preso-plot/raw/main/examples/using_graph_functions/result/plot_bar_graph.png

### Using matplotlibrc files

By reading `matplotlibrc` files, you can customize the `matplotlib` style as a whole, i.e. without specifying it with `rcParams`, etc.
For details, see [Matplotlib documentation](https://matplotlib.org/stable/tutorials/introductory/customizing.html).

| Function                                               | Description                                                |
| :----------------------------------------------------- | :--------------------------------------------------------- |
| `reipresoplot.use_line_graph_style_as_global_settings` | Use `matplotlibrc` file for line graphs as global settings |
| `reipresoplot.use_bar_graph_style_as_global_settings`  | Use `matplotlibrc` file for bar graphs as global settings  |
| `reipresoplot.get_line_graph_mpl_style_path`           | Get the path to the `matplotlibrc` file for line graphs    |
| `reipresoplot.get_bar_graph_mpl_style_path`            | Get the path to the `matplotlibrc` file for bar graphs     |

If you want to apply the style globally to the entire graph plot, use `reipresoplot.use_XXX_graph_style_as_global_settings`.

```python
from matplotlib import pyplot as plt
from reipresoplot import use_line_graph_style_as_global_settings

use_line_graph_style_as_global_settings()

plt.plot(x, y)
plt.show()
```

If you want to use it temporarily, use a context manager.

```python
from reipresoplot import get_line_graph_mpl_style_path

mpl_style_path: str = get_line_graph_mpl_style_path()
with plt.style.context(mpl_style_path):
    plt.plot(x, y)
    plt.show()
```

#### Line graph changes

Please refer to the code at [examples/using_matplotlibrc_files/for_line_graph.py](https://github.com/NakuRei/rei-preso-plot/blob/main/examples/using_matplotlibrc_files/for_line_graph.py) for line graph changes.

|           Before            |           After           |
| :-------------------------: | :-----------------------: |
| ![Before][before_line_link] | ![After][after_line_link] |

[before_line_link]: https://raw.githubusercontent.com/NakuRei/rei-preso-plot/main/examples/using_matplotlibrc_files/result/line_graph_before.png
[after_line_link]: https://raw.githubusercontent.com/NakuRei/rei-preso-plot/main/examples/using_matplotlibrc_files/result/line_graph_after.png

#### Bar graph changes

Please refer to the code at [examples/using_matplotlibrc_files/for_bar_graph.py](https://github.com/NakuRei/rei-preso-plot/blob/main/examples/using_matplotlibrc_files/for_bar_graph.py) for bar graph changes.

|           Before           |          After           |
| :------------------------: | :----------------------: |
| ![Before][before_bar_link] | ![After][after_bar_link] |

[before_bar_link]: https://raw.githubusercontent.com/NakuRei/rei-preso-plot/main/examples/using_matplotlibrc_files/result/bar_graph_before.png
[after_bar_link]: https://raw.githubusercontent.com/NakuRei/rei-preso-plot/main/examples/using_matplotlibrc_files/result/bar_graph_after.png

## Test

You can test graph drawing with Pytest.

```shell
pytest
```

## Author

[NakuRei](https://notes.nakurei.com/about/)

## License

© 2023 NakuRei

This software is released under the MIT License, see LICENSE.
