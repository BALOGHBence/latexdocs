# -*- coding: utf-8 -*-
import pylatex as pltx
from abc import abstractmethod

from .base import TexBase


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
    
    Parameters
    ----------
    plot_options : str, Optional
        Options to control the layout. See the examples.
        Default is 'height=4cm, width=6cm, grid=major'.
    
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
        Default is False.
        
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


class Image(BaseTexDocItem):
    """
    A class to embed images in your document.
    
    Parameters
    ----------
    *args : tuple, Optional
        The first positional argument can be the full path to a file.
        
    position : str, Optional
        Controls the position of the figure. Default is 'H'.
        
    width or w : int, Optional
        The width of the image.
        
    filename : str, Optional
        The full path of the file to read. The path must be provided
        either with this argument, or as the first position argument. 
        Default is None.

    caption : str, Optional
        The caption of the table.

    Example
    -------
    Assuming you have a file `image.png` on your local filesystem:
    
    >>> from latexdocs import Document, Image
    >>> doc = Document()
    >>> img = Image("image.png", position='h!', width='350px')
    
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
        self._width = 7.5 if width is None else width
        self._position = 'H' if position is None else position
        self._caption = caption
        self._filename = filename

    @classmethod
    def from_plt(cls, path, *args, **kwargs):
        """
        Returns an instance from the currently active matplotlib figure.
        
        Parameters
        ----------
        path : str
            The path where the file is to be stored.
            
        """
        import matplotlib.pyplot as plt
        plt.savefig(path)
        return Image(*args, filename=path, **kwargs)
    
    def _append2doc_(self, doc, *args, **kwargs):
        with doc.create(pltx.Figure(position=self._position)) as pic:
            pic.add_image(self._filename, width=self._width)
            if self._caption is not None:
                pic.add_caption(self._caption)
        return doc
    