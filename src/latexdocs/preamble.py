# -*- coding: utf-8 -*-
from pylatex import (NoEscape, Package, Command, NewPage)
from linkeddeepdict import LinkedDeepDict


__default__packages__ = LinkedDeepDict()

# Tools related to displaying math.
__default__packages__['amsmath']

# for the 'operatorname' command, frequently to print symbols
__default__packages__['amsopn']

# To automatically break long equations into multiple lines.
__default__packages__['breqn']

# For the \coloneqq command, and the defining equality symbol ':='.
__default__packages__['mathtools']

__default__packages__['enumitem'] # to customize enumerations
__default__packages__['xcolor'] # colors
__default__packages__['lmodern'] # high quality fonts

# to insert pgf files
__default__packages__['pgf']
__default__packages__['pgfplots']
__default__packages__['pdfpages']

# tables and other floats
__default__packages__['float']
__default__packages__['tabularx']


def append_packages(doc, packages=None):
    if packages is None:
        packages = __default__packages__
    for pkg, options in packages.items():
        pkgo = options if len(options) > 0 else None
        doc.packages.append(Package(pkg, options=pkgo))    
    return doc


def append_cover(doc, title=None, author=None, date=True, maketitle=False):
    """
    Appends a cover page to the document.
    
    Parameters
    ----------
    title : str, Optional
        The title of the document. Default is None.

    author : str, Optional
        The author of the document. Default is None.

    date : bool, Optional
        If True, a date is show on the title page. Default is False.
     
    """
    if maketitle:
        maketitle = False
        if title is not None:
            maketitle = True
            doc.preamble.append(Command('title', title))
        if author is not None:
            maketitle = True
            doc.preamble.append(Command('author', author))
        if date:
            maketitle = True
            doc.preamble.append(Command('date', NoEscape(r'\today')))
        if maketitle:
            doc.append(NoEscape(r'\maketitle'))
            doc.append(NewPage())
            doc.append(NoEscape(r'\tableofcontents'))
            doc.append(NewPage())
    return doc