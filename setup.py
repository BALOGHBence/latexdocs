# -*- coding: utf-8 -*-
import codecs
import os.path
from setuptools import find_packages, setup


def read(rel_path):
    here = os.path.abspath(os.path.dirname(__file__))
    with codecs.open(os.path.join(here, rel_path), 'r') as fp:
        return fp.read()


def get_version(rel_path):
    for line in read(rel_path).splitlines():
        if line.startswith('__version__'):
            delim = '"' if '"' in line else "'"
            return line.split(delim)[1]
    else:
        raise RuntimeError("Unable to find version string.")
    
    
def get_description(rel_path):
    for line in read(rel_path).splitlines():
        if line.startswith('__description__'):
            delim = '"' if '"' in line else "'"
            return line.split(delim)[1]
    else:
        raise RuntimeError("Unable to find description string.")


with open("README.md", "r") as fh:
    long_description = fh.read()


with open('requirements.txt') as f:
    required = f.read().splitlines()


_init_path = "src/latexdocs/__init__.py"
_version = get_version(_init_path)
_description = get_description(_init_path)
_url = 'https://github.com/BALOGHBence/latexdocs'
_download_url = _url + '/archive/refs/tags/{}.zip'.format(_version)


setup(
	name="latexdocs",
    version=_version,                        
    author="Bence Balogh",
    author_email = 'benceeok@gmail.com',                   
    description=_description,
    long_description=long_description,   
    long_description_content_type="text/markdown",
	url = _url, 
    download_url = _download_url,
	packages=find_packages(where='src'),
	classifiers=[
        'Development Status :: 4 - Beta',     
        'License :: OSI Approved :: MIT License',   
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",   
        'Programming Language :: Python :: 3 :: Only',
		'Operating System :: OS Independent'
    ],                                      
    python_requires='>=3.7, <3.11',                             
    package_dir={'':'src'},     
    install_requires=required,
	zip_safe=False,
)


