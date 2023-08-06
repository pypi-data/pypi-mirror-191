#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""Tests for `kiara_plugin.jupyter` package."""

import pytest  # noqa

import kiara_plugin.jupyter


def test_assert():

    assert kiara_plugin.jupyter.get_version() is not None
