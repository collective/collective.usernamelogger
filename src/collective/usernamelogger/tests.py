from unittest import TestCase, defaultTestLoader
from zope.testing import doctest
from Testing import ZopeTestCase as ztc
from Products.Five import zcml
from Products.Five import fiveconfigure
from Products.PloneTestCase import PloneTestCase as ptc
from collective.testcaselayer.ptc import BasePTCLayer, ptc_layer

optionflags = (doctest.REPORT_ONLY_FIRST_FAILURE |
               doctest.ELLIPSIS | doctest.NORMALIZE_WHITESPACE)

ptc.setupPloneSite()


class Layer(BasePTCLayer):
    """ set up basic testing layer """

    def afterSetUp(self):
        # load zcml for this package and its dependencies
        fiveconfigure.debug_mode = True
        from collective import usernamelogger
        zcml.load_config('configure.zcml', package=usernamelogger)
        fiveconfigure.debug_mode = False
        # after which the required packages can be initialized
        ptc.installPackage('collective.usernamelogger', quiet=True)

layer = Layer(bases=[ptc_layer])


class FunctionalTestCase(ptc.FunctionalTestCase):
    """ base class for functional tests """

    layer = layer


class UsernameTests(TestCase):

    def username(self, value):
        from collective.usernamelogger import username
        from base64 import encodestring
        return username('__ac=%s' % encodestring(value))

    def testSessionCookieWithColon(self):
        self.assertEquals(self.username('john:secret'), 'john')

    def testSessionCookieWithColonInHex(self):
        self.assertEquals(self.username('6a6f686e:736563726574'), 'john')

    def testSessionCookieWithSpaces(self):
        self.assertEquals(self.username('\xd2\xe7\x9bh\x81\xd6=U\xd1\x8f\x07'
            '\xa1\xb2*JdC\x14\x8a\xab john'), 'john')

    def testSessionCookieWithExclamationMark(self):
        self.assertEquals(self.username('\xa35\xeeE\xad\x93\xd1\x0b\xff\x0f'
            '\xf1\x1b\xb1\xb1c7\x85\xf1U\x00\x1f"\'Ci\x16\xd6$nF894e3aa223john'
            '!'), 'john')

    def testDoublyEncodedCookieWithIncorrectPadding(self):
        from urllib import quote
        from base64 import encodestring
        from collective.usernamelogger import username
        TEST_USERNAME = 'admin'
        TEST_PASSWORD = 'admin1'
        hex_credentials = ':'.join([token.encode('hex') for token in \
                                    (TEST_USERNAME, TEST_PASSWORD)])

        # base64 encode credentials - this will add '='s for padding
        b64encoded_credentials = encodestring(hex_credentials).strip()

        # Quote the base64 encoded string *twice*
        # This will mess up the padding unless it's unquoted twice
        broken_cookie = "__ac=%s" % quote(quote(b64encoded_credentials))
        self.assertTrue(username(broken_cookie) == TEST_USERNAME)


def test_suite():
    suite = defaultTestLoader.loadTestsFromName(__name__)
    suite.addTest(
        ztc.FunctionalDocFileSuite(
           'browser.txt', package='collective.usernamelogger',
           test_class=FunctionalTestCase, optionflags=optionflags)
    )
    return suite
