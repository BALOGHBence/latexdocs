# -*- coding: utf-8 -*-
try:
    from collections.abc import Iterable
except ImportError:
    from collections import Iterable


def alphabet(abctype: str = 'latin', **kwargs) -> Iterable:
    if abctype in ('ord', 'o'):
        start = kwargs.pop('start', 0)
    elif abctype in ('latin', 'l'):
        start = ord(kwargs.pop('start', 'a'))
    elif abctype == 'u':
        start = ord(kwargs.pop('start', '\u0000'))
    elif abctype in ('greek', 'g'):
        start = ord(kwargs.pop('start', '\u03b1'))
    while True:
        yield chr(start)
        start += 1


def ordrange(N: int = 1, **kwargs) -> Iterable:
    start = kwargs.pop('start', 0)
    if isinstance(start, str):
        start = ord(start)
    stop = kwargs.pop('stop', None)
    if stop is None or stop == start:
        stop = start + N
    return [chr(c) for c in range(start, stop)]


def latinrange(N: int = 1, **kwargs) -> Iterable:
    start = kwargs.pop('start', 97)
    stop = kwargs.pop('stop', None)
    return ordrange(N, start=start, stop=stop)


def urange(N: int = 1, **kwargs) -> Iterable:
    start = kwargs.pop('start', '\u0000')
    stop = kwargs.pop('stop', None)
    if stop is None:
        stop = start
    return ordrange(N, start=ord(start), stop=ord(stop))


def greekrange(N: int = 1) -> Iterable:
    return urange(N, start='\u03b1')


def arabicrange(N: int = 1, **kwargs) -> Iterable:
    start = kwargs.pop('start', 0)
    stop = kwargs.pop('stop', None)
    if stop is None or stop == start:
        stop = start + N
    return [str(c) for c in range(start, stop)]