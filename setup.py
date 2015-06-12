from setuptools import setup, find_packages

version = '1.3'
readme = open('README.rst').read()
history = open('CHANGES.rst').read()

setup(name = 'collective.usernamelogger',
      version = version,
      description = 'Log user names when using cookie authentication in Zope/Plone.',
      long_description = readme[readme.find('\n\n'):readme.find('Contact')] + history,
      classifiers = [
        'Development Status :: 5 - Production/Stable',
        'Environment :: Web Environment',
        'Framework :: Plone',
        'Framework :: Zope2',
        'Intended Audience :: System Administrators',
        'Intended Audience :: Other Audience',
        'License :: OSI Approved :: Zope Public License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Topic :: Software Development :: Libraries :: Python Modules',
      ],
      keywords = 'zope plone logging pas',
      author = 'Andreas Zeidler',
      author_email = 'az@zitc.de',
      url = 'http://pypi.python.org/pypi/collective.usernamelogger',
      license = 'BSD',
      packages = find_packages('src'),
      package_dir = {'': 'src'},
      namespace_packages = ['collective'],
      include_package_data = True,
      platforms = 'Any',
      zip_safe = False,
      install_requires = [
          'setuptools',
          'collective.monkeypatcher',
      ],
      extras_require = { 'test': [
          'collective.testcaselayer',
          'Products.PloneTestCase',
      ]},
      entry_points = '''
        [z3c.autoinclude.plugin]
        target = plone
      ''',
)
