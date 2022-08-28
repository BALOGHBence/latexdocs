# -*- coding: utf-8 -*-
import unittest
import numpy as np
from pylatex import Tabular, Math, Plot, Matrix, Alignat
from pylatex.utils import italic
from latexdocs import Document, TikZFigure, Image
import os


class TestMain(unittest.TestCase):
    
    def test_pdflatex(self):
        image_filename = '.\examples\image.png'
        
        a = np.array([[100, 10, 20]]).T
        M = np.array([[2, 3, 4],
                        [0, 0, 1],
                        [0, 0, 2]])

        doc = Document(title='Document Title', author='BB', date=True)

        doc['Some basic content'].append('Some regular text and some')
        doc['Some basic content'].append(italic('italic text. '))
        doc['Some basic content'].append('\nAlso some crazy characters: $&#{}')
        doc['Some basic content', 'Math that is incorrect'].append((Math(data=['2*3', '=', 9])))
                                                                
        content = Math(data=[Matrix(M), Matrix(a), '=', Matrix(M * a)])
        doc['Another section', 'Correct matrix equations'].append(content)

        table = Tabular('rc|cl')
        table.add_hline()
        table.add_row((1, 2, 3, 4))
        table.add_hline(1, 2)
        table.add_empty_row()
        table.add_row((4, 5, 6, 7))
        doc['Some basic content', 'Table of something'].append(table)
        
        agn = Alignat(numbering=False, escape=False)
        agn.append(r'\frac{a}{b} &= 0 \\')
        agn.extend([Matrix(M), Matrix(a), '&=', Matrix(M * a)])
        doc['Another section', 'Alignat math environment'].append(agn)

        fig = TikZFigure(plot_options='height=4cm, width=6cm, grid=major')
        fig.append(Plot(name='model', func='-x^5 - 242'))
        coordinates = [
            (-4.77778, 2027.60977),
            (-3.55556, 347.84069),
            (-2.33333, 22.58953),
            (-1.11111, -493.50066),
            (0.11111, 46.66082),
            (1.33333, -205.56286),
            (2.55556, -341.40638),
            (3.77778, -1169.24780),
            (5.00000, -3269.56775),
        ]
        fig.append(Plot(name='estimate', coordinates=coordinates))
        #doc['Another section']['Beautiful graphs']['figure:fig1'] = fig
        doc['Another section']['Beautiful graphs'].append(fig)

        img = Image(filename=image_filename, position='h!', 
                    caption='A simple structure.', width='350px')
        doc['Another section']['An image'].append(img)
        #doc['Another section']['An image']['image:img1'] = img

        doc.build().generate_pdf('basic_example', clean_tex=True, compiler='pdflatex')
        
                            
if __name__ == "__main__":
    
    unittest.main()