#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Author: fanwei.zeng
# Time: 2019/3/23 17:22
import time
import unittest

from redis_funnel.distributed import qps_factory
import redis


qps = qps_factory(host="localhost", port=6379, db=0)


def dummy():
    pass


class TestDistributedQps(unittest.TestCase):
    def setUp(self):
        self.r = redis.Redis(host="localhost", port=6379, db=0)

    def tearDown(self):
        pass

    def gen_f(self, n):
        self.r.delete("1000001:test")
        return qps("1000001", "test", n)(dummy)

    def test_qps(self):
        for max_qps in xrange(0, 10000, 100):
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
