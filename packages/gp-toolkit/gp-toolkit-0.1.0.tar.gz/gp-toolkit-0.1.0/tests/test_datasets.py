#!/usr/bin/env python

from gptk.datasets import load_snelson_1d, load_motorcycle


def test_load_snelson_1d():

    dataset = load_snelson_1d()

    assert dataset.data.shape == (200, 1)
    assert dataset.target.shape == (200, 1)


def test_load_motorcycle():

    dataset = load_motorcycle()

    assert dataset.data.shape == (94, 1)
    assert dataset.target.shape == (94, 1)
