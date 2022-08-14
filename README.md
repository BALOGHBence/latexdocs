[![Binder](https://mybinder.org/badge_logo.svg)](https://mybinder.org/v2/gh/dewloosh/latexdocs/main?labpath=examples%2Flpp.ipynb?urlpath=lab)
[![CircleCI](https://circleci.com/gh/dewloosh/latexdocs.svg?style=shield)](https://circleci.com/gh/dewloosh/latexdocs) 
[![Documentation Status](https://readthedocs.org/projects/latexdocs/badge/?version=latest)](https://latexdocs.readthedocs.io/en/latest/?badge=latest) 
[![License](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![PyPI](https://badge.fury.io/py/latexdocs.svg)](https://pypi.org/project/latexdocs) 

# **latexdocs** - A document generation solution for LaTeX

> **Warning**
> This package is under active development and in an **alpha stage**. Come back later, or star the repo to make sure you don’t miss the first stable release!

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

`latexdocs` can be installed (either in a virtual enviroment or globally) from PyPI using `pip` on Python >= 3.6:

```console
>>> pip install latexdocs
```

## **Basic Example**

```python
from latexdocs import Document, TikZFigure, Image

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
doc['Another section']['Beautiful graphs'].append(fig)

img = Image(filename=image_filename, position='h!', 
            caption='A simple structure.', width='350px')
doc['Another section']['An image'].append(img)


doc.build().generate_pdf('basic_example_latexdocs', clean_tex=False, compiler='pdfLaTeX')
```


## **Testing**

To run all tests, open up a console in the root directory of the project and type the following

```console
>>> python -m unittest
```

## **Dependencies**

`pylatex`, `lightdeepdict`

## **License**

This package is licensed under the MIT license.