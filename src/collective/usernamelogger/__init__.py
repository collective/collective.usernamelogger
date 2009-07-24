import string
import base64
import time
import Cookie


def username(cookie, name=None):
    """ try to extract username from PAS cookie """
    if cookie is not None:
        cookies = Cookie.SimpleCookie()
        cookies.load(cookie)
        if '__ac' in cookies:
            ac = base64.decodestring(cookies['__ac'].value + '=====')
            if ' ' in ac:
                token, name = ac.rsplit(' ', 1)
            elif ':' in ac:
                user, pwd = ac.split(':', 1)
                name = user.decode('hex')
    return name


# the following is a copy of the `log` method from
# `ZServer.medusa.http_server.http_request.py` (around line 272)
# plus the extra call to the above function to extract the username
def log (self, bytes):
    user_agent=self.get_header('user-agent')
    if not user_agent: user_agent=''
    referer=self.get_header('referer')
    if not referer: referer=''

    auth=self.get_header('Authorization')
    name='Anonymous'
    if auth is not None:
        if string.lower(auth[:6]) == 'basic ':
            try: decoded=base64.decodestring(auth[6:])
            except base64.binascii.Error: decoded=''
            t = string.split(decoded, ':', 1)
            if len(t) < 2:
                name = 'Unknown (bad auth string)'
            else:
                name = t[0]

    # support for cookies and cookie authentication
    name = username(self.get_header('Cookie'), name)

    self.channel.server.logger.log (
        self.channel.addr[0],
        '- %s [%s] "%s" %d %d "%s" "%s"\n' % (
            name,
            self.log_date_string (time.time()),
            self.request,
            self.reply_code,
            bytes,
            referer,
            user_agent
            )
        )
