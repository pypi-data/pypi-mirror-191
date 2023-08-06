dls-mainiac
=======================================================================

Convenient Python helper classes for cli Main programs.

Intended advantages:

- consistent command line
- consistent logging

Installation
-----------------------------------------------------------------------
::

    pip install git+https://gitlab.diamond.ac.uk/kbp43231/dls-mainiac.git 

    dls-mainiac --version

Summary
-------------------------------------------------

TBD
    

Documentation
-----------------------------------------------------------------------

See https://www.cs.diamond.ac.uk/dls-mainiac for more detailed documentation.

Building and viewing the documents locally::

    git clone git+https://gitlab.diamond.ac.uk/kbp43231/dls-mainiac.git 
    cd dls-mainiac
    virtualenv /scratch/$USER/venv/dls-mainiac
    source /scratch/$USER/venv/dls-mainiac/bin/activate 
    pip install -e .[dev]
    make -f .dls-mainiac/Makefile validate_docs
    browse to file:///scratch/$USER/venvs/dls-mainiac/build/html/index.html

Topics for further documentation:

- TODO list of improvements
- change log


..
    Anything below this line is used when viewing README.rst and will be replaced
    when included in index.rst

