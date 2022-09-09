# -*- coding: utf-8 -*-
import pylatex as pltx
from abc import abstractmethod

from .base import TexBase
from .preamble import append_packages, append_cover
from .utils import section


_default_geometry_options_ = {
    "tmargin": "1.5cm",
    "lmargin": "1.5cm",
    "rmargin": "1.5cm"
}


class BaseTexDoc(TexBase):
    """
    Base class for all document types.

    """
    documentclass = None

    def __init__(self, *args, geometry_options=None, title=None, author=None,
                 date=False, doc=None, content=None, **kwargs):
        super().__init__(*args, **kwargs)
        isroot = self.is_root()
        if title is not None:
            assert isroot, "Only the root object can have a title!"
        if author is not None:
            assert isroot, "Only the root object can have an author!"
        title = title if title is not None else 'Documentation'
        self._title = title
        self._author = author
        self._date = date
        self._content = content if content is not None else []
        if geometry_options is None:
            geometry_options = _default_geometry_options_
        self._geometry_options = geometry_options
        self._doc = doc

    @property
    def title(self) -> str:
        """
        Returns the title of the document.

        """
        return self.root()._title

    @property
    def doc(self) -> pltx.Document:
        """
        Returns the underlying document instance.

        """
        return self.root()._doc

    @abstractmethod
    def init_doc(self, **kwargs) -> pltx.Document:
        """
        Override this to create a new document type.

        """
        ...

    def _adopt_child_(self, child):
        if isinstance(child, BaseTexDoc):
            child.parent = self
        return child

    def is_nested(self, **kwargs) -> bool:
        """
        Returns `True` if the current section has subsections, `False` otherwise.

        """
        level = kwargs.get('_level', self.depth)
        return (self.has_children() or len(self.content) > 0) and level <= 3

    def has_children(self):
        return any(map(lambda v: isinstance(v, BaseTexDoc), self.values()))

    def _append2doc_(self, doc, *args, level=None, nosection=False, **kwargs):
        level = level if level is not None else self.depth
        if self.is_nested(_level=level) and not nosection:
            with doc.create(section(self.key, level=level)):
                for c in self.content:
                    if hasattr(c, '_append2doc_'):
                        doc = c._append2doc_(doc, level=level, nosection=True)
                    else:
                        doc.append(c)
        else:
            for c in self.content:
                if hasattr(c, '_append2doc_'):
                    doc = c._append2doc_(doc, level=level, nosection=True)
                else:
                    doc.append(c)
        return doc

    def build(self, *args, **kwargs) -> pltx.Document:
        """
        Builds and returns an instance of :class:`pylatex.document.Document`.

        Example
        -------
        >>> from latexdocs import Document
        >>> doc = Document(title='Title', author='Author', date=True)
        >>> doc['Section 1'].append('Some regular text')
        >>> doc.build()

        """
        doc = kwargs.get('_doc', None)
        level = kwargs.get('_level', None)
        if doc is None:
            assert self.is_root()
            doc = self.init_doc()
            return self.build(_doc=doc, _level=0)
        else:
            assert isinstance(level, int)
            if level == 0:
                doc = self._append2doc_(doc, level=level, nosection=True)
            else:
                doc = self._append2doc_(doc, level=level)
            for v in self.values():
                if isinstance(v, BaseTexDoc):
                    v.build(_doc=doc, _level=level+1)
            return doc

    def generate_pdf(self, *args, clean_tex=False, compiler='pdflatex', **kwargs):
        """
        Builds the document and generates a pdf in one go.

        Parameters
        ----------
        args : tuple, Optional
            Extra positional arguments are forwarded to `pylatex.Document.generate_pdf`.

        clean_tex : bool, Optional
            Default is False.

        compiler : str, Optional
            The compiler to use. Default is `pdflatex`. See the docs of PyLaTeX
            for all the available options.

        kwargs : tuple, Optional
            Extra kyeword arguments are forwarded to `pylatex.Document.generate_pdf`.

        Example
        -------
        >>> from latexdocs import Document
        >>> doc = Document(title='Title', author='Author', date=True)
        >>> doc['Section 1'].append('Some regular text')
        >>> doc.generate_pdf('filename', compiler='pdflatex')

        """
        self.build().generate_pdf(*args, clean_tex=clean_tex, compiler=compiler, **kwargs)


class Document(BaseTexDoc):
    """
    Base class to store information about a document.

    Parameters
    ----------
    geometry_options : dict, Optional
        A dictionary containing information about the geometry of the
        document. Default is None.

    title : str, Optional
        The title of the document. Default is None.

    author : str, Optional
        The author of the document. Default is None.

    date : bool, Optional
        If True, a date is show on the title page. Default is False.

    doc : :class:`pylatex.document.Document`, Optional
        An instance of `pylatex.Document`, if you already have one.
        Default is None.

    content : list, Optional
        Content related to the current section. Default is None.    

    Notes
    -----
    The implementation is not foolproof. For instance, if you ask for the date 
    to be shown but provide no title or author, you are gonna experience problems
    which I don't care about (the author). Don't be dumb.

    Example
    -------
    >>> from latexdocs import Document
    >>> doc = Document(title='Title', author='Author', date=True)

    See Also
    --------
    :class:`linkeddeepdict.LinkedDeepDict`
    :class:`pylatex.document.Document`

    """

    documentclass = 'article'

    def init_doc(self, maketitle=None, **kwargs) -> pltx.Document:
        """
        Initializes the document. This covers appending packages
        and the preamble.

        """
        dcls = self.__class__.documentclass
        kwargs['documentclass'] = kwargs.get('documentclass', dcls)
        kwargs['geometry_options'] = self._geometry_options
        doc = pltx.Document(**kwargs)
        doc = append_packages(doc)
        doc = append_cover(doc, self._title, self._author, self._date)
        return doc


class Article(Document):
    """
    Top level class for articles.

    Example
    -------
    >>> from latexdocs import Article
    >>> doc = Article(title='Title', author='Author', date=True)

    See Also
    --------
    :class:`linkeddeepdict.LinkedDeepDict`
    :class:`pylatex.document.Document`

    """
    documentclass = 'article'


class Book(Document):
    """
    Top level class for books.

    Example
    -------
    >>> from latexdocs import Book
    >>> doc = Book(title='Title', author='Author', date=True)

    See Also
    --------
    :class:`linkeddeepdict.LinkedDeepDict`
    :class:`pylatex.document.Document`

    """
    documentclass = 'book'
