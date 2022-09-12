# -*- coding: utf-8 -*-
import unittest
import numpy as np
from pylatex import Tabular, Math, Plot, Matrix, Alignat, NewLine, Tabularx, NoEscape
from pylatex.utils import italic
from latexdocs import Document, TikZFigure, Image
from latexdocs import Table, TableX
from texttable import Texttable
import latextable
import os


class TestTables(unittest.TestCase):
    
    def test_pdflatex(self):

        doc = Document()
        
        table = Tabular('rc|cl')
        table.add_hline()
        table.add_row((1, 2, 3, 4))
        table.add_hline(1, 2)
        table.add_empty_row()
        table.add_row((4, 5, 6, 7))
        doc.append(table)
        doc.append(NewLine())

        table = Tabularx('X|X|X|X')
        table.add_hline()
        table.add_row((1, 2, 3, 4))
        table.add_hline(1, 2)
        table.add_empty_row()
        table.add_row((4, 5, 6, 7))
        doc.append(table)
        doc.append(NewLine())

        # %% [markdown]
        # Tables using `texttable` and `latextable`

        table_1 = Texttable()
        table_1.set_cols_align(["l", "r", "c"])
        table_1.set_cols_valign(["t", "m", "b"])
        table_1.add_rows([["Name", "Age", "Nickname"],
                        ["Mr\nXavier\nHuon", 32, "Xav'"],
                        ["Mr\nBaptiste\nClement", 1, "Baby"],
                        ["Mme\nLouise\nBourgeau", 28, "Lou\n \nLoue"]])
        print('-- Example 1: Basic --')
        print('Texttable Output:')
        print(table_1.draw())
        print('\nLatextable Output:')
        content = latextable.draw_latex(table_1, caption="An example table.",
                                        label="table:example_table")
        print(content)
        doc.append(NoEscape(content))

        # %% [markdown]
        # Tables using `latexdocs`

        labels = ['A', 'B', 'C', 'D']
        data = np.array([[1, 2, 3, 4], [5, 6, 7, 8]])
        doc.append(Table(data=data, columns=labels, table_spec=r"c|c|c|c"))

        table = Table('c c c c', 'h!', caption="This is a table.",
                    label="table:tbl1")
        table.add_hline()
        table.add_row(('Case', "Method 1", "Method 2", "Method 3"))
        table.add_hline()
        table.add_hline()
        table.add_row((1, 50, 837, 970))
        table.add_row((2, 51, 838, 971))
        table.add_row((3, 52, 839, 972))
        table.add_row((4, 53, 840, 973))
        table.add_hline()
        doc.append(table)

        labels = ['A', 'B', 'C', 'D']
        data = np.array([[1, 2, 3, 4], [5, 6, 7, 8]])
        nD = data.shape[-1]
        table_spec = r"|".join(nD * [r">{\centering\arraybackslash}X",])
        doc.append(TableX(table_spec, 'h!', data=data, columns=labels))

        doc.build().generate_pdf('tables', compiler='pdflatex')
        
                            
if __name__ == "__main__":
    
    unittest.main()