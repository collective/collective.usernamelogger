from base64 import decodestring, binascii
from time import time
from urllib import unquote
from Cookie import CookieError, SimpleCookie
from ZPublisher import HTTPRequest

import os

cookie_name = os.environ.get('USERNAMELOGGER_AC_COOKIE_NAME', '__ac')


def repeatedly_unquote(cookie):
    """Keep unquoting the cookie value until it doesn't change any more.
    We do this to deal with doubly-quoted base64 strings that otherwise would
    have incorrect padding.
    """
    done = False
    unquoted_cookie = cookie
    while not done:
        if unquote(unquoted_cookie) == unquoted_cookie:
            done = True
        unquoted_cookie = unquote(unquoted_cookie)
    return unquoted_cookie


def username(cookie, name=None):
    """ try to extract username from PAS cookie """
    if cookie is not None:
        cookies = SimpleCookie()
        try:
            cookies.load(cookie)
        except CookieError:
            return name

        if cookie_name in cookies:
            # Deal with doubly quoted cookies
            ac_cookie = repeatedly_unquote(cookies[cookie_name].value)

            try:
                ac = decodestring(ac_cookie + '=====')
            except (TypeError, binascii.Error):
                return name

            # plone.session 3.x (Plone 4.x)
            if '!' in ac[40:]:
                name, user_data = ac[40:].split('!', 1)
            # plone.session 2.x (Plone 3.x)
            elif ' ' in ac[20:21]:
                name = ac[21:]
            # PluggableAuthService.CookieAuthHelper
            elif ':' in ac:
                user, pwd = ac.split(':', 1)
                # PluggableAuthService >= 1.5
                try:
                    name = user.decode('hex')
                # PluggableAuthService < 1.5
                except TypeError:
                    name = user
    return name


def prepare_log_entry(self, bytes):
    user_agent=self.get_header('user-agent')
    if not user_agent: user_agent=''
    referer=self.get_header('referer')
    if not referer: referer=''

    ip_addr = self.channel.addr[0]
    forwarded_for = self.get_header('X-Forwarded-For')
    if forwarded_for and ip_addr in HTTPRequest.trusted_proxies:
        forwarded_for = [e.strip() for e in forwarded_for.split(',')]
        forwarded_for.reverse()
        for entry in forwarded_for:
            if entry not in HTTPRequest.trusted_proxies:
                ip_addr = entry
                break

    auth=self.get_header('Authorization')
    name='Anonymous'
    if auth is not None:
        if auth[:6].lower() == 'basic ':
            try: decoded = decodestring(auth[6:])
            except binascii.Error: decoded=''
            t = decoded.split(':', 1)
            if len(t) < 2:
                name = 'Unknown (bad auth string)'
            else:
                name = t[0]

    # support for cookies and cookie authentication
    name = username(self.get_header('Cookie'), name)

    return {'ip_addr': ip_addr,
            'user': name,
            'date': self.log_date_string (time()),
            'request_line': self.request,
            'response_code': self.reply_code,
            'bytes': bytes,
            'referer': referer,
            'user_agent': user_agent}


def format_log_entry(self, data):
    return '- %(user)s [%(date)s] "%(request_line)s" %(response_code)d' \
        ' %(bytes)d "%(referer)s" "%(user_agent)s"\n' % data


# the following is a copy of the `log` method from
# `ZServer.medusa.http_server.http_request.py` (around line 272)
# plus the extra call to the above function to extract the username
def log (self, bytes):
    data = self.prepare_log_entry(bytes)
    message = self.format_log_entry(data)
    self.channel.server.logger.log(data['ip_addr'], message)


def apply_patches(scope, original, replacement):
    # This patches ".log":
    setattr(scope, original, replacement)
    # we also need our helper methods:
    setattr(scope, 'prepare_log_entry', prepare_log_entry)
    setattr(scope, 'format_log_entry', format_log_entry)
