# (asimtote) tests.ios.config
#
# Copyright (C) Robert Franklin <rcf34@cam.ac.uk>



import unittest

from asimtote.ios import CiscoIOSConfig



class TestAsimtote_CiscoIOSConfig(unittest.TestCase):
    def setUp(self):
        self.cfg = CiscoIOSConfig()


    def test_globals(self):
        c = """
hostname TestRouter
"""

        self.cfg.parse_str(c)
        self.assertEqual(self.cfg, { "hostname": "TestRouter" })
