# -*- coding: utf-8 -*-
from linkeddeepdict import LinkedDeepDict
from abc import abstractmethod


class TexBase(LinkedDeepDict):
    """
    Base class for all document items.
    
    """
    
    def __init__(self, *args, content=None, **kwargs):
        super().__init__(*args, **kwargs)
        self._content = content if content is not None else []
        
    @property
    def name(self) -> str:
        """
        Returns the name of the current section.
        
        """
        return self._name
        
    @property
    def content(self) -> list:
        """
        Returns the content of the current section.
        
        """
        return self._content
    
    def _adopt_child_(self, child):
        if isinstance(child, TexBase):
            child.parent = self
        return child
    
    def append(self, *args):
        """
        Appends new content to the current section or item. 
        
        Example
        -------
        >>> from latexdocs import Document
        >>> doc = Document(title='Title', author='Author', date=True)
        >>> doc['Section 1'].append('Some regular text')
        
        """
        if len(args) > 0:
            args = list(map(self._adopt_child_, args))
        for a in args:
            return self._content.append(a)
    
    @abstractmethod
    def _append2doc_(self, doc, *args, **kwargs):
        """
        Override this to create a new document item type.
        
        """
        ...