#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
ammo.phantom
~~~~~~~~~~~~

Functions to generate raw HTTP request.
"""

import pprint
pp = pprint.PrettyPrinter(indent=4)
import io
import httplib


class HttpCompiler(object):
    version = '3.1'

    def __init__(self, method=None, headers=None):
        self.method = method
        self.headers = headers

    def build_raw(self, url, method=None, body=None, headers=None, tag=None):
        '''
        @see http://docs.python.org/2.7/library/httplib.html#httplib.HTTPConnection.request
        '''
        headers = headers or self.headers
        assert isinstance(headers, dict)
        host = headers.get('Host', None)
        assert host
        method = method or self.method
        assert method

        conn = httplib.HTTPConnection(host)
        bio = io.BytesIO()
        bio.sendall = bio.write
        conn.sock = bio
        conn.request(method, url, body=body, headers=headers)
        return bio.getvalue()

    def build_phantom(self, *args, **kwargs):
        """Compile HTTP request in Yandex-tank(ammo) format.
        For more info about format @see
        http://phantom-doc-ru.readthedocs.org/en/latest/writing-a-phantom-conf.html#ammo-stpd
        All args and kwargs proxied to httplib.HTTPConnection.request method.

        Returns:
            str, ready to use with yandex-tank tool ammo file.
        """
        tag = kwargs.get('tag', None)
        req_ph = self.build_raw(*args, **kwargs)

        if kwargs.get('body'):  # httplib miss this for bodyless requests
            req_ph += '\r\n\r\n'

        if tag:
            req_ph = '{0} {1}\n'.format(len(req_ph), tag) + req_ph
        else:
            req_ph = '{0}\n'.format(len(req_ph)) + req_ph

        req_ph += '\n'
        return req_ph
