"""Import graph library for Python packages."""
from __future__ import annotations

import os


def get_file_dependencies(
    package_path: str,
    file_path: str,
    relative_only: bool = True,
) -> list[str]:
    """
    Given a Python package and a file in that package, returns all the filepaths
    that the path imports.

    If relative_only is True, it filters out builtin and pip installed packages,
    and only returns file paths that are present in the package.
    """
    package_path = os.path.abspath(package_path)
    # TODO: implement logic!
    return []
