"""
A collection of functions for integrating with the Archimedes API
"""
import json
from http import HTTPStatus

import requests
from requests.exceptions import (  # pylint:disable=redefined-builtin
    ConnectionError,
    ConnectTimeout,
    HTTPError,
    JSONDecodeError,
    Timeout,
)
from retry.api import retry_call

from archimedes import NoneAuth, get_auth
from archimedes.configuration import get_api_timeout
from archimedes.logger import logger

RETRY_EXCEPTIONS = (ConnectionError, ConnectTimeout, HTTPError, Timeout)


class ArchimedesApi:  # pylint:disable=too-few-public-methods
    """
    Make request to the Archimedes API
    """

    def __init__(self):
        self.session = requests.Session()

    def request(  # pylint:disable=too-many-arguments
        self,
        url,
        method="GET",
        access_token=None,
        retry_count=2,
        retry_delay=2,
        **kwargs,
    ):
        """
        Make request to the Archimedes API. It automatically retries retry_count times
        on failure.

        Args:
            url:
                full URL of the API endpoint.
            method:
                HTTP method to use.
            access_token:
                authorization token; if None, tries to get the token automatically based
                on the authentication configuration.
            retry_count:
                number of times to retry the request. if 0, only one request is made.
            retry_delay:
                delay between retries in seconds.
            **kwargs:
                other kwargs to requests.request.

        Returns:
            Response from the API as a python object.
        """
        logger.debug("Making Archimedes API %s request to %s: %s", method, url, kwargs)
        if access_token is None:
            archimedes_auth = get_auth()
            if archimedes_auth is None:
                raise NoneAuth(
                    "access_token parameter must be passed when using "
                    "USE_WEB_AUTHENTICATION"
                )
            access_token = archimedes_auth.get_access_token_silent()

        timeout = kwargs.pop("timeout", get_api_timeout())

        headers = kwargs.pop("headers", {})
        headers.update({"Authorization": f"Bearer {access_token}"})

        response = retry_call(
            self.session.request,
            fargs=(method, url),
            fkwargs={"headers": headers, "timeout": timeout, **kwargs},
            tries=retry_count + 1,
            delay=retry_delay,
            exceptions=RETRY_EXCEPTIONS,
        )

        if response.status_code not in [HTTPStatus.OK, HTTPStatus.CREATED]:
            try:
                response_json = response.json()
                if "message" in response_json:
                    error_message = response_json.get("message")
                elif "detail" in response_json:
                    error_message = response_json.get("detail")
                else:
                    error_message = json.dumps(response_json)
            except JSONDecodeError:
                error_message = response.content
            params_str = str(kwargs.get("params"))
            data_str = str(kwargs.get("data"))
            raise HTTPError(
                f"API Error while requesting {url} with parameters {params_str} and data {data_str}: "
                f"{error_message}"
            )

        return response.json()


api = ArchimedesApi()
