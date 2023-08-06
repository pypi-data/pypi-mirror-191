from typing import Union


def generate_items_for_focus(
    data_num: int,
    default_colors: list[str],
    focus_indexes: Union[int, list[int], None],
    focus_color: Union[str, None],
    not_focus_color: str,
) -> tuple[list[str], list[int], list[str]]:
    # initialization
    colors: list[str] = [not_focus_color] * data_num
    z_orders: list[int] = [1] * data_num
    font_weights: list[str] = ["normal"] * data_num
    # when no focus index
    if focus_indexes is None or len(focus_indexes) < 1:
        return default_colors, z_orders, font_weights
    # int to list
    if type(focus_indexes) == int:
        focus_indexes: list[int] = [focus_indexes]
    # generation
    for index, focus_index in enumerate(focus_indexes):
        if data_num <= focus_index:
            raise ValueError(f'"focus_index" {focus_index} is out of range.')
        if focus_color is None:
            colors[focus_index] = default_colors[index]
        else:
            colors[focus_index] = focus_color
        z_orders[focus_index] = 2
        font_weights[focus_index] = "bold"

    return colors, z_orders, font_weights
