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
"""Provides the result of an execution run."""
from typing import Dict


class ExecutionResult:
    """Result of an execution."""

    def __init__(self) -> None:
        self._exceptions: Dict[int, Exception] = {}

    @property
    def exceptions(self) -> Dict[int, Exception]:
        """Provide a map of statements indices that threw an exception. """
        return self._exceptions

    def has_test_exceptions(self) -> bool:
        """
        Returns true if any exceptions were thrown during the execution.
        """
        return bool(self._exceptions)

    def report_new_thrown_exception(self, stmt_idx: int, ex: Exception) -> None:
        """
        Report an exception that was thrown during execution
        :param stmt_idx: the index of the statement, that caused the exception
        :param ex: the exception
        """
        self._exceptions[stmt_idx] = ex

    # TODO(fk) traces.