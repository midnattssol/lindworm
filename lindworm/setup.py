from setuptools import setup
import pathlib as p


setup(
    name='lindworm',
    version='0.1.0',
    description='Lindworm programming language compiler and standard library',
    url='https://github.com/midnattssol/lindworm',
    author='midnattssol',
    author_email='cd154a7e15@protonmail.com',
    license='BSD 2-clause',
    packages=['lindworm', 'sigurdlib', 'utils'],
    install_requires=[
        "numpy",
        "autopep8",
        "mako",
        "more_itertools",
        "regex"
    ],
    scripts=["bin/lindworm", "bin/sigurd"],
    # scripts=["bin/sigurd"],
    classifiers=[
        'Development Status :: 1 - Planning',
        'License :: OSI Approved :: BSD License',
        'Operating System :: POSIX :: Linux',
        'Programming Language :: Python :: 3',
    ],
    include_package_data=True
)
