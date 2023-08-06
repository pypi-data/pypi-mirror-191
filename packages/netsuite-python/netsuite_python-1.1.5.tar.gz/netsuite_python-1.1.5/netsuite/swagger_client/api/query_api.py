# coding: utf-8

"""
    NetSuite REST API
"""

from __future__ import absolute_import

import re  # noqa: F401

# python 2 and python 3 compatibility library
import six
import json

from netsuite.swagger_client.api_client import ApiClient


class QueryApi(object):

    def __init__(self, api_client=None):
        if api_client is None:
            api_client = ApiClient()
        self.api_client = api_client

    def execute_query(self, query, **kwargs):
        all_params = ['prefer']  # noqa: E501
        params = locals()
        for key, val in six.iteritems(params['kwargs']):
            if key not in all_params:
                raise TypeError(
                    "Got an unexpected keyword argument '%s'"
                    " to method customer_get" % key
                )
            params[key] = val
        del params['kwargs']

        header_params = {}
        if 'prefer' in params:
            header_params['Prefer'] = params['prefer']  # noqa: E501
        else:
            header_params['Prefer'] = 'transient'

        # Authentication setting
        auth_settings = ['oAuth2ClientCredentials']
        response = json.loads(self.api_client.call_api('',
                                                       'POST',
                                                       header_params=header_params,
                                                       auth_settings=auth_settings,
                                                       body={"q": f"{query}"},
                                                       _return_http_data_only=True,
                                                       _preload_content=False).data.decode('UTF-8'))
        if 'items' in response:
            if type(response.get("items")) is list:
                return response.get("items")
            else:
                items = []
                items.append(response.get("items"))
                return items
        else:
            return None