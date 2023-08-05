#!/usr/bin/env python3
# pylint: disable=line-too-long, missing-function-docstring, logging-fstring-interpolation
# pylint: disable=too-many-locals, broad-except, too-many-arguments, raise-missing-from
"""
    pyp8s module
"""

import pytest

from pyp8s import MetricsHandler


def test_inc_simple():
    MetricsHandler.inc("testMetric", 1)


def test_inc_multilabel():
    MetricsHandler.inc("testMetric", 1, more="labels", mooore="mooooore")


def test_inc_and_get_metrics():
    MetricsHandler.inc("testMetric", 1, go="labels", labels="rule")
    excepted_metric_key = "go_labels_kind_testMetric_labels_rule"
    metrics = MetricsHandler.get_metrics()

    print(metrics)

    assert excepted_metric_key in metrics


def test_set_and_get_metrics():
    MetricsHandler.set("biscuitFat", 18, kg="yes", lbs="no")
    excepted_metric_key = "kg_yes_kind_biscuitFat_lbs_no"
    metrics = MetricsHandler.get_metrics()

    print(metrics)

    assert excepted_metric_key in metrics


@pytest.mark.xfail()
def test_double_start():
    MetricsHandler.serve()
    MetricsHandler.serve()
