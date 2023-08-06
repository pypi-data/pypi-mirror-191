import pandas as pd

from supu.statistics import confidence_interval


def describe_with_ci(df: pd.DataFrame, confidence: float = 0.95) -> pd.DataFrame:
    """Add confidence intervals to a DataFrame's describe() output.

    The input dataframe should have a multi-index, with the last level being the
    dependent variable. The output will have the same index, and the same
    columns as the output of df.describe(), with the addition of two columns
    for the lower and upper bounds of the 95% confidence interval.
    """
    d = df.columns[-1]
    levels = tuple(range(df.index.nlevels))
    groupby = df.groupby(level=levels)
    groups = dict(list(groupby))
    cis = pd.DataFrame(
        [
            confidence_interval(g[d], confidence_level=confidence)
            for g in groups.values()
        ],
        index=list(groups.keys()),
        columns=["lower_ci", "upper_ci"],
    )
    desc = groupby.describe()
    desc.columns = desc.columns.droplevel()
    return pd.concat([desc, cis], axis=1)
