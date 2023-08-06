# Copyright 2020 Georges Racinet <georges.racinet@octobus.net>
#
# This software may be used and distributed according to the terms of the
# GNU General Public License version 2 or any later version.
#
# SPDX-License-Identifier: GPL-2.0-or-later
from grpc import StatusCode
import logging

logger = logging.getLogger(__name__)

HGITALY_ISSUES_URL = "https://foss.heptapod.net/heptapod/hgitaly/-/issues"


class ServiceError(RuntimeError):
    """An exception class to complement setting of context.

    In cases where a more precise exception than the bare `Exception()` raised
    by `ServicerContext.abort()` is useful.

    Caller is expected to set code and optionally details.
    """


def not_implemented(context, issue: int):
    """Raise with NOT_IMPLEMENTED status code and link to issue.
    """
    msg = "Not implemented. Tracking issue: %s/%d" % (HGITALY_ISSUES_URL,
                                                      issue)
    logger.error(msg)
    context.abort(StatusCode.UNIMPLEMENTED, msg)
