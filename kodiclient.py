from typing import Mapping

import requests
from jsonrpcclient import Error, Ok, parse, request

KODI_JSON_NAMESPACES = [
    "VideoLibrary", "Settings", "Favourites", "AudioLibrary", "Application",
    "Player", "Input", "System", "Playlist", "Addons", "AudioLibrary", "Files",
    "GUI", "JSONRPC", "PVR", "xbmc"
]


class KodiNamespaceMethodCatcher(object):
    """
    provides a __getattr__ method which
    catches all method calls and makes the
    corresponding server requests
    """

    def __init__(self, url: str, headers: Mapping[str, str], auth: tuple[str, str], namespace: str):
        self.url = url
        self.headers = headers
        self.auth = auth
        self.namespace = namespace

    def __getattr__(self, function):
        """
        answer the function calls in a generic way
        """

        def func(*args):
            if args:
                data = args[0]
            else:
                data = None
            response = requests.post(self.url, headers=self.headers, auth=self.auth, timeout=10,
                                     json=request("{0}.{1}".format(self.namespace, function), data))
            match parse(response.json()):
                case Ok(result, id_):
                    return result
                case Error(code, message, data, id_):
                    raise ConnectionError(f"connection to {self.url} not possible: {code} {message} / data: {data}")
            return None

        return func


class KodiJSONClient(object):
    """
    instantiate KodiNamespaceMethodCatcher classes
    for all Kodi JSON namespaces which allows any
    of the Kodi JSON methods to be called as methods
    of the KodiJSONClient, e.g
    <KodiJSONClient object>.JSONRPC.Ping() or
    <KodiJSONClient object>.Player.GetActivePlayers()
    """

    def __init__(self, host, port, user, pwd):
        self.url = 'http://{0}:{1}/jsonrpc'.format(host, port)
        self.headers = {'content-type': 'application/json'}
        self.auth = (user, pwd)
        for namespace in KODI_JSON_NAMESPACES:
            self.__dict__[namespace] = KodiNamespaceMethodCatcher(
                self.url, self.headers, self.auth, namespace)
