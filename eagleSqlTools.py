#!/bin/env python

# Module to access the EAGLE public database
# John Helly 2015 for the Virgo Consortium
# Modified: Kyle Oman 2018 for Python 2 & 3 compatibility

import numpy as np
try:
    # Python 3 compatible imports
    from urllib.parse import urlencode
    from urllib.request import urlopen, HTTPPasswordMgrWithDefaultRealm, \
        OpenerDirector, install_opener, build_opener, HTTPBasicAuthHandler, \
        HTTPCookieProcessor
    from http.cookiejar import LWPCookieJar
except ImportError:
    # Python 2 compatible imports
    from urllib import urlencode
    from urllib2 import HTTPPasswordMgrWithDefaultRealm, OpenerDirector, \
        HTTPBasicAuthHandler, HTTPCookieProcessor, install_opener, \
        build_opener, urlopen
    from cookielib import LWPCookieJar


import re
from getpass import getpass

# Mapping between SQL and numpy types
numpy_dtype = {
    b"real"     : np.float32,
    b"float"    : np.float64,
    b"int"      : np.int32,
    b"bigint"   : np.int64,
    b"char"     : np.dtype("|S256"),
    b"nvarchar" : np.dtype("|S256")
}

# Cookie storage - want to avoid creating a new session for every query
cookie_file = "sql_cookies.txt"
cookie_jar = LWPCookieJar(cookie_file)
try:
    cookie_jar.load(ignore_discard=True)
except IOError:
    pass


class _WebDBConnection:
    def __init__(self, username, password=None):
        """Class to store info required to connect to the web server"""
        # Get password if necessary
        if password is None:
            password = getpass()
        # Get URL for the database
        self.db_url = "http://galaxy-catalogue.dur.ac.uk:8080/Eagle"
        # Set up authentication and cookies
        self.password_mgr = HTTPPasswordMgrWithDefaultRealm()
        self.password_mgr.add_password(None, self.db_url, username, password)
        self.opener = OpenerDirector()
        self.auth_handler   = HTTPBasicAuthHandler(self.password_mgr)
        self.cookie_handler = HTTPCookieProcessor(cookie_jar)

    def _execute_query(self, sql):
        """Run an SQL query and return the result as a record array"""
        url = self.db_url + "?" + urlencode({'action': 'doQuery', 'SQL': sql})
        install_opener(build_opener(self.auth_handler, self.cookie_handler))
        response = urlopen(url)
        cookie_jar.save(ignore_discard=True)

        # Check for OK response
        line = response.readline()
        if bytes(line) != b"#OK\n":
            raise Exception(response.readlines())

        # Skip rows until we reach QUERYTIMEOUT
        while True:
            line = bytes(response.readline())
            if line == b"":
                raise Exception("Unexpected end of file while reading result"
                                "header")
            elif line.startswith(b"#QUERYTIMEOUT"):
                break

        # Skip QUERYTIME
        if not(bytes(response.readline()).startswith(b"#QUERYTIME")):
            raise Exception("Don't understand result header!")

        # Read column info
        # (also discards line with full list of column names)
        columns = []
        while True:
            line = bytes(response.readline())
            if not line.startswith(b"#"):
                break
            else:
                m = re.match(b"^#COLUMN ([0-9]+) name=([\w]+) "
                             b"JDBC_TYPE=(-?[0-9]+) JDBC_TYPENAME=([\w]+)\n$",
                             line)
                if m is not None:
                    columns.append(m.groups())
                else:
                    raise Exception("Don't understand column info: "+line)

        # Construct record type for the output
        types = [numpy_dtype[col[3]] for col in columns]
        try:
            # Python 2 compatible
            names = [col[1] for col in columns]
            dtype = np.dtype([(n, t) for n, t in zip(names, types)])
        except TypeError:
            # Python 3 compatible
            names = [col[1].decode() for col in columns]
            dtype = np.dtype([(n, t) for n, t in zip(names, types)])

        # Return the data as a record array
        return np.genfromtxt(response, dtype=dtype, delimiter=",")

    def fetch_docs(self, table):
        """Return a list of strings containing the documentation page for """
        """the specified table"""
        url = self.db_url + "/Help?" + urlencode(
            {'page': "databases/Eagle/"+table}
        )
        install_opener(build_opener(self.auth_handler, self.cookie_handler))
        response = urlopen(url)
        cookie_jar.save(ignore_discard=True)
        return response.readlines()


def connect(user, password=None):
    """Connect to EAGLE database and return a connection object"""
    return _WebDBConnection(user, password)


def execute_query(con, sql):
    return con._execute_query(sql)
