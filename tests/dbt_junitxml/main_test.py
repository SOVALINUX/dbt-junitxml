# -*- coding: utf-8 -*-
from __future__ import annotations

import click.exceptions
import pytest
from dbt_junitxml.main import get_custom_properties
from dbt_junitxml.main import validate_custom_properties


@pytest.mark.parametrize(
    "value, expected",
    [
        ("param1=1,param2=2", {"param1": "1", "param2": "2"}),
        (("param1=1", "param2=2"), {"param1": "1", "param2": "2"}),
    ],
)
def test_validate_custom_properties(value, expected):
    assert validate_custom_properties(None, None, value) == expected


def test_validate_custom_properies_none():
    assert validate_custom_properties(None, None, None) is None


@pytest.mark.parametrize(
    "value",
    [
        "param1=1,param2=2,",
        "param1:1",
    ],
)
def test_validate_custom_properties_error(value):
    with pytest.raises(click.exceptions.BadParameter):
        validate_custom_properties(None, None, "param1=1,param2")


@pytest.mark.parametrize(
    "path, custom_properties, expected",
    [
        (
            "models/source/area/some_model.yml",
            {"Source": "path_levels[1]", "Area": "path_levels[2]"},
            {"attribute": ["Source:source", "Area:area"]},
        ),
        (
            "models/source/area/some_model.yml",
            {"version": "1.2"},
            {"attribute": ["version:1.2"]},
        ),
        (
            "models/source/area/some_model.yml",
            {
                "Source": "path_levels[1]",
                "Area": "path_levels[4]",
                "version": "1.2",
            },
            {"attribute": ["Source:source", "version:1.2"]},
        ),
    ],
)
def test_get_custom_properties(path, custom_properties, expected):
    assert get_custom_properties(path, custom_properties) == expected
