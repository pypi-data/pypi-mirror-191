# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['eyepy', 'eyepy.core', 'eyepy.data', 'eyepy.io', 'eyepy.io.he']

package_data = \
{'': ['*']}

install_requires = \
['construct-typing>=0.5.5,<0.6.0',
 'imagecodecs>=2021.11.20,<2022.0.0',
 'matplotlib>=3.5.1,<4.0.0',
 'nptyping>=2.3.1,<3.0.0',
 'pandas>=1.5.3,<2.0.0',
 'scikit-image>=0.19.1,<0.20.0']

setup_kwargs = {
    'name': 'eyepie',
    'version': '0.7.0',
    'description': 'The Python package for working with ophthalmological data.',
    'long_description': '# eyepy\n\n[![Documentation](https://img.shields.io/badge/docs-eyepy-blue)](https://MedVisBonn.github.io/eyepy)\n[![PyPI version](https://badge.fury.io/py/eyepie.svg)](https://badge.fury.io/py/eyepie)\n[![DOI](https://zenodo.org/badge/292547201.svg)](https://zenodo.org/badge/latestdoi/292547201)\n\nThe `eyepy` python package provides a simple interface to import and process OCT volumes. Everything you import with one of our import functions becomes an `EyeVolume` object which provides a unified interface to the data. The `EyeVolume` object provides methods to plot the localizer image and B-scans as well as to compute and plot quantifications of voxel annotations such as drusen. Check out the [documentation](https://MedVisBonn.github.io/eyepy), especially the [Cookbook](https://medvisbonn.github.io/eyepy/cookbook/) chapter, for more information.\n\n## Features\n\n* Import HEYEY E2E, VOL and XML exports\n* Import B-Scans from a folder\n* Import public [AMD Dataset from Duke University](https://people.duke.edu/~sf59/RPEDC_Ophth_2013_dataset.htm)\n* Import data of the [RETOUCH Challenge](https://retouch.grand-challenge.org/).\n* Compute Drusen voxel annotation from BM and RPE layer segmentations\n* Quantify voxel annotations on a customizable circular grid\n* Plot annotated localizer\n* Plot annotated B-scans\n* Save and load EyeVolume objects\n\n## Getting Started\n\n### Installation\nTo install the latest version of eyepy run `pip install -U eyepie`. It is `eyepie` and not `eyepy` for installation with pip.\n\nWhen you don\'t hava a supported OCT volume at hand you can check out our sample dataset to get familiar with `eyepy`.\n```python\nimport eyepy as ep\n# Import HEYEX XML export\nev = ep.data.load("drusen_patient")\n```\n\n# Related Projects:\n\n+ [OCT-Converter](https://github.com/marksgraham/OCT-Converter): Extract raw optical coherence tomography (OCT) and fundus data from proprietary file formats. (.fds/.fda/.e2e/.img/.oct/.dcm)\n+ [eyelab](https://github.com/MedVisBonn/eyelab): A GUI for annotation of OCT data based on eyepy\n+ Projects by the [Translational Neuroimaging Laboratory](https://github.com/neurodial)\n  + [LibOctData](https://github.com/neurodial/LibOctData)\n  + [LibE2E](https://github.com/neurodial/LibE2E)\n  + [OCT-Marker](https://github.com/neurodial/OCT-Marker)\n+ [UOCTE](https://github.com/TSchlosser13/UOCTE) Unofficial continuation of https://bitbucket.org/uocte/uocte\n+ [OCTAnnotate](https://github.com/krzyk87/OCTAnnotate)\n+ [heyexReader](https://github.com/ayl/heyexReader)\n+ [OCTExplorer](https://www.iibi.uiowa.edu/oct-reference) Iowa Reference Algorithm\n',
    'author': 'Olivier Morelle',
    'author_email': 'oli4morelle@gmail.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'https://github.com/MedVisBonn/eyepy',
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8,<3.11',
}


setup(**setup_kwargs)
