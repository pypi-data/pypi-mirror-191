# This should be only one line. If it must be multi-line, indent the second
# line onwards to keep the PKG-INFO file format intact.
"""New sphinx theme for ZEIT ONLINE docs
"""

from setuptools import setup, find_packages
import os.path


def project_path(*names):
    return os.path.join(os.path.dirname(__file__), *names)


setup(
    name='zondocs_theme',
    version='1.0.3',

    install_requires=[
        'setuptools',
    ],

    entry_points={
        'sphinx.html_themes': [
            'zondocs_theme = zondocs_theme',
        ],
    },

    author='Nico Bruenjes <nico.bruenjes@zeit.de>',
    author_email='nico.bruenjes@zeit.de',
    license='MIT',
    url='https://github.com/zeitonline/zondocs_theme/',

    keywords='',
    classifiers="""\
License :: OSI Approved :: MIT License
Programming Language :: Python
Programming Language :: Python :: 2
Programming Language :: Python :: 3
Framework :: Sphinx
Framework :: Sphinx :: Theme
"""[:-1].split('\n'),
    description=__doc__.strip(),
    long_description='\n\n'.join(open(project_path(name)).read() for name in (
        'README.rst',
        'CHANGES.txt',
    )),

    packages=find_packages('src'),
    package_dir={'': 'src'},
    include_package_data=True,
    zip_safe=False,
)
