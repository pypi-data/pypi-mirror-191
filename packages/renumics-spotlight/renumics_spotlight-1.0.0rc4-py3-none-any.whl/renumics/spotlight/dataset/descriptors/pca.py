"""
This module provides the capability to generate PCA embeddings for Renumics
data types Embedding, Sequence1D, Audio and Image.
"""

from typing import Optional, Tuple

from sklearn.decomposition import PCA
from sklearn.preprocessing import StandardScaler
import numpy as np

from renumics.spotlight import Dataset
from renumics.spotlight.dataset import exceptions
from .utils import align_column_data


def pca(
    dataset: Dataset,
    column: str,
    n_components: int = 8,
    inplace: bool = False,
    suffix: str = "pca",
    overwrite: bool = False,
) -> Optional[Tuple[np.ndarray, np.ndarray]]:
    """
    Generate PCA embeddings for the given column of a dataset and
    optionally write them back into dataset.
    """
    # pylint: disable=too-many-arguments
    embedding_column_name = f"{column}-{suffix}"
    if inplace and not overwrite and embedding_column_name in dataset.keys():
        raise exceptions.ColumnExistsError(
            f'Column "{embedding_column_name}" already exists. Either set '
            f"another `suffix` argument or set `overwrite` argument to `True`."
        )
    data, mask = align_column_data(dataset, column, allow_nan=False)

    if inplace:
        if overwrite and embedding_column_name in dataset.keys():
            del dataset[embedding_column_name]
        dataset.append_embedding_column(embedding_column_name, optional=True)
    if len(data) == 0:
        if inplace:
            return None
        return np.empty((0, n_components), dtype=data.dtype), np.full(
            len(dataset), False
        )

    data = StandardScaler().fit_transform(data)
    embeddings = PCA(n_components=n_components).fit_transform(data)
    if inplace:
        dataset[embedding_column_name, mask] = embeddings
        return None
    return embeddings, mask
