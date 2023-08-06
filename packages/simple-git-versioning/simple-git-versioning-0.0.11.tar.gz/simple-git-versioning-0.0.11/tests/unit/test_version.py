# SPDX-License-Identifier: MIT

import os

import pytest
from packaging.version import Version
from sh.contrib import git
from versioning import version

from . import gitdir, tmpdir


def _format_commit_message(message: str) -> str:
    return "\n".join(map(str.strip, message.strip().split("\n")))


def test_project_s_version_is_set():
    from versioning import __version__

    Version(__version__)


def test_version_not_in_git_repository(tmpdir):
    os.chdir(tmpdir)
    with pytest.raises(RuntimeError, match="not a git work tree"):
        version()


def test_version_default(gitdir):
    os.chdir(gitdir)
    assert version() == Version("0.0.0")


def test_version_at_tag(gitdir):
    os.chdir(gitdir)
    git.commit("--allow-empty", "--message", "initial empty commit")
    git.tag("--annotate", "--message", "version 1.0.0", "1.0.0")
    assert version() == Version("1.0.0")


def test_version_patch(gitdir):
    os.chdir(gitdir)
    git.commit("--allow-empty", "--message", "initial empty commit")
    git.tag("--annotate", "--message", "version 1.0.0", "1.0.0")
    git.commit(
        "--allow-empty",
        "--message",
        _format_commit_message(
            """
            lorem ipsum dolor sit amet

            ci-version-bump: patch
            """
        ),
    )
    assert version() == Version("1.0.1")


def test_version_minor(gitdir):
    os.chdir(gitdir)
    git.commit("--allow-empty", "--message", "initial empty commit")
    git.tag("--annotate", "--message", "version 1.0.0", "1.0.0")
    git.commit(
        "--allow-empty",
        "--message",
        _format_commit_message(
            """
            lorem ipsum dolor sit amet

            ci-version-bump: minor
            """
        ),
    )
    assert version() == Version("1.1.0")


def test_version_major(gitdir):
    os.chdir(gitdir)
    git.commit("--allow-empty", "--message", "initial empty commit")
    git.tag("--annotate", "--message", "version 1.0.0", "1.0.0")
    git.commit(
        "--allow-empty",
        "--message",
        _format_commit_message(
            """
            lorem ipsum dolor sit amet

            ci-version-bump: major
            """
        ),
    )
    assert version() == Version("2.0.0")


def test_version_major_minor_patch(gitdir):
    os.chdir(gitdir)
    git.commit("--allow-empty", "--message", "initial empty commit")
    git.tag("--annotate", "--message", "version 1.0.0", "1.0.0")
    git.commit(
        "--allow-empty",
        "--message",
        _format_commit_message(
            """
            lorem ipsum dolor sit amet

            ci-version-bump: major
            """
        ),
    )
    git.commit(
        "--allow-empty",
        "--message",
        _format_commit_message(
            """
            lorem ipsum dolor sit amet

            ci-version-bump: minor
            """
        ),
    )
    git.commit(
        "--allow-empty",
        "--message",
        _format_commit_message(
            """
            lorem ipsum dolor sit amet

            ci-version-bump: patch
            """
        ),
    )
    assert version() == Version("2.1.1")


def test_version_patch_minor_major(gitdir):
    os.chdir(gitdir)
    git.commit("--allow-empty", "--message", "initial empty commit")
    git.tag("--annotate", "--message", "version 1.0.0", "1.0.0")
    git.commit(
        "--allow-empty",
        "--message",
        _format_commit_message(
            """
            lorem ipsum dolor sit amet

            ci-version-bump: patch
            """
        ),
    )
    git.commit(
        "--allow-empty",
        "--message",
        _format_commit_message(
            """
            lorem ipsum dolor sit amet

            ci-version-bump: minor
            """
        ),
    )
    git.commit(
        "--allow-empty",
        "--message",
        _format_commit_message(
            """
            lorem ipsum dolor sit amet

            ci-version-bump: major
            """
        ),
    )
    assert version() == Version("2.0.0")


def test_version_patch_minor(gitdir):
    os.chdir(gitdir)
    git.commit("--allow-empty", "--message", "initial empty commit")
    git.tag("--annotate", "--message", "version 1.0.0", "1.0.0")
    git.commit(
        "--allow-empty",
        "--message",
        _format_commit_message(
            """
            lorem ipsum dolor sit amet

            ci-version-bump: patch
            """
        ),
    )
    git.commit(
        "--allow-empty",
        "--message",
        _format_commit_message(
            """
            lorem ipsum dolor sit amet

            ci-version-bump: minor
            """
        ),
    )
    assert version() == Version("1.1.0")


def test_version_default_bump_is_patch(gitdir):
    os.chdir(gitdir)
    git.commit("--allow-empty", "--message", "initial empty commit")
    git.tag("--annotate", "--message", "version 1.0.0", "1.0.0")
    git.commit("--allow-empty", "--message", "lorem ipsum dolor sit amet")
    git.commit("--allow-empty", "--message", "lorem ipsum dolor sit amet")
    git.commit("--allow-empty", "--message", "lorem ipsum dolor sit amet")
    assert version() == Version("1.0.3")


def test_version_ignores_unrelated_trailers(gitdir):
    os.chdir(gitdir)
    git.commit("--allow-empty", "--message", "initial empty commit")
    git.tag("--annotate", "--message", "version 1.0.0", "1.0.0")
    git.commit(
        "--allow-empty",
        "--message",
        _format_commit_message(
            """
            lorem ipsum dolor sit amet

            Acked-by: John Smith <john.smith@example.com>
            Signoed-off-by: Jane Doe <jane.doe@example.com>
            Change-type: major
            """
        ),
    )
    assert version() == Version("1.0.1")


def test_version_typos_in_trailer_values_get_caught(gitdir):
    os.chdir(gitdir)
    git.commit("--allow-empty", "--message", "initial empty commit")
    git.tag("--annotate", "--message", "version 1.0.0", "1.0.0")
    git.commit(
        "--allow-empty",
        "--message",
        _format_commit_message(
            """
            lorem ipsum dolor sit amet

            ci-version-bump: path
            """
        ),
    )
    with pytest.raises(RuntimeError, match="patch, minor, or major"):
        version()
