# -*- coding: utf-8 -*-
from typing import Iterable
import pylatex as pltx
import numpy as np

from .items import BaseTexDocItem


class XTabular(pltx.Tabular):
    """
    A class to represent tables that may span across pages.

    This uses the ``xtab`` package.
    """

    _latex_name = 'xtabular'

    packages = [pltx.Package('xtab')]


class Table(BaseTexDocItem):
    """
    A class to handle tables using the `tabular` enviroment.
    
    Parameters
    ----------
    table_spec : str, Optional
        Controls alignment of the columns. If not provided, a default setting
        is inferred from the `columns` argument, is provided. Default is None.
        
    pos : str, Optional
        Control the position of the table. Default is 'h'.
    
    columns : Iterable, Optional
        Column labels. Default is None.
        
    data : Iterable, Optional
        The data content of the table. Default is None.
        
    hline : bool, Optional
        Controls wether horizontal lines are to be added after rows or not.
        Only if data is provided at creation. Default is False.
        
    centering : bool, Optional
        Controls wether the table is centralized or not. Default is True.
        
    caption : str, Optional
        The caption of the table.
        
    label : str, Optional
        The label of the table for later referencing.
    
    Example
    -------
    >>> from latexdocs import Document, Table
    >>> doc = Document()
    >>> columns = ['A', 'B', 'C', 'D']
    >>> data = np.array([[1, 2, 3, 4], [5, 6, 7, 8]])
    >>> doc.append(Table(data=data, columns=columns))
    
    >>> table = Table('c c c c', pos='h', caption="This is a table.", label="table:tblref")
    >>> table.add_hline()
    >>> table.add_row(('Case', "Method 1", "Method 2", "Method 3"))
    >>> table.add_hline()
    >>> table.add_hline()
    >>> table.add_row((1, 50, 837, 321))
    >>> table.add_row((2, 60, 437, 142))
    >>> table.add_row((3, 70, 857, 708))
    >>> table.add_row((4, 80, 172, 710))
    >>> table.add_hline()
    >>> doc.append(table)
    
    See Also
    --------
    :class:`pylatex.table.Tabular`
    
    """
    
    _tlbcls_ = pltx.Tabular

    def __init__(self, table_spec=None, pos='h', *, columns=None, data=None,
                 hlines=False, centering=True, caption=None, label=None, **kwargs):
        super().__init__(**kwargs)
        if data is not None:
            if not isinstance(data, np.ndarray):
                data = np.array(data)
        if table_spec is None:
            if data is not None:
                assert columns is not None, "Labels must be provided alongside data."
                table_spec = 'c'.join(['|', ] * (len(columns) + 1))
        self._data = data
        self._columns = columns
        self._caption = caption
        self._hlines = hlines
        self._centering = centering
        self._pos = pos
        self._label = label
        self._table = self._tlbcls_(table_spec)

    def add_hline(self, *args, **kwargs):
        """
        Adds a horizontal line to the table. The call is forwarded to 
        :class:`pylatex.table.Tabular`.
        """
        self._table.add_hline(*args, **kwargs)
    
    def add_row(self, *args, **kwargs):
        """
        Adds a new row to the table. The call is forwarded to 
        :class:`pylatex.table.Tabular`.
        """
        self._table.add_row(*args, **kwargs)

    def add_rows(self, data: Iterable, **kwargs):
        """
        Adds multiple rows to the table. The call is forwarded to 
        :class:`pylatex.table.Tabular`.
        """
        for d in data:
            self._table.add_row(d, **kwargs)

    def add_empty_row(self):
        """
        Adds an empty row to the table. The call is forwarded to 
        :class:`pylatex.table.Tabular`.
        """
        self._table.add_empty_row()

    def _append2doc_(self, doc, *args, **kwargs):        
        before = r"\begin{}[{}]".format(r'{table}', self._pos)        
        if self._centering:
            before += r"\centering"
        doc.append(pltx.NoEscape(before))
        
        if self._data is not None:
            self._table.add_hline()
            self._table.add_row(self._columns)
            self._table.add_hline()
            nR, _ = self._data.shape
            for iR in range(nR):
                self._table.add_row(self._data[iR])
                if self._hlines:
                    self._table.add_hline()
            self._table.add_hline()
        doc.append(pltx.NoEscape(self._table.dumps()))
            
        after = ""
        if self._caption is not None:
            c = "{" + self._caption + "}"
            after += r"\caption{}".format(c)
        if self._label is not None:
            c = "{" + self._label + "}"
            after += r"\label{}".format(c)
        after += r"\end{table}"
        doc.append(pltx.NoEscape(after))
        
        return doc


class TableX(Table):
    """
    A class to handle tables using the `tabularx` enviroment.

    Example
    -------
    >>> from latexdocs import Document, TableX
    >>> doc = Document()
    >>> columns = ['A', 'B', 'C', 'D']
    >>> data = np.array([[1, 2, 3, 4], [5, 6, 7, 8]])
    >>> nD = data.shape[-1]
    >>> table_spec = r"|".join(nD * [r">{\centering\arraybackslash}X",])
    >>> doc.append(TableX(table_spec, 'h!', data=data, columns=labels))

    """
    
    _tlbcls_ = pltx.Tabularx
