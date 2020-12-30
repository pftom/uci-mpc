#!/bin/bash
ENDPOINTS=0:127.0.0.1:11111,1:127.0.0.1:22222

python align_and_filter.py alice.dat 1 0 $ENDPOINTS False 2>&1 >/dev/null &

python align_and_filter.py bob.dat 13 1 $ENDPOINTS True