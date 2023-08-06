from setuptools import setup, Extension, find_packages
import codecs
import os

here = os.path.abspath(os.path.dirname(__file__))

with codecs.open(os.path.join(here, "README_uuRest.md"), encoding="utf-8") as fh:
    LONG_DESCRIPTION = "\n" + fh.read()

VERSION = '0.0.4'
DESCRIPTION = 'Unicorn Universe REST API (Unicorn Systems & Unicorn Application Framework)'
LONG_DESCRIPTION = LONG_DESCRIPTION.replace(f'\r', '')

# Setting up
setup(
    name="uuRest",
    version=VERSION,
    author="jaromirsivic (Jaromir Sivic)",
    author_email="<email@email.com>",
    long_description_content_type="text/markdown",
    description=DESCRIPTION,
    long_description=LONG_DESCRIPTION,
    packages=find_packages(),
    install_requires=['json'],
    keywords=['python', 'uuRest', 'Unicorn Systems', 'UAF', 'Unicorn Application Framework'],
    classifiers=[
        "Development Status :: 1 - Planning",
        "Intended Audience :: Developers",
        "Programming Language :: Python :: 3",
        "Operating System :: Unix",
        "Operating System :: MacOS :: MacOS X",
        "Operating System :: Microsoft :: Windows",
    ]
)
