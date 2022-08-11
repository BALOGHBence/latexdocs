# -*- coding: utf-8 -*-
try:
    from collections.abc import Iterable
except ImportError:
    from collections import Iterable
import six

from pylatex import (NoEscape, Package, Command,
                     Section, Subsection, Subsubsection)


def append_packages(doc):

    # Tools related to displaying math.
    doc.packages.append(Package('amsmath'))

    # Sympy uses the 'operatorname' command frequently to print symbols.
    doc.packages.append(Package('amsopn'))

    # To automatically break long equations into multiple lines.
    doc.packages.append(Package('breqn'))

    # For the \coloneqq command, and the defining equality symbol ':='.
    doc.packages.append(Package('mathtools'))

    # Miscallenaous
    doc.packages.append(Package('enumitem'))  # to customize enumerations
    doc.packages.append(Package('xcolor'))  # colors
    doc.packages.append(Package('lmodern'))  # high quality fonts

    # to insert pgf files
    doc.packages.append(Package('pgf'))
    doc.packages.append(Package('pgfplots'))
    doc.packages.append(Package('pdfpages'))

    # tables
    # doc.packages.append(Package('tabular'))
    doc.packages.append(Package('tabularx'))
    
    # precise positioning of figures and other floats
    doc.packages.append(Package('float'))

    return doc


def append_preamble(doc, title=None, author=None, date=True):
    if title is not None:
        doc.preamble.append(Command('title', title))
    if author is not None:
        doc.preamble.append(Command('author', author))
    if date:
        doc.preamble.append(Command('date', NoEscape(r'\today')))
    return doc


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
    The formatter to use to print a floating point number with 4 digits:

    >>> from dewloosh.core.tools import issequence
    >>> issequence([1, 2])
    True

    To print the actual value as a string:

    >>> issequence('lorem ipsum')
    False    
    """
    return (
        isinstance(arg, Iterable)
        and not isinstance(arg, six.string_types)
    )


def floatformatter(*args, sig: int = 6, **kwargs) -> str:
    """
    Returns a formatter, which essantially a string temapate
    ready to be formatted.

    Parameters
    ----------
    sig : int, Optional
        Number of significant digits. Default is 6.

    Returns
    -------
    string
        The string to be formatted.

    """
    return "{" + "0:.{}g".format(sig) + "}"


def float_to_str_sig(value, *args, sig: int = 6, atol: float = 1e-7,
                     **kwargs) -> str:
    """
    Returns a string representation of a floating point number, with
    given significant digits.

    Parameters
    ----------
    value : float or a sequence of floats
        A single value, or an iterable.

    sig : int
        Number of significant digits.

    atol : float
        Floating point tolerance. Values smaller than this 
        in the absolute sense are treated as zero.

    Returns
    -------
    string or a sequence of strings
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
