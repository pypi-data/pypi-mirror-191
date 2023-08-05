

from .common import IS_PY3

if IS_PY3:
    import http.client as httplib
else:
    import httplib