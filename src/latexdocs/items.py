# -*- coding: utf-8 -*-
import pylatex as pltx
from abc import abstractmethod

from .base import TexBase
from .utils import float_to_str_sig


class BaseTexDocItem(TexBase):
    """
    Base class for all document items.
    
    """
    
    def __init__(self, *args, content=None, **kwargs):
        c = content if content is not None else []
        if len(args) > 0:
            c += list(args)
        super().__init__(content=c, **kwargs)
                                
    @abstractmethod
    def _append2doc_(self, doc, *args, **kwargs):
        """
        Override this to create a new document item type.
        
        """
        ...


class TikZFigure(BaseTexDocItem):
    """
    A class to handle TikZ figures.
    
    Example
    -------
    >>> from latexdocs import Document, TikZFigure
    >>> doc = Document(title='Title', author='Author', date=True)
    >>> fig = TikZFigure(plot_options='height=4cm, width=6cm, grid=major')
    >>> fig.append(Plot(name='model', func='-x^5 - 242'))
    >>> coordinates = [
    >>>     (-4.77778, 2027.60977),
    >>>     (-3.55556, 347.84069),
    >>>     (-2.33333, 22.58953),
    >>>     (-1.11111, -493.50066),
    >>>     (0.11111, 46.66082),
    >>>     (1.33333, -205.56286),
    >>>     (2.55556, -341.40638),
    >>>     (3.77778, -1169.24780),
    >>>     (5.00000, -3269.56775),
    >>> ]
    >>> fig.append(Plot(name='estimate', coordinates=coordinates))
    >>> doc['Section', 'Subsection'].append(fig)
    
    """

    def __init__(self, *args, plot_options=None, **kwargs):
        super().__init__(*args, **kwargs)
        if plot_options is None:
            plot_options = 'height=4cm, width=6cm, grid=major'
        self.plot_options = plot_options

    def _append2doc_(self, doc, *args, **kwargs):
        with doc.create(pltx.TikZ()):
            with doc.create(pltx.Axis(options=self.plot_options)) as plot:
                for c in self.content:
                    plot.append(c)
        return doc
    

class Text(BaseTexDocItem):
    """
    A class to handle simple text content.
    
    Parameters
    ----------
    txt : str
        The content.
        
    bold : bool, Optional
        Default is None.
        
    """
    
    def __init__(self, txt, *args, bold=False, **kwargs):
        super().__init__(*args, **kwargs)
        if bold:
            self._content = [r"\textbf" + ("{" + txt + '}')]
        else:
            self._content = [txt]
        self.bold = bold

    def _append2doc_(self, doc, *args, **kwargs):
        for c in self.content:
            doc.append(pltx.NoEscape(c))
        return doc    


class Table(BaseTexDocItem):
    """
    A class to handle tables using the `tabular` enviroment.
    
    Example
    -------
    >>> from latexdocs import Document, Table
    >>> doc = Document(title='Title', author='Author', date=True)
    >>> labels = ['A', 'B', 'C', 'D']
    >>> data = np.array([[1, 2, 3, 4], [5, 6, 7, 8]])
    >>> doc['Tables'].append(Table(data=data, labels=labels))
    
    """

    def __init__(self, *args, labels=None, data=None, table_spec=None, hline=False, **kwargs):
        super().__init__(*args, **kwargs)
        if table_spec is None:
            assert labels is not None
            table_spec = 'c'.join(['|',] * (len(labels) + 1))
        self._table_spec = table_spec
        self._data = data
        self._labels = labels
        self._hline = hline

    def _append2doc_(self, doc, *args, **kwargs):
        table = pltx.Tabular(self._table_spec)
        table.add_hline()
        table.add_row(self._labels)
        table.add_hline()
        nR, _ = self._data.shape
        for iR in range(nR):
            table.add_row(self._data[iR])
            if self._hline:
                table.add_hline()
        table.add_hline()
        doc.append(table)
        return doc
    

class TableX(BaseTexDocItem):
    """
    A class to handle tables using the `tabularx` enviroment.
    
    Example
    -------
    >>> from latexdocs import Document, TableX
    >>> doc = Document(title='Title', author='Author', date=True)
    >>> labels = ['A', 'B', 'C', 'D']
    >>> data = np.array([[1, 2, 3, 4], [5, 6, 7, 8]])
    >>> doc['Tables'].append(TableX(data=data, labels=labels, table_spec=r"X|X|X|X"))
    
    """

    def __init__(self, *args, labels=None, data=None, table_spec=None, 
                 hline=False, before=None, after=None, **kwargs):
        super().__init__(*args, **kwargs)
        if table_spec is None:
            assert labels is not None
            table_spec = r'X'.join(['|',] * (len(labels)+1))
        self._table_spec = table_spec
        self._data = data
        self._labels = labels
        self._hline = hline
        self.before = before
        self.after = after

    def _append2doc_(self, doc, *args, **kwargs):
        if self.before is None:
            n = len(self._labels)
            spec = r'{' + self._table_spec +  r'}'
            before = r"\begin{}{}{}".format(r'{tabularx}', r'{\textwidth}', spec)
        else:
            before = self.before
        doc.append(pltx.NewLine())
        doc.append(pltx.NoEscape(before))
                
        header = r'&'.join(self._labels) + r" \\ "
        doc.append(pltx.NoEscape(header))
        doc.append(pltx.NoEscape(r"\hline"))
        
        nR, _ = self._data.shape
        frmt = lambda x : float_to_str_sig(x, sig=4)
        for iR in range(nR):
            item = r'&'.join(map(frmt, self._data[iR])) + r" \\ "
            doc.append(pltx.NoEscape(item))
        
        if self.after is None:
            after = r"\end{tabularx}"
        else:
            after = self.after
        doc.append(pltx.NoEscape(after))
        return doc


class Image(BaseTexDocItem):
    """
    A class to embed images in your document.

    Example
    -------
    Assuming you have a file `image.png` on your local filesystem:
    
    >>> from latexdocs import Document, Image
    >>> doc = Document(title='Title', author='Author', date=True)
    >>> img = Image(filename="image.png", position='h!', caption=None, width='350px')
    
    """

    def __init__(self, *args, position=None, width=None, filename=None, 
                 caption=None, w=None,**kwargs):
        super().__init__(*args, **kwargs)
        if filename is None:
            assert len(args) > 0, "No filepath provided!"
            assert isinstance(
                args[0], str), "The path of the file must be a string."
            filename = args[0]
        width = width if w is None else w
        if isinstance(width, str):
            if width.lower() == 'full':
                width = pltx.NoEscape(r"\textwidth")
        self.width = 7.5 if width is None else width
        self.position = 'H' if position is None else position
        self.caption = caption if caption is not None else ''
        self.filename = filename

    @classmethod
    def from_plt(cls, path, *args, **kwargs):
        import matplotlib.pyplot as plt
        plt.savefig(path)
        return Image(*args, filename=path, **kwargs)
    
    def _append2doc_(self, doc, *args, **kwargs):
        with doc.create(pltx.Figure(position=self.position)) as pic:
            pic.add_image(self.filename, width=self.width)
            pic.add_caption(self.caption)
        return doc
    