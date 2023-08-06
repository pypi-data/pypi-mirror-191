import pandas as pd


def mean_encode(df: pd.DataFrame, groupby: str, target: str):
    """
    Groups a Pandas DataFrame via a given column and return
    the mean of the target variable for that grouping.

    Args:
        df (pd.DataFrame): Pandas DataFrame.
        groupby (str): Column to group by.
        target (str): Target variable column.

    Returns:
        pandas.Dataframe: Mean for the target variable across the group.
    """
    mean_encoded = df.groupby(groupby)[target].mean()
    return df[groupby].map(mean_encoded)
