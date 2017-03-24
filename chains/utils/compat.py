from __future__ import absolute_import

import sys

if sys.version_info < (3,):
    ord = ord
else:
    def ord(char):
        return char

try:
    from itertools import izip
    izip = izip
except ImportError:
    izip = zip

try:
    from cStringIO import StringIO
except ImportError:
    from io import StringIO

try:
    from BytesIO import BytesIO
except ImportError:
    from io import BytesIO

if sys.version_info < (3,):
    def iteritems(d, **kw):
        return d.iteritems(**kw)
else:
    def iteritems(d, **kw):
        return iter(d.items(**kw))

try:
    from urllib.request import unquote
except ImportError:
    from urllib2 import unquote

