#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Author: fanwei.zeng
# Time: 2019/3/24 13:08
import time
import unittest

from redis_funnel.local import qps


def dummy():
    pass


class TestLocalQps(unittest.TestCase):
    def setUp(self):
        pass

    def tearDown(self):
        pass

    @staticmethod
    def gen_f(n):
        return qps(n)(dummy)

    def test_qps(self):
        for max_qps in xrange(0, 500000, 1000):
            if max_qps == 0:
                max_qps = 1
            seconds = 10
            count = 0
            f = self.gen_f(max_qps)
            start = time.time()
            while time.time() - start <= seconds:
                f()
                count += 1

            real_qps = count / float(seconds)
            print "%s,%s" % (max_qps, real_qps)
            self.assertTrue(real_qps <= max_qps)


if __name__ == "__main__":
    unittest.main()
