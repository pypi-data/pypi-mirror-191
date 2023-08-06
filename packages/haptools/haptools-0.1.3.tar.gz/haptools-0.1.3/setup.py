# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['haptools', 'haptools.data']

package_data = \
{'': ['*']}

install_requires = \
['click>=8.0.3',
 'cyvcf2>=0.30.14',
 'matplotlib>=3.5.1',
 'numpy>=1.20.0',
 'pysam>=0.19.0']

extras_require = \
{'docs': ['Sphinx>=4.3.2',
          'sphinx-autodoc-typehints>=1.12.0',
          'sphinx-rtd-theme>=1.0.0',
          'numpydoc>=1.1.0',
          'sphinx-click>=3.0.2'],
 'files': ['Pgenlib>=0.81.3']}

entry_points = \
{'console_scripts': ['haptools = haptools.__main__:main']}

setup_kwargs = {
    'name': 'haptools',
    'version': '0.1.3',
    'description': 'Ancestry and haplotype aware simulation of genotypes and phenotypes for complex trait analysis',
    'long_description': '# haptools\n[![pypi version](https://img.shields.io/pypi/v/haptools)](https://pypi.org/project/haptools)\n[![image](https://anaconda.org/bioconda/haptools/badges/version.svg)](https://anaconda.org/bioconda/haptools)\n[![license](https://img.shields.io/pypi/l/haptools)](LICENSE)\n![status](https://github.com/CAST-genomics/haptools/workflows/Tests/badge.svg)\n\nHaptools is a collection of tools for simulating and analyzing genotypes and phenotypes while taking into account haplotype information. Haptools supports fast simulation of admixed genomes (with `simgenotype`), visualization of admixture tracks (with `karyogram`), simulating haplotype- and local ancestry-specific phenotype effects (with `transform` and `simphenotype`), and computing a variety of common file operations and statistics in a haplotype-aware manner.\n\nHomepage: [https://haptools.readthedocs.io/](https://haptools.readthedocs.io/)\n\nVisit our homepage for installation and usage instructions.\n\n![haptools commands](https://drive.google.com/uc?id=1c0i_Hjms7579s24zRsKp5yMs7BxNHed_)\n',
    'author': 'Arya Massarat',
    'author_email': 'None',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'https://github.com/cast-genomics/haptools',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'extras_require': extras_require,
    'entry_points': entry_points,
    'python_requires': '>=3.7,<3.11',
}


setup(**setup_kwargs)
