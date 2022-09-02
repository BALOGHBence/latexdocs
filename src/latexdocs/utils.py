# -*- coding: utf-8 -*-
try:
    from collections.abc import Iterable
except ImportError:
    from collections import Iterable
import six

from pylatex import (NoEscape, Section, Subsection, Subsubsection)


def expr_to_ltx(lhs, rhs, *args, env='{equation}', sign='=',
                dfrac=False, pre=None, post=None, **kwargs):
    if dfrac:
        lhs = lhs.replace('frac', 'dfrac')
        rhs = rhs.replace('frac', 'dfrac')
    if isinstance(pre, str):
        lhs = ' '.join([pre, lhs])
    if isinstance(post, str):
        rhs = ' '.join([rhs, post])
    return NoEscape(
        r"""
        \begin{env}
            {lhs} {sign} {rhs}
        \end{env}
        """.format(env=env,
                   lhs=lhs,
                   sign=sign,
                   rhs=rhs
                   )
    )


def expr_to_ltx_breqn(lhs, rhs, *args, env='{dmath}', **kwargs):
    return expr_to_ltx(lhs, rhs, *args, env=env, **kwargs)


def eq_to_ltx_multiline(lhs, rhs, *args, nsplit=2, **kwargs):
    kwargs['env'] = '{multline}'


def section(title: str, *args, level=1, **kwargs):
    if level == 1:
        return Section(title, *args, **kwargs)
    elif level == 2:
        return Subsection(title, *args, **kwargs)
    elif level == 3:
        return Subsubsection(title, *args, **kwargs)
    raise NotImplementedError


def issequence(arg) -> bool:
    """
    Returns `True` if `arg` is any kind of iterable, but not a string,
    returns `False` otherwise.

    Examples
    --------
    >>> from latexdocs.utils import issequence
    >>> issequence([1, 2])
    True

    >>> issequence('lorem ipsum')
    False    
    """
    return (
        isinstance(arg, Iterable)
        and not isinstance(arg, six.string_types)
    )


def floatformatter(*args, sig: int = 6, **kwargs) -> str:
    """
    Returns a formatter, which basically is a string template
    ready to be formatted.

    Parameters
    ----------
    sig : int, Optional
        Number of significant digits. Default is 6.

    Returns
    -------
    str
        The string to be formatted.
        
    Example
    --------
    Print the value of pi as a string with 4 significant digits:

    >>> from latexdocs.utils import floatformatter
    >>> import math
    >>> formatter = floatformatter(sig=4)
    >>> formatter.format(math.pi)
    '3.142'

    """
    return "{" + "0:.{}g".format(sig) + "}"


def float_to_str_sig(value, *args, sig: int = 6, atol: float = 1e-7,
                     **kwargs) -> str:
    """
    Returns a string representation of a floating point number, with
    given significant digits.

    Parameters
    ----------
    value : float or a list of float
        A single value, or an iterable.

    sig : int
        Number of significant digits.

    atol : float
        Floating point tolerance. Values smaller than this 
        in the absolute sense are treated as zero.

    Returns
    -------
    str or list of str
        String representation of the provided input.

    Example
    --------
    Print the value of pi as a string with 4 significant digits:

    >>> from latexdocs.utils import float_to_str_sig
    >>> import math
    >>> float_to_str_sig(math.pi, sig=4)
    '3.142'

    """
    if not issequence(value):
        if atol is not None:
            if abs(value) < atol:
                value = 0.0
        return floatformatter(sig=sig).format(value)
    else:
        try:
            import numpy as np
        except ImportError:
            raise ImportError("You need numpy for this.")
        value = np.array(value)
        if atol is not None:
            inds = np.where(np.abs(value) < atol)[0]
            value[inds] = 0.0
        formatter = floatformatter(sig=sig)
        def f(v): return formatter.format(v)
        return list(map(f, value))
