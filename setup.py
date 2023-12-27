# Project Python 2048

# Python Modules
from setuptools import setup, find_packages

# Local Modules
from py2048.version import VERSION

DESCRIPTION = 'Python clone of 2048',
# LONG_DESCRIPTION = DESCRIPTION

# with open('README.md', 'r', encoding='utf-8') as readme:
#     LONG_DESCRIPTION = readme.read()

setup(
    name='Py2048',
    author='Michael Buckley',
    description=DESCRIPTION,
    # long_description=LONG_DESCRIPTION,
    # long_description_content_type = 'text/markdown',
    version=VERSION,
    packages=find_packages(),
    install_requires=[
        'pygame'
    ],
    keywords=['python','networking','network','mac','oui','ieee']
)