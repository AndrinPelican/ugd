from setuptools import setup, find_packages
import os


modulelist = []
for path, subdirs, files in os.walk('./ugd'):
    for name in files:
          modulelist.append(os.path.join(path, name))

with open("readme.md", "r") as fh:
    long_description = fh.read()


setup(name='ugd',
      version='0.4.0',
      description='Drawing uniformly graphs under partition constraints (Partition Adjacency Matrix). Commonly used for network testing.',
      long_description=long_description,
      long_description_content_type='text/markdown',
    classifiers=[
        "Programming Language :: Python :: 3",
    ],
    install_requires=[
          'numpy',
          'matplotlib'
      ],
      author='Andrin Pelican',
      author_email='andrin.pelican@student.unisg.ch',
      packages=find_packages()
     )
