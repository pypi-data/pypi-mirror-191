"""
The version of the package can be returned as a single string or a dict.

When a string, it comes from the package __version__.
When a dict, it also has __version__,
as well as versions of other depdency packages.
"""

from typing import Optional

import dls_logformatter.version
import psutil

from dls_mainiac_lib import __version__

psutil_version = psutil.__version__


# ----------------------------------------------------------
def version() -> str:
    """
    Version of the dls_mainiac_lib package as a string.
    """

    return __version__


# ----------------------------------------------------------
def meta(given_meta: Optional[dict] = None) -> dict:
    """
    Returns version information from the dls_mainiac_lib package
    and its dependencies as a dict.
    Adds version information to a given meta dict if it was provided.
    """

    meta = {}
    meta["dls_mainiac_lib"] = version()
    meta.update(dls_logformatter.version.meta())
    meta["psutil"] = psutil_version

    try:
        import graypy

        meta["graypy"] = graypy.__version__
        meta["graypy"] = ".".join([str(s) for s in meta["graypy"]])
    except Exception:
        meta["graypy"] = "unavailable"

    if given_meta is not None:
        given_meta.update(meta)
    else:
        given_meta = meta

    return given_meta
