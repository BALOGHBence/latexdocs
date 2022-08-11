# -*- coding: utf-8 -*-
from pylatex import (NoEscape, Package, Command)
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
    
    if packages is not None:
        packages = __default__packages__
    
    for pkg, options in packages.items():
        pkgo = options if len(options) > 0 else None
        doc.packages.append(Package(pkg, options=pkgo))    

    return doc


def append_cover(doc, title=None, author=None, date=True):
    if title is not None:
        doc.preamble.append(Command('title', title))
    if author is not None:
        doc.preamble.append(Command('author', author))
    if date:
        doc.preamble.append(Command('date', NoEscape(r'\today')))
    return doc