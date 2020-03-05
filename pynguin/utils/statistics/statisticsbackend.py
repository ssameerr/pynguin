# This file is part of Pynguin.
#
# Pynguin is free software: you can redistribute it and/or modify
# it under the terms of the GNU Lesser General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# Pynguin is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Lesser General Public License for more details.
#
# You should have received a copy of the GNU Lesser General Public License
# along with Pynguin.  If not, see <https://www.gnu.org/licenses/>.
"""Provides an interface for a statistics writer."""
import logging
from abc import ABCMeta, abstractmethod
from pathlib import Path
from typing import TypeVar, Dict, Generic

import pynguin.configuration as config

T = TypeVar("T")  # pylint: disable=invalid-name


class OutputVariable(Generic[T]):
    """Encapsulates an output variable of the result statistics."""

    def __init__(self, name: str, value: T) -> None:
        self._name = name
        self._value = value

    @property
    def name(self) -> str:
        """Provides access to the name of the variable"""
        return self._name

    @property
    def value(self) -> T:
        """Provides access to the value of the variable"""
        return self._value

    def __str__(self) -> str:
        return f"{self._name}: {self._value}"

    def __repr__(self) -> str:
        return f"OutputVariable({self._name}, {self._value})"


# pylint: disable=too-few-public-methods
class AbstractStatisticsBackend(metaclass=ABCMeta):
    """An interface for a statistics writer."""

    @abstractmethod
    def write_data(self, data: Dict[str, OutputVariable]) -> None:
        """Write the particular statistics values."""


# pylint: disable=too-few-public-methods
class CSVStatisticsBackend(AbstractStatisticsBackend):
    """A statistics backend writing all (selected) output variables to a CSV file."""

    _logger = logging.getLogger(__name__)

    def write_data(self, data: Dict[str, OutputVariable]) -> None:
        try:
            output_dir = self._get_report_dir()
            output_file = output_dir / "statistics.csv"
            with output_file.open(mode="a") as csv_file:
                if output_file.stat().st_size == 0:  # file is empty, write CSV header
                    csv_file.write(self._get_csv_header(data))
                    csv_file.write("\n")
                csv_file.write(self._get_csv_data(data))
                csv_file.write("\n")
        except IOError as error:
            logging.warning("Error while writing statistics: %s", error)

    def _get_report_dir(self) -> Path:
        report_dir = Path(config.INSTANCE.report_dir)
        if not report_dir.exists():
            try:
                report_dir.mkdir(parents=True, exist_ok=True)
            except OSError:
                msg = "Cannot create report dir %s", config.INSTANCE.report_dir
                self._logger.error(msg)
                raise RuntimeError(msg)
        return report_dir

    @staticmethod
    def _get_csv_header(data: Dict[str, OutputVariable]) -> str:
        return ",".join([k for k, _ in data.items()])

    @staticmethod
    def _get_csv_data(data: Dict[str, OutputVariable]) -> str:
        return ",".join([str(v.value) for _, v in data.items()])


# pylint: disable=too-few-public-methods
class ConsoleStatisticsBackend(AbstractStatisticsBackend):
    """Simple dummy backend that just outputs all output variables to the console"""

    def write_data(self, data: Dict[str, OutputVariable]) -> None:
        for key, value in data.items():
            print(f"{key}: {value}")