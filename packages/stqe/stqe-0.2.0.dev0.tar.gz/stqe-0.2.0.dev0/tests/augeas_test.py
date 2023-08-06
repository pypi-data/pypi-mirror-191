#!/usr/bin/python


import unittest

from libsan.host.mp import mp_enable, mpath_conf_match, mpath_conf_remove, mpath_conf_set


class TestAugeas(unittest.TestCase):
    def test_validate_mpath_conf(self):
        test_string = "TEST123"
        # This tests if changes done to multipath.conf are valid
        assert mp_enable() is True
        assert mpath_conf_set("/blacklist/wwid[last()+1]", test_string) is True
        assert mpath_conf_remove(mpath_conf_match("/blacklist/wwid", test_string), test_string) is True
