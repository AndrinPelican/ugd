# How to upload a new version to pypi

See: 
- https://www.youtube.com/watch?v=QgZ7qv4Cd0Y
- https://packaging.python.org/tutorials/packaging-projects/

Do: 
- source a virtual environment with setuptools
- delete all the folders in the dist/ directory
- *run:* python3 setup.py sdist bdist_wheel
- *run:* twine upload dist/*

When looking at changes use:

- pip install --no-cache-dir  ugd

to install it, otherwise it uses a cached version

Sometimes markdown not rendered by PyPi

## Todo

* fix: through error if controlled or testvariable requres the vardict, but it is not probided


* output
    * think about how to test integer stat sequence for independence...

### after github repository


For an illustration more extensive use cases, see the examples scripts in:

- www.github/mcd.com .... 
