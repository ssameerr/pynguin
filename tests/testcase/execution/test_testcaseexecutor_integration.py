#  This file is part of Pynguin.
#
#  SPDX-FileCopyrightText: 2019–2020 Pynguin Contributors
#
#  SPDX-License-Identifier: LGPL-3.0-or-later
#
"""Integration tests for the executor."""
import pynguin.configuration as config
import pynguin.testcase.defaulttestcase as dtc
import pynguin.testcase.statements.parametrizedstatements as param_stmt
import pynguin.testcase.statements.primitivestatements as prim_stmt
from pynguin.instrumentation.machinery import install_import_hook
from pynguin.testcase.execution.executiontracer import ExecutionTracer
from pynguin.testcase.execution.testcaseexecutor import TestCaseExecutor


def test_simple_execution():
    config.INSTANCE.module_name = "tests.fixtures.accessibles.accessible"
    tracer = ExecutionTracer()
    with install_import_hook(config.INSTANCE.module_name, tracer):
        test_case = dtc.DefaultTestCase()
        test_case.add_statement(prim_stmt.IntPrimitiveStatement(test_case, 5))
        executor = TestCaseExecutor(tracer)
        assert not executor.execute([test_case]).has_test_exceptions()


def test_illegal_call(method_mock):
    config.INSTANCE.module_name = "tests.fixtures.accessibles.accessible"
    test_case = dtc.DefaultTestCase()
    int_stmt = prim_stmt.IntPrimitiveStatement(test_case, 5)
    method_stmt = param_stmt.MethodStatement(
        test_case, method_mock, int_stmt.return_value
    )
    test_case.add_statement(int_stmt)
    test_case.add_statement(method_stmt)
    tracer = ExecutionTracer()
    with install_import_hook(config.INSTANCE.module_name, tracer):
        executor = TestCaseExecutor(tracer)
        result = executor.execute([test_case])
        assert result.has_test_exceptions()


def test_no_exceptions(short_test_case):
    config.INSTANCE.module_name = "tests.fixtures.accessibles.accessible"
    tracer = ExecutionTracer()
    with install_import_hook(config.INSTANCE.module_name, tracer):
        executor = TestCaseExecutor(tracer)
        result = executor.execute([short_test_case])
        assert not result.has_test_exceptions()
