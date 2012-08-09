from base64 import decodestring, binascii
from time import time
from urllib import unquote
from Cookie import SimpleCookie
from ZPublisher import HTTPRequest


def username(cookie, name=None):
    """ try to extract username from PAS cookie """
    if cookie is not None:
        cookies = SimpleCookie()
        cookies.load(cookie)
        if '__ac' in cookies:
            ac = decodestring(unquote(cookies['__ac'].value) + '=====')
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


# the following is a copy of the `log` method from
# `ZServer.medusa.http_server.http_request.py` (around line 272)
# plus the extra call to the above function to extract the username
def log (self, bytes):
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

    self.channel.server.logger.log (
        ip_addr,
        '- %s [%s] "%s" %d %d "%s" "%s"\n' % (
            name,
            self.log_date_string (time()),
            self.request,
            self.reply_code,
            bytes,
            referer,
            user_agent
            )
        )
