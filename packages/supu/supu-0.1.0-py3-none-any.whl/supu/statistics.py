from typing import Any, NamedTuple, Union

import numpy as np
from scipy.stats import bootstrap

try:
    from collections.abc import Sequence
except ImportError:
    from typing import Sequence


def confidence_interval(data: Union[Sequence, Any], **kwargs) -> NamedTuple:
    """Return the confidence interval for the mean of the data."""
    if not isinstance(data[0], Sequence):
        data = [data]
    return bootstrap(
        data, np.mean, vectorized=True, axis=-1, **kwargs
    ).confidence_interval
