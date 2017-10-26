#! /bin/sh
export DJ_PASS='fixme';
exec python -mcProfile -o perftest.out perftest.py;
