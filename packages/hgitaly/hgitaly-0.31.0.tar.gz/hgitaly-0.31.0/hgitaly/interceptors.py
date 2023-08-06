# Copyright 2022 Georges Racinet <georges.racinet@octobus.net>
#
# This software may be used and distributed according to the terms of the
# GNU General Public License version 2 or any later version.
#
# SPDX-License-Identifier: GPL-2.0-or-later
import itertools
import logging
from typing import (
    Any,
    Callable
)

import grpc
from grpc_interceptor import ServerInterceptor

from . import message

logger = logging.getLogger(__name__)


def is_streaming(message) -> bool:
    """Tell whether a gRPC message is streaming (iterable).

    Note that messages aren't plain strings nor Python collections.
    """
    return hasattr(message, '__iter__')


class RequestLoggerInterceptor(ServerInterceptor):
    """Log every request.

    Mostly taken from the example in grpc-interceptor documentation.

    In case of streaming requests, only the first one of the stream gets
    logged. With Gitaly convention, this is usually the only one carrying
    interesting metadata.
    """

    def intercept(
            self,
            method: Callable,
            request: Any,
            context: grpc.ServicerContext,
            method_name: str,
    ) -> Any:
        if is_streaming(request):
            first = next(iter(request))
            request = itertools.chain([first], request)
        else:
            first = request

        # of course it would be great to change the logger depending
        # on the service, but with (H)Gitaly naming conventions, the class
        # name of the request contains all the information.
        logger.debug("Starting to process RPC %r", message.Logging(first))

        response = method(request, context)

        if is_streaming(response):
            return (resp for resp in response)
        else:
            return response
