# SPDX-License-Identifier: MIT

from pathlib import Path
from tempfile import TemporaryDirectory
from typing import Iterator

import pytest
from sh.contrib import git


@pytest.fixture
def tmpdir() -> Iterator[Path]:
    with TemporaryDirectory() as directory:
        yield Path(directory)


@pytest.fixture
def gitdir(tmpdir: Path) -> Iterator[Path]:
    git.init(tmpdir)
    git.bake("-C", tmpdir).config("user.name", "Jane Doe")
    git.bake("-C", tmpdir).config("user.email", "jane.doe@example.com")
    yield tmpdir
