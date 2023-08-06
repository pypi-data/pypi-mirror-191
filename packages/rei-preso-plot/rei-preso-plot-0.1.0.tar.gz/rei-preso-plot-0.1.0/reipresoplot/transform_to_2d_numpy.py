import numpy as np

from numpy.typing import ArrayLike, DTypeLike, NDArray
from typing import Union


def transform_to_2d_numpy(
    data: ArrayLike,
    dtype: Union[DTypeLike, None] = None,
) -> NDArray:
    if dtype is None:
        data = np.array(data)
    else:
        data = np.array(data, dtype=dtype)
    if len(data.shape) == 1:
        data = data.reshape(1, -1)
    assert len(data.shape) == 2
    return data
