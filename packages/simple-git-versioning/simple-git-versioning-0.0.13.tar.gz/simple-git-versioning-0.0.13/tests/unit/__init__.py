# SPDX-License-Identifier: MIT

from pathlib import Path
from tempfile import TemporaryDirectory
from typing import Iterator

import pytest
from sh import pushd
from sh.contrib import git


@pytest.fixture
def tmpdir() -> Iterator[Path]:
    with TemporaryDirectory() as directory:
        yield Path(directory)


@pytest.fixture
def gitdir(tmpdir: Path) -> Iterator[Path]:
    with pushd(tmpdir):
        git.init()
        git.config("user.name", "Jane Doe")
        git.config("user.email", "jane.doe@example.com")
    yield tmpdir
