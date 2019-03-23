import pytest

from ants_converter import ants2txt

def test_ants_converter():
    ants2txt('test_data/labels.txt', 'test_data/ants/')
