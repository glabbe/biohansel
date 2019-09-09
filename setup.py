#!/usr/bin/env python
# -*- coding: utf-8 -*-

from setuptools import setup, find_packages

from bio_hansel import __version__, program_name, program_desc

classifiers = """
Development Status :: 3 - Alpha
Environment :: Console
License :: OSI Approved :: Apache Software License
Intended Audience :: Science/Research
Topic :: Scientific/Engineering
Topic :: Scientific/Engineering :: Bio-Informatics
Programming Language :: Python :: 3.5
Programming Language :: Python :: 3.6
Programming Language :: Python :: Implementation :: CPython
Operating System :: POSIX :: Linux
""".strip().split('\n')

with open('README.rst') as readme_file:
    readme = readme_file.read()

setup(
    name=program_name,
    version=__version__,
    packages=find_packages(exclude=['tests']),
    url='https://github.com/phac-nml/{}'.format(program_name),
    license='Apache Software License 2.0',
    author='Peter Kruczkiewicz',
    author_email='peter.kruczkiewicz@gmail.com',
    description=program_desc,
    long_description=readme,
    keywords='Salmonella enterica Heidelberg Enteritidis SNP kmer subtyping Aho-Corasick',
    classifiers=classifiers,
    package_dir={program_name: program_name},
    package_data={program_name: ['data/*/*.fasta', 'data/*/*.tsv',]},
    install_requires=[
        'numpy>=1.12.1',
        'pandas>=0.20.1',
        'pyahocorasick>=1.1.6',
        'attrs',
    ],
    extras_require={
        'test': ['pytest>=3.0.7',],
    },
    entry_points={
        'console_scripts': [
            'hansel={}.main:main'.format(program_name),
        ],
    }
)
