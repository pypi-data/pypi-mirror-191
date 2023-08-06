import warnings
from copy import deepcopy
from typing import Dict, List, Set, Union

import numpy as np



class DuplicatedElementWarning(UserWarning):
    """If contains repeated elements."""

    ...


class InexistentElementWarning(UserWarning):
    """If the element selected does not exist."""

    ...


class OverwritedValueWarning(UserWarning):
    """If a user could accidentally be overwriting a previously stored value."""

    ...



class DataPool:
    """A basic container for unlabeled and labeled data."""

    def __init__(
        self, unlabeled: Union[List[int], np.ndarray, Set[int]], *args, **kwargs
    ) -> None:
        """Create a new instance of DataPool.

        Args:
            unlabeled (Union[List[int], np.ndarray, Set[int]]): List, numpy array, or set of distinct unlabeled indices.
        """  # noqa: E501

        self._labeled = set()
        self._unlabeled = set(unlabeled)
        self.loop_dictionary: Dict[int, Dict[int, set]] = {}

    @property
    def labeled(self) -> List[int]:
        """Getter method for labeled attribute.

        Returns:
            List[int]: Return labeled indices as a/an (unordered) list
        """
        return list(self._labeled)

    @property
    def unlabeled(self) -> List[int]:
        """Getter method for unlabeled attribute.

        Returns:
            List[int]: Return unlabeled indices as a/an (unordered) list
        """
        return list(self._unlabeled)

    def __contains__(self, index: int) -> bool:
        """Check whether an index presents in DataPool or not.

        Args:
            index (int): index to test on

        Returns:
            bool: True if the index presents in labeled or unlabeled pool, False otherwise
        """  # noqa: E501
        return index in self.labeled or index in self.unlabeled

    def _input_sanity_check(
        self, container: str, value: int, labeled: bool = False
    ) -> int:
        """Sanity check for the value to be processed.

        Args:
            container (str): DEPRECATED. Name of the pool to be checked, must be "labeled" or "unlabeled".
            value (int): value that needs to run checks on
            labeled (bool, optional): Whether to check the value on the labeled or unlabeled pool. Defaults to False.
        """  # noqa: E501
        assert container in [
            "labeled",
            "unlabeled",
        ], "Invalid container value, must be 'labeled' or 'unlabeled'"
        warnings.warn(
            "Usage of 'container' will be removed in the future. "
            "Please use 'labeled' argument instead.",
            DeprecationWarning,
            stacklevel=2,
        )

        if not isinstance(value, int):
            warnings.warn(
                "Value data type must be int. Trying to convert it now...",
                RuntimeWarning,
                stacklevel=3,
            )
            return int(value)
        else:
            return value

    def add(self, container: str, value: int, labeled: bool = False) -> None:
        """Add an index to the labeled or unlabeled pool.

        Args:
            container (str): DEPRECATED. Name of the pool to be added, must be "labeled" or "unlabeled".
            value (int): A new index to be added
            labeled (bool, optional): Whether to add a new index to the labeled or unlabeled pool. Defaults to False.
        """  # noqa: E501
        value = self._input_sanity_check(container, value, labeled)
        pool = self._labeled if container == "labeled" or labeled else self._unlabeled
        if value in pool:
            warnings.warn(
                f"Element {value} is already in the pool, skipping...",
                category=DuplicatedElementWarning,
                stacklevel=2,
            )
        else:
            pool.add(value)

    def delete(self, container: str, value: int, labeled: bool = False) -> None:
        """Discard an index in the labeled or unlabeled pool.

        Args:
            container (str): DEPRECATED. Name of the pool to be removed from, must be "labeled" or "unlabeled".
            value (int): A new index to be deleted
            labeled (bool, optional): Whether to remove the index in the labeled or unlabeled pool. Defaults to False.
        """  # noqa: E501
        value = self._input_sanity_check(container, value, labeled)
        pool = self._labeled if container == "labeled" or labeled else self._unlabeled
        if value not in pool:
            warnings.warn(
                f"Element {value} to discard is not in the pool, skipping...",
                category=InexistentElementWarning,
                stacklevel=2,
            )
        else:
            pool.remove(value)

    def update(
        self,
        container: str,
        values: Union[List[int], np.ndarray, Set[int]],
        labeled: bool = False,
    ) -> None:
        """Add multiple indices to the labeled or unlabeled pool.

        Args:
            container (str): DEPRECATED. Name of the pool to be added, must be "labeled" or "unlabeled".
            values (Union[List[int], np.ndarray, Set[int]]): indices to be added. Duplicated indices will be discarded.
            labeled (bool, optional): Whether to add indices to the labeled or unlabeled pool. Defaults to False.
        """  # noqa: E501
        _ = self._input_sanity_check(
            container, -1, labeled
        )  # TODO: properly handle the -1 here
        pool = self._labeled if container == "labeled" or labeled else self._unlabeled
        pool |= set(values)

    def difference_update(
        self,
        container: str,
        values: Union[List[int], np.ndarray, Set[int]],
        labeled: bool = False,
    ) -> None:
        """DEPRECATED. Discard multiple indices in the labeled or unlabeled pool.

        Args:
            container (str): DEPRECATED. Name of the pool to be removed from, must be "labeled" or "unlabeled".
            values ((Union[List[int], np.ndarray, Set[int]])): indices to be removed. Duplicated indices will be discarded.
            labeled (bool, optional): Whether to remove indices in the labeled or unlabeled pool. Defaults to False.
        """  # noqa: E501
        warnings.warn(
            "Usage of 'difference_update' will be remove in the future. "
            "Please use 'difference' method instead.",
            DeprecationWarning,
            stacklevel=2,
        )
        self.difference(container, values, labeled)

    def difference(
        self,
        container: str,
        values: Union[List[int], np.ndarray, Set[int]],
        labeled: bool = False,
    ) -> None:
        """Discard multiple indices in the labeled or unlabeled pool.

        Args:
            container (str): DEPRECATED. Name of the pool to be removed from, must be "labeled" or "unlabeled".
            values ((Union[List[int], np.ndarray, Set[int]])): indices to be removed. Duplicated indices will be discarded.
            labeled (bool, optional): Whether to remove indices in the labeled or unlabeled pool. Defaults to False.
        """  # noqa: E501
        _ = self._input_sanity_check(
            container, -1, labeled
        )  # TODO: properly handle the -1 here
        pool = self._labeled if container == "labeled" or labeled else self._unlabeled
        pool -= set(values)

    def loop_snapshot(self, loop_number: int, verbose=False) -> None:
        """Store the current state of the labeled and unlabeled pool as a dict. It will enable you
        to call on self.loop_dictionary to access the unlabeled or labeled pool at a particular
        step.

        Args:
            loop_number (int): An integer that represents the loop number.
            verbose (bool, optional): Print logging details. Defaults to False.
        """  # noqa: E501
        if not isinstance(loop_number, int):
            warnings.warn(
                "Value data type must be int. Trying to convert it now...",
                RuntimeWarning,
                stacklevel=3,
            )
            loop_number = int(loop_number)

        self.loop_dictionary[loop_number] = {
            "unlabeled": deepcopy(self.unlabeled),
            "labeled": deepcopy(self.labeled),
        }
        if verbose:
            print(f"Loop snapshot at loop {loop_number} successful")

    def random_sample(
        self, container: str, quantity: int, seed: int = None, labeled: bool = False
    ) -> np.ndarray:
        """Randomly sample indices from the labeled or unlabeled pool.

        Args:
            container (str): DEPRECATED. Name of the pool to sample, must be "labeled" or "unlabeled".
            quantity (int): Number of items to sample.
            seed (int, optional): Seed value to be used in the random process. Defaults to None.
            labeled (bool, optional): Whether to sample in the labeled or unlabeled pool. Defaults to False.

        Returns:
            np.ndarray: Selected indices that were randomly sampled.
        """  # noqa: E501
        # TODO: error checking on quantity
        quantity = self._input_sanity_check(container, quantity, labeled)
        pool = self.labeled if container == "labeled" or labeled else self.unlabeled
        selected = np.random.default_rng(seed).choice(pool, quantity, replace=False)
        return selected
