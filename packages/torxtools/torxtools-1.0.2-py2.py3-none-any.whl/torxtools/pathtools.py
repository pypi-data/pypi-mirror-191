"""
Functions for working with filesystem paths.

The :func:`expandpath` does recursive shell-like expansion of paths from lists.
"""
import os
import typing as t

import boltons.pathutils

__all__ = [
    "expandpath",
]


def expandpath(path: t.Union[str, t.List[str], None]) -> t.Union[str, t.List[str], None]:
    """
    Recursive shell-like expansion of environment variables and tilde home directory.

    Parameters
    ----------
    path: str, [str], None
        a single path, a list of paths, or none.

    Returns
    -------
    str, [str], None:
        a single expanded path, a list of expanded path, or none

    Example
    -------

    .. code-block:: python

        import os
        from torxtools import pathtools

        os.environ["SPAM"] = "eggs"
        assert pathtools.expandpath(["~/$SPAM/one", "~/$SPAM/two"]) == [
            os.path.expanduser("~/eggs/one"),
            os.path.expanduser("~/eggs/two"),
        ]

    See Also
    --------
    :py:func:`boltons:boltons.pathutils.expandpath`
    """

    def _expandpath(path):
        if path is None:
            return None
        if isinstance(path, list):
            return [_expandpath(p) for p in path]
        return boltons.pathutils.expandpath(path)

    return _expandpath(path)


def cachedir(appname: str, path: str) -> str:
    """
    Find a suitable location for cache files.

    Parameters
    ----------
    appname: str
        Name of application. Used as last part of the cachedir path.

    path: str
        a single path, a list of paths, or none.

    Returns
    -------
    str, None:
        a suitable cachedir, created if not existing
    """

    def create_cachedir(path: str) -> str:
        # Check that path exists and is correct type
        if os.path.isdir(path):
            return path
        os.mkdir(path)
        return path

    # Path was passed, create it
    if path:
        return create_cachedir(path)

    if not appname:
        return None

    # Root: use /var/cache
    if os.geteuid() == 0:
        path = expandpath(f"/var/cache/{appname}")
        return create_cachedir(path)

    # Non-Root: use xdg
    path = expandpath(f"$XDG_CACHE_HOME/{appname}")
    return create_cachedir(path)
