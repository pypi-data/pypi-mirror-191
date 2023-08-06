"""
This module enables embedding generation for Renumics Audio and Sequence1D
columns based on catch22
"""
from typing import List, Optional, Tuple

import numpy as np
from sktime.transformations.panel.catch22 import Catch22, feature_names

from renumics.spotlight import Audio, Dataset, Sequence1D
from renumics.spotlight.dataset import exceptions
from .utils import align_column_data


def get_feature_names(catch24: bool = False) -> List[str]:
    """
    Get Catch22 feature names in the same order as returned by :func:`catch22`.
    """
    names = list(feature_names)
    if catch24:
        names += ["DN_Mean", "DN_Spread_Std"]
    return names


def catch22(
    dataset: Dataset,
    column: str,
    catch24: bool = False,
    inplace: bool = False,
    suffix: Optional[str] = None,
    overwrite: bool = False,
    as_float_columns: bool = False,
) -> Optional[Tuple[np.ndarray, np.ndarray]]:
    """
    Generate Catch22 embeddings for the given column of a dataset and
    optionally write them back into dataset.
    """
    # pylint: disable=too-many-arguments, too-many-branches
    if suffix is None:
        suffix = "catch24" if catch24 else "catch22"
    column_type = dataset.get_column_type(column)
    if column_type not in (Audio, Sequence1D):
        raise exceptions.InvalidDTypeError(
            f"catch22 is only applicable to columns of type `Audio` and "
            f'`Sequence1D`, but column "{column}" of type {column_type} received.'
        )

    column_names = []
    if as_float_columns:
        for name in get_feature_names(catch24):
            column_names.append("-".join((column, suffix, name)))
    else:
        column_names.append(f"{column}-{suffix}")
    if inplace and not overwrite:
        for name in column_names:
            if name in dataset.keys():
                raise exceptions.ColumnExistsError(
                    f'Column "{name}" already exists. Either set another '
                    f"`suffix` argument or set `overwrite` argument to `True`."
                )
    data, mask = align_column_data(dataset, column, allow_nan=False)

    if inplace:
        if overwrite:
            for name in column_names:
                if name in dataset.keys():
                    del dataset[name]
        for name in column_names:
            if as_float_columns:
                dataset.append_float_column(name, optional=True)
            else:
                dataset.append_embedding_column(name, optional=True)
    if len(data) == 0:
        if inplace:
            return None
        return np.empty((0, 24 if catch24 else 22), dtype=data.dtype), np.full(
            len(dataset), False
        )

    embeddings = Catch22().fit_transform(data.reshape((len(data), 1, -1))).to_numpy()
    if catch24:
        embeddings = np.append(
            embeddings, np.stack([data.mean(axis=1), data.std(axis=1)]).T, axis=1
        )

    if inplace:
        if as_float_columns:
            for name, values in zip(column_names, embeddings.T):
                dataset[name, mask] = values
        else:
            dataset[column_names[0], mask] = embeddings
        return None
    return embeddings, mask
