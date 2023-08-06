import warnings

# from munch import munchify

import http.client
import socket

import xmltodict
import urllib3

import requests

from ka_utg.com import Com
from ka_utg.log import Log
from ka_utg.utg import d_Uri

from ka_uts.uts import Json

warnings.filterwarnings("ignore")


class Http:

    class Client:

        @staticmethod
        def get(**kwargs):
            m_data = None
            d_uri = kwargs.get('d_uri')
            params = kwargs.get('params')
            data = kwargs.get('data')
            headers = kwargs.get('headers')

            uri_path = d_Uri.sh_path(d_uri, params)

            # parms_urlencode = urllib.parse.urlencode(parms)
            # uri_path_query = f"{uri_path}?{query}&{parms_urlencode}"

            try:
                connection = http.client.HTTPSConnection(
                               d_uri.authority, timeout=10)

                Log.Eq.debug("data", data)
                Log.Eq.debug("headers", headers)
                Log.Eq.debug("connection", d_uri.authority)
                Log.Eq.debug("uri_path", uri_path)

                connection.request("GET", uri_path, data, headers)
                response = connection.getresponse()
                data_ = response.read()
                d_data = Json.loads(data_)
                m_data = d_data

                connection.close()

                Log.Eq.debug("d_data", d_data)

            except socket.timeout:
                Log.error("connection's timeout: 10 expired")
                raise
            except Exception:
                raise

            # if isinstance(m_data, (dict, tuple, list)):
            #     return munchify(m_data)
            # else:
            #     return m_data
            return m_data


class Urllib3:

    class Content:

        @staticmethod
        def sh(resp):

            data_decoded = resp.data.decode('utf-8')
            Log.Eq.debug("data_decoded", data_decoded)
            if data_decoded.startswith("<"):
                data = xmltodict.parse(data_decoded)
            elif data_decoded.startswith(("{", "[")):
                data = Json.loads(data_decoded)
            else:
                data = data_decoded
            Log.Eq.debug("data", data)
            # if isinstance(data, (dict, tuple, list)):
            #     return munchify(data)
            # else:
            #     return data
            return data

    class Request:

        @staticmethod
        def get(**kwargs):
            data = None
            uri = kwargs.get('uri')
            try:
                data = None
                http = urllib3.PoolManager()
                resp = http.request('GET', uri)

                Log.Eq.debug("resp", resp)

                data = Urllib3.Content.sh(resp)

                Log.Eq.debug("data", data)
            except Exception:
                # Log.error(e, exc_info=True)
                raise

            return data


class Request:

    class Content:

        class D_Content:

            @staticmethod
            def sh(resp):
                ct = resp.headers['Content-Type']
                a_ct = ct.split(';')
                # d_ct = munchify({})
                d_ct = {}
                d_ct['content_type'] = a_ct[0].strip()
                if len(a_ct) > 1:
                    d_ct['charset'] = a_ct[1].strip()

                Log.Eq.debug("resp.headers", resp.headers)
                Log.Eq.debug("d_ct", d_ct)

                return d_ct

        @classmethod
        def sh(cls, resp):
            d_ct = cls.D_Content.sh(resp)

            Log.Eq.debug("d_ct", d_ct)

            if d_ct['content_type'] == 'application/json':
                content = resp.json()
            elif d_ct['content_type'] == 'text/plain':
                content = resp.text
            elif d_ct['content_type'] == 'text/xml':
                content = xmltodict.parse(resp.text)
            elif d_ct['content_type'] == 'text/html':
                content = resp.text
            else:
                content = None
            # if isinstance(content, (dict, tuple, list)):
            #     return munchify(content)
            # return content
            return content

    class Uri:

        @staticmethod
        def sh(uri, **kwargs):
            if uri is None:
                d_uri = kwargs.get('d_uri')
                Log.Eq.debug("d_uri", d_uri)
                uri = d_Uri.sh(d_uri)
                Log.Eq.debug("uri", uri)
            return uri

    class Kw:

        @staticmethod
        def sh(**kwargs):
            params = kwargs.get('params')
            data = kwargs.get('data')
            headers = kwargs.get('headers')
            auth = kwargs.get('auth')

            Log.Eq.debug("auth", auth)
            Log.Eq.debug("params", params)
            Log.Eq.debug("data", data)
            Log.Eq.debug("headers", headers)

            kw = {}
            if data is not None:
                kw['data'] = data
            if params is not None:
                kw['params'] = params
            if headers is not None:
                kw['headers'] = headers
            if auth is not None:
                kw['auth'] = auth

            Log.Eq.debug("kw", kw)

            return kw

    class Session:

        @classmethod
        def get(cls, uri=None, **kwargs):
            uri = Request.Uri.sh(uri, **kwargs)
            content = None
            kw = Request.Kw.sh(**kwargs)
            try:
                if 'session' not in Com.App.reqs:
                    Com.App.reqs.session = requests.Session()
                resp = Com.App['reqs']['session'].get(uri, **kw)
                resp.raise_for_status()

                Log.Eq.debug("resp", resp)
                Log.Eq.debug("resp.headers", resp.headers)

                content = Request.Content.sh(resp)
            except requests.exceptions.HTTPError as e:
                # Need to check its an 404, 503, 500, 403 etc.
                # status_code = e.response.status_code
                Log.warning(e, exc_info=True)
            except Exception:
                # Log.error(e, exc_info=True)
                raise

            Log.Eq.debug("content", content)
            return content

    class Request:

        @classmethod
        def get(cls, uri=None, **kwargs):
            uri = Request.Uri.sh(uri, **kwargs)
            content = None
            kw = Request.Kw.sh(**kwargs)
            try:
                resp = requests.get(uri, **kw)
                Log.Eq.debug(">>> kw", kw)
                Log.Eq.debug(">>> resp", resp)
                Log.Eq.debug(">>> resp.headers", resp.headers)

                resp.raise_for_status()

                content = Request.Content.sh(resp)
            except requests.exceptions.HTTPError as e:
                # Need to check its an 404, 503, 500, 403 etc.
                status_code = e.response.status_code
                Log.Eq.debug("e.response.status_code", status_code)
                Log.warning(e, exc_info=True)
            except Exception:
                # Log.error(e, exc_info=True)
                raise

            return content
            Log.Eq.debug("EEE content", content)


class Uri:
    """ Manage uri's
    """
    @staticmethod
    def dispatch_get(httpmod):
        if Com.App.httpmod == "H_C":
            return Http.Client.get
        elif Com.App.httpmod == "U3_R":
            return Urllib3.Request.get
        elif Com.App.httpmod == "R_R":
            return Request.Request.get
        elif Com.App.httpmod == "R_S":
            return Request.Session.get
        return Request.Session.get

    @classmethod
    def get(cls, **kwargs):
        get_ = cls.dispatch_get(Com.App.httpmod)
        content = get_(**kwargs)
        Log.Eq.debug('content', content)
        # if isinstance(content, (dict, tuple, list)):
        #     return munchify(content)
        # else:
        #     return content
        return content
