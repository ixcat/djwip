#! /usr/bin/env python

import pstats
p = pstats.Stats('perftest.out')
p.strip_dirs().sort_stats('cumtime').print_stats()
