Changelog
=========


1.3 (2015-06-12)
----------------

- Don't crash if we get a CookieError.
  [vincentfretin]

- Properly deal with doubly quoted __ac cookies (e.g. from PAS.CookieAuthHelper).
  [lgraf]

- skip binascii.Error
  [kroman0]

- Added getting real client ip
  [kroman0]


1.2 (2011-08-16)
----------------

- Added support for Plone 4.x session cookies.
  [buchi]

- Handle auth cookies that aren't hex encoded (used in PluggableAuthService
  < 1.5).
  [buchi]

- Add `z3c.autoinclude` entry point for automatic ZCML loading in Plone 3.3+.
  [witsch]


1.1 (2010-01-07)
----------------

- Unquote the cookie value before attempting to decode it.
  [vincentfretin]


1.0 (2009-08-08)
----------------

- Re-release unchanged 1.0a2 as final.
  [witsch]


1.0a2 (2009-07-24)
------------------

- Split session cookie from the right as the token can also contain spaces.
  [witsch]

- Handle session cookies first as they can contain a colon, thereby breaking
  the hexadecimal decode.
  [witsch]


1.0a1 (2009-07-23)
------------------

- Initial release
  [witsch]
