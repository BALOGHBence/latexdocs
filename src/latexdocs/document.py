# -*- coding: utf-8 -*-
import pylatex as pltx
from linkeddeepdict import LinkedDeepDict

from .utils import append_packages, append_preamble, section, float_to_str_sig


_default_geometry_options_ = {
    "tmargin": "1.5cm",
    "lmargin": "1.5cm",
    "rmargin": "1.5cm"
}

class TexDocument(LinkedDeepDict):
    

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
    def name(self):
        return self._name

    @property
    def content(self):
        return self._content

    @property
    def title(self):
        return self._title

    @property
    def doc(self):
        return self._doc

    def init_doc(self) -> pltx.Document:
        doc = pltx.Document(geometry_options=self._geometry_options)
        doc = append_packages(doc)
        doc = append_preamble(doc, self._title, self._author, self._date)
        return doc

    def _adopt_child_(self, child):
        if isinstance(child, TexDocument):
            child.parent=self
        return child

    def append(self, *args):
        if len(args) > 0:
            args = list(map(self._adopt_child_, args))
        return self._content.append(*args)

    def is_nested(self, **kwargs):
        level = kwargs.get('_level', self.depth)
        return (self.has_children() or len(self.content) > 0) and level <= 3

    def has_children(self):
        return any(map(lambda v: isinstance(v, TexDocument), self.values()))

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
        doc = kwargs.get('_doc', None)
        level = kwargs.get('_level', None)
        if doc is None:
            assert self.is_root()
            if doc is None:
                doc = self.init_doc()
            append_packages(doc)
            append_preamble(doc, self._title, self._author, self._date)
            return self.build(_doc=doc, _level=0)
        else:
            assert isinstance(level, int)
            if level == 0:
                doc = self._append2doc_(doc, level=level, nosection=True)
            else:
                doc = self._append2doc_(doc, level=level)
            for v in self.values():
                if isinstance(v, TexDocument):
                    v.build(_doc=doc, _level=level+1)
            return doc

    def generate_pdf(self, *args, clean_tex=False, compiler='pdfLaTeX', **kwargs):
        self.build().generate_pdf(*args, clean_tex=clean_tex, compiler=compiler, **kwargs)


class Document(TexDocument):
    
    documentclass='article'
    
    def __init__(self, *args, parent=None, **kwargs):
        assert parent is None, "Article must be at the top."
        super().__init__(*args, parent=None, **kwargs)
        
    def init_doc(self) -> pltx.Document:
        doc = pltx.Document(geometry_options=self._geometry_options)
        doc = append_packages(doc)
        doc = append_preamble(doc, self._title, self._author, self._date)
        return doc


class Article(Document):
    
    documentclass='article'
    
    def init_doc(self) -> pltx.Document:
        doc = pltx.Document(geometry_options=self._geometry_options)
        doc = append_packages(doc)
        doc = append_preamble(doc, self._title, self._author, self._date)
        return doc
    
    
class Book(Document):
    
    documentclass='book'
    
    def init_doc(self) -> pltx.Document:
        doc = pltx.Document(geometry_options=self._geometry_options)
        doc = append_packages(doc)
        doc = append_preamble(doc, self._title, self._author, self._date)
        return doc

#%%

class TikZFigure(TexDocument):

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
    

class Text(TexDocument):

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


class Table(TexDocument):

    def __init__(self, *args, labels=None, data=None, table_spec=None, hline=False, **kwargs):
        super().__init__(*args, **kwargs)
        if table_spec is None:
            assert labels is not None
            table_spec = 'c'.join(['|',] * (len(labels) + 1))
        self._table_spec = table_spec
        self._data = data
        self._labels = labels
        self._hline = hline
        self._content = [None]

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
    

class TableX(TexDocument):

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
        self._content = [None]
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


class Image(TexDocument):

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
    
    def _append2doc_(self, doc, *args, level=None, **kwargs):
        with doc.create(pltx.Figure(position=self.position)) as pic:
            pic.add_image(self.filename, width=self.width)
            pic.add_caption(self.caption)
        return doc
    