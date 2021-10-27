#!/usr/bin/env python3

import re

example = """
 T/V                N    NB     P     Q               Time                 Gflops
--------------------------------------------------------------------------------
WR11C2R4      115200   192     6     8            3417.23             2.9826e+02
HPL_pdgesv() start time Mon May 24 01:41:36 2021

HPL_pdgesv() end time   Mon May 24 02:38:33 2021

--------------------------------------------------------------------------------
||Ax-b||_oo/(eps*(||A||_oo*||x||_oo+||b||_oo)*N)=   2.22081836e-03 ...... PASSED
================================================================================
"""

def parse_hpl(text):
    cols = "T/V N NB P Q Time Gflops".split()
    types = [str, int, int, int, int, float, float]
    hdr = re.compile(r'\s*' + r'\s+'.join(cols) + r'\s*$')
    expr = re.compile(r'\s*' + r'\s+'.join(r'(\S+)' for _ in cols) + r'\s*$')
    ans = {k:[] for k in cols}

    state = 0
    for line in text.split('\n'):
        #print(state,line)
        if state == 0 and hdr.match(line):
            state = 1
            continue
        if state == 1 and re.match('-+\s*$', line):
            state = 2
            continue
        if state == 2:
            m = expr.match(line)
            if not m:
                state = 0
                continue
            for i,k in enumerate(cols):
                ans[k].append(types[i](m[i+1]))
    return ans

def test_parse_hpl():
    ans = parse_hpl(example)
    print(ans)
    assert len(ans['Gflops']) == 1
    assert ans['Gflops'][0] > 0.0
