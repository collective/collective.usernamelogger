collective.usernamelogger
=========================

Introduction
------------

This package provides logging of user names in `Zope`_'s access log files
when using cookie-based authentication as provided by PluggableAuthService_
and `plone.session`_.

  .. _`Zope`: http://www.zope.org/
  .. _`PluggableAuthService`: http://pypi.python.org/pypi/Products.PluggableAuthService/
  .. _`plone.session`: http://pypi.python.org/pypi/plone.session/


Installation
------------

The easiest way to use this package is when working with installations
based on `zc.buildout`_.  Here you can simply add the package to your "eggs"
and "zcml" options, run buildout and restart your `Zope`_/`Plone`_ instance.

  .. _`zc.buildout`: http://pypi.python.org/pypi/zc.buildout/
  .. _`Plone`: http://www.plone.org/

Alternatively you can use the following configuration file to extend your
existing buildout::

  [buildout]
  extends = buildout.cfg

  [instance]
  eggs += collective.usernamelogger
  zcml += collective.usernamelogger

After that you should see user names being logged in your access log file,
typically at `<site-root>/var/log/instance-Z2.log`.


Contact
-------

| Andreas Zeidler <az@zitc.de> 
| zitc, http://zitc.de/
