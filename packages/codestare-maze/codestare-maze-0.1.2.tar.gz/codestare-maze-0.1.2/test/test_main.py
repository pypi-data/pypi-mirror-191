import contextlib
import sys

import pytest

from codestare.mazes.main import main


@pytest.fixture
def args(request, monkeypatch):
    """patch sys args"""
    args = getattr(request, 'param', [])
    monkeypatch.setattr(
        sys,
        'argv',
        [sys.argv[0]] + args
    )
    yield


@pytest.mark.parametrize('args', [
    ['--file', 'labyrinth.txt', 'growing_tree', '60', '30'],
    pytest.param([], marks=pytest.mark.exits),
], indirect=True)
def test_main(request, args):
    ctx = pytest.raises(SystemExit) if request.node.get_closest_marker('exits') else contextlib.nullcontext()
    with ctx:
        main()
