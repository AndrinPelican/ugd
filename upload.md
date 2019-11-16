# How to upload a new version to pypi

See: 
- https://www.youtube.com/watch?v=QgZ7qv4Cd0Y
- https://packaging.python.org/tutorials/packaging-projects/

Do: 
- source a virtual environment with setuptools  (there are some versions of the build and upload packages which cause problems)
- delete all the folders in the dist/ directory
- *run:* python3 setup.py sdist bdist_wheel
- *run:* twine upload dist/*

Username: Andrin

When looking at changes use:

- pip install --no-cache-dir  ugd

to install it, otherwise it uses a cached version

Sometimes markdown not rendered by PyPi



### after github repository


For an illustration more extensive use cases, see the examples scripts in:

- www.github/mcd.com .... 
