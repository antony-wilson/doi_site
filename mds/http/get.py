'''
This module is used to make HTTP HEAD and GET calls.
'''

import base64
import logging
import socket
import urllib.error
import urllib.parse
import urllib.request
from ssl import SSLError

from django.http import HttpResponse

from doi_site.settings import DATACITE_USER_NAME, DATACITE_PASSWORD, TIME_OUT
from mds.http.helper import get_response, get_opener

LOGGING = logging.getLogger(__name__)


def get(request_method, url, headers):
    """
    Send a get or head request to DataCite.

    Args:
        request_method (str): This should be 'GET' or 'HEAD'
        url (str): The URL to call
        headers (dict): A dictionary of headers to use

    Return:
        a HTTPResponse

    """
    LOGGING.info('get(%s,%s,%s)', request_method, url, headers)
    _set_timeout()
    opener = get_opener()
    auth_string = (base64.encodebytes((DATACITE_USER_NAME + ':' + DATACITE_PASSWORD).encode())).rstrip()
    headers.update({'Authorization': 'Basic ' + str(auth_string)})
    req = urllib.request.Request(url, data=None, headers=headers)
    if request_method == "HEAD":
        req.get_method = lambda: 'HEAD'
    try:
        response = opener.open(req)
    except (urllib.error.HTTPError) as ex:
        msg = ex.readlines()
        if ex.code in [404, 410]:
            LOGGING.info('HTTPError error getting %s. %s', url, msg)
        else:
            LOGGING.warn('HTTPError error getting %s. %s', url, msg)
        return get_response(msg, ex.code)
    except (socket.timeout, urllib.error.URLError) as ex:
        LOGGING.warn('Timeout or URLError error getting %s. %s', url, ex.reason)
        return get_response(ex.reason, 500)
    except (SSLError) as ex:
        LOGGING.warn('SSLError error getting %s. %s', url, ex)
        return get_response(ex, 500)
    finally:
        _close(opener)
    if 'Content-Type' in response.headers:
        ret_response = HttpResponse(content_type=
                                    response.headers.get('Content-Type'))
    else:
        ret_response = HttpResponse()
    ret_response.status_code = response.code
    ret_response.reason_phrase = response.msg
    # pylint: disable=maybe-no-member
    ret_response.writelines(response.readlines())
    return ret_response


def _set_timeout():
    """
    Set the time out used by urllib.

    """
    socket.setdefaulttimeout(TIME_OUT)


def _close(opener):
    """
    Close the URL opener.

    """
    try:
        opener.close()
    # pylint: disable=bare-except
    except:
        pass
