[![CircleCI](https://circleci.com/gh/dewloosh/latexdocs.svg?style=shield)](https://circleci.com/gh/dewloosh/latexdocs) 
[![Documentation Status](https://readthedocs.org/projects/latexdocs/badge/?version=latest)](https://latexdocs.readthedocs.io/en/latest/?badge=latest) 
[![License](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![PyPI](https://badge.fury.io/py/latexdocs.svg)](https://pypi.org/project/latexdocs) 

# **latexdocs** - A document generation solution for LaTeX

latexdocs is a Python library with the goal of making the generation of LaTeX documents as easy as possible. It builds on [PyLaTeX](https://github.com/JelteF/PyLaTeX), but offers a different approach to structuring your document or writing custom extensions.

## **Documentation**

Click [here](https://latexdocs.readthedocs.io/en/latest/) to read the documentation.

## **Installation**
This is optional, but we suggest you to create a dedicated virtual enviroment at all times to avoid conflicts with your other projects. Create a folder, open a command shell in that folder and use the following command

```console
>>> python -m venv venv_name
```

Once the enviroment is created, activate it via typing

```console
>>> .\venv_name\Scripts\activate
```

`latexdocs` can be installed (either in a virtual enviroment or globally) from PyPI using `pip` on Python >= 3.7:

```console
>>> pip install latexdocs
```

Installing latex on different operating systems is well described [here](https://latex-tutorial.com/installation/).

## **Basic Example**

The equivalent of the [example](https://jeltef.github.io/PyLaTeX/current/examples/full.html) provided by the folks at `PyLaTeX` would be the following:

```python
from latexdocs import Document, TikZFigure, Image
from pylatex import Alignat, Matrix, Math, Tabular, Plot
from pylatex.utils import italic
import numpy as np

image_filename = 'image.png'

doc = Document(title='Basic Example', author='PyLaTeX', date=True)

doc['Some basic content'].append('Some regular text and some')
doc['Some basic content'].append(italic('italic text. '))
doc['Some basic content'].append('\nAlso some crazy characters: $&#{}')
doc['Some basic content', 'Math that is incorrect'].append((Math(data=['2*3', '=', 9])))

a = np.array([[100, 10, 20]]).T
M = np.matrix([[2, 3, 4],
                [0, 0, 1],
                [0, 0, 2]])
                                                        
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
doc['Another section']['Beautiful graphs'].append(fig)

img = Image(filename=image_filename, position='h!', 
            caption='A simple structure.', width='350px')
doc['Another section']['An image'].append(img)

# doc.build() returns a pylatex.Document instance
doc.build().generate_pdf('basic_example', compiler='pdflatex')
```

## **Contributing**

Since latexdocs builds on PyLaTeX, we suggest you to contribute to that package and enjoy the result here.

## **Testing**

To run all tests, open up a console in the root directory of the project and type the following (requires the `unittest` library to be installed)

```console
>>> python -m unittest
```

## **License**

Copyright 2022 Bence Balogh, under [the MIT license](https://github.com/dewloosh/latexdocs/blob/master/LICENSE).
