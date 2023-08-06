# Rudimentary soil model primarily for vertical stresses under level ground.
Define soil layers, assemble them into soil profile and compute total vertical stresses, pore pressures, and effective vertical stresses at specified locations beneath a level ground. In addition, return requested soil parameters at specified depths. One can use these parameters at specified depths to perform futher analysis. This is a work in progress.

## Documentation
[pyvstress documentation](https://pyvstress.readthedocs.io/en/latest/)


## References:
 - [Maxim Millen's eng-tools](https://github.com/eng-tools)
 - [Nico Schlömer and others pygmsh](https://github.com/nschloe/pygmsh)
 - [Albert Kottke's pysra](https://github.com/arkottke/pysra)
 - [note.nkmk.me](https://note.nkmk.me/en/python-pip-install-requirements/)

## Usage
Sorry for the lack of documentation. I am in the process of learning how to create documentation from python docstrings. I am a slow learner so I do not know when that will be ready. Once that is up, maybe I will include few examples in the documentation. Untill then please refer to the `tests` and the `examples` folders. 

## Requirements
There is a *requirements.txt* file which was generated using `pipreqs`. The version number may not be very important. Only Python and Numpy are required for the package:
 - python: the latest version, most probably 3.10, but version number may not be too important
 - numpy

If you have a `.venv` virtual environment, `pipreqs` returns a bunch of packages. In such cases use `--ignore .venv`.

```
pipreqs.pireqs ./ --ignore .venv
```
Use `--force` if *requirement.txt* already exists.

However, these additional packages are required to run the example files
 - pandas
 - matplotlib
 - altair
 - hancalcs

# Project folder
pyvstress <- This is the package root directory
├── build
├── dist
├── docs
├── examples
├── LICENSE.md
├── pyproject.toml
├── pyvstress
    ├── __about__.py
    ├── exceptions.py
    ├── __init__.py
    ├── __pycache__
    ├── soil.py
    └── utility_functions.py
├── pyvstress.egg-info
├── README.md
├── requirements.txt
└── tests


# Local installation in virtual environment
1. Make a `.venv` directory in the project folder.
2. Make a virtual environment `python -m venv .venv`
3. Activate the virtual environment `source .venv/bin/activate`
4. Install the requirements `python -m pip install -r requirements.txt`
5. Install the package locally `pip install -e .`

Above (4) and (5) are run after activating the virtual environment. This will install the package to the virtual environment. Any changes your make to the source code will be reflected in the package.

# Build system
Creater a `pyproject.toml` file. Refer to `Setuptools` [Quickstart Userguide](https://setuptools.pypa.io/en/latest/userguide/quickstart.html)

- Place a `pyproject.toml` in the root directory of the project. Check the file for this package in the project root directory.

- Install `setuptools` and `build` using `pip` in the virtual environment `.venv`.

- Run `python -m build` in the package root directory. This will create `.whl` and `.tar.gz` in the `/build` directory for distribution. 


## Upload to TestPyPI with twine
```
twine upload --repository testpypi dist/*
```

## Installation
```
$ pip install --index-url https://test.pypi.org/simple/ pygeotech
```

## Publishing
I will try to create the documentation using the docstrings with Sphinx and publish those in [Read the docs](https://readthedocs.org/).

1. Install `sphinx` and `sphinx-rtd-theme`, in the same environment in which you are building your package.

```
pip install sphinx
pip install sphinx-rtd-theme
```

2. Create `docs` directory in your package directory to hold the documentation files.
```mkdir docs```

3. Run `sphinx-quickstart` in the `docs` folder. Provide the information and when asked about creating a separate folder for build type `y`.

```cd docs
sphinx-quickstart
```
The `docs` folder will have
```
build
source
Makefile
make.bat
```
Within the `source` folder there will be two files:

```
conf.py
index.rst
```
4. Run the Sphinx API documentation command `sphinx-apidoc` to generate Sphinx source files.
```
sphinx-apidoc -o source/ ../pyvstress
```
5. Edit the `conf.py` file. 
    - a. Change the `html_theme` to the one of your liking, `html_theme = 'sphinx_rtd_theme`.
    - b. For autocode generattion from docstrings in the code, specifiy the directory of source code.
    ```
    import os
    import sys
    sys.path.insert(0, os.path.abspath('../../pysoil/'))
    ``` 
    - c. Also add some extensions
    ```
    extensions = ['sphinx.ext.todo', 'sphinx.ext.viewcode', 'sphinx.ext.autodoc']
    ```
6. Run `make htlm` build the `htlm` files in the `build/` directory.

7. Log into `ReadTheDocs` and click on `Import Project`. Fill out the fields. For the repository URL use `https://gitlab.com/geosharma/pyvstress.git`. This can be got from `CLONE -> Clone with HTPPS` URL.

8. Then in `Projects -> Admin -> Integration`, click on `Add Integration` and choose `GitLab incoming webhook`.

9. Then copy the URL starting with `readthedocs.org/api/v2/webhook/...../......` and paste it into GitLab Project `Settings -> Webhooks` 
References:
 - [Read the docs](https://readthedocs.org/)
 - [Sphinx-RTD-Tutorial](https://sphinx-rtd-tutorial.readthedocs.io/en/latest/index.html)
 - [A idiot's guide to Python documentation with Sphinx and ReadTheDocs](https://samnicholls.net/2016/06/15/how-to-sphinx-readthedocs/)
 - [Read the Docs VSC Integration](https://docs.readthedocs.io/en/stable/integrations.html#github)
 - [Deplyoing a Sphinx project online](https://www.sphinx-doc.org/en/master/tutorial/deploying.html)
 -[Making Readthedocs for a Python package](https://pennyhow.github.io/blog/making-readthedocs/)
 -[An introduction to Sphinx and Read the Docs for Technical Writers](https://www.ericholscher.com/blog/2016/jul/1/sphinx-and-rtd-for-writers/)