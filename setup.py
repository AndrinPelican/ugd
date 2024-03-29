from setuptools import setup, find_packages, Extension
import os


modulelist = []
for path, subdirs, files in os.walk('./ugd'):
    for name in files:
          modulelist.append(os.path.join(path, name))

try:
    with open("readme.md", "r") as fh:
        long_description = fh.read()
except:
    long_description = 'Drawing graphs uniformly at random subject to partition constraints (Partition Adjacency Matrix). Used for network testing.'


setup(name='ugd',
      version='0.6.5',
      description='Drawing graphs uniformly at random subject to partition constraints (Partition Adjacency Matrix). Used for network testing.',
      long_description_content_type='text/markdown',
      long_description=long_description,
    classifiers=[
        "Programming Language :: Python :: 3",
    ],
    install_requires=[
          'numpy',
          'matplotlib',
          'statsmodels',
          'pandas'
      ],
      author='Andrin Pelican',
      author_email='pelicanandrin@gmail.com',
      packages=find_packages()
     )
