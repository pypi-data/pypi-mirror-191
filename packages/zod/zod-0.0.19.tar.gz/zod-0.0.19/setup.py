# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['zod',
 'zod.anno',
 'zod.anno.tsr',
 'zod.cli',
 'zod.data_classes',
 'zod.eval',
 'zod.eval.detection',
 'zod.eval.detection.nuscenes_eval.common',
 'zod.eval.detection.nuscenes_eval.detection',
 'zod.utils',
 'zod.visualization']

package_data = \
{'': ['*'], 'zod.eval.detection': ['nuscenes_eval/*']}

install_requires = \
['dataclass-wizard>=0.22.2',
 'h5py>=3.1',
 'numpy-quaternion>=2022.4.2',
 'numpy>=1.19,<2.0',
 'pillow>=7',
 'pyquaternion>=0.9',
 'scipy>=1.5,<2.0',
 'tqdm>=4.60']

extras_require = \
{'all': ['typer[all]>=0.7.0',
         'dropbox>=11.36.0',
         'opencv-python>=4',
         'matplotlib>=3',
         'plotly>=5,<6',
         'pandas>=1.3,<2.0',
         'notebook>=5',
         'imageio>=2,<3'],
 'cli': ['typer[all]>=0.7.0', 'dropbox>=11.36.0']}

entry_points = \
{'console_scripts': ['zod = zod.cli.main:app']}

setup_kwargs = {
    'name': 'zod',
    'version': '0.0.19',
    'description': 'Zenseact Open Dataset',
    'long_description': '# Zenseact Open Dataset\nThe Zenseact Open Dataset (ZOD) is a large multi-modal autonomous driving dataset developed by a team of researchers at [Zenseact](https://zenseact.com/). The dataset is split into three categories: *Frames*, *Sequences*, and *Drives*. For more information about the dataset, please refer to our [coming soon](), or visit our [website](https://zod.zenseact.com).\n\n## Examples\nFind examples of how to use the dataset in the [examples](examples/) folder. Here you will find a set of jupyter notebooks that demonstrate how to use the dataset, as well as an example of how to train an object detection model using [Detectron2](https://github.com/facebookresearch/detectron2).\n\n## Installation\n\nTo intstall the library only, run:\n```bash\npip install zod\n```\n\nTo install the library, along with the CLI, run:\n```bash\npip install zod[cli]\n```\n\nTo install the full devkit, with all dependencies, run:\n```bash\npip install zod[all]\n```\n\n## Download using the CLI\n\nThis is an example of how to download the ZOD Frames mini-dataset using the CLI. Prerequisites are that you have applied for access and received a download link. To download the mini-dataset, run:\n```bash\nzod download --url <download-link> --output-dir <path/to/outputdir> frames --mini\n```\nsimilarly, to download the full dataset (including all lidar scans before and after the keyframe), run:\n```bash\nzod download --url <download-link> --output-dir <path/to/outputdir> frames --lidar --num-scans-before -1 --num-scans-after -1 --oxts --images --blur --dnat --calibrations --annotations\n```\nthis will download all the previous and future lidar scans (as `num-scans-before=-1` and `num-scans-after=-1`), the OxTS data, the images (with both the blur and DNAT anonymization), the calibration files, the annotations, and all other necessary files. If you dont want any previous or future lidar scans, run:\n```bash\nzod download --url <download-link> --output-dir <path/to/outputdir> frames --lidar --num-scans-before 0 --num-scans-after 0 --oxts --images --blur --dnat --calibrations --annotations\n```\n\nFor a full list of options for ZOD download, run:\n```bash\nzod download frames --help\nzod download sequences --help\n```\ndepending on which dataset you want to download.\n\n\n## Anonymization\nTo preserve privacy, the dataset is anonymized. The anonymization is performed by [brighterAI](https://brighter.ai/), and we provide two separate modes of anonymization: deep fakes (DNAT) and blur. In our paper, we show that the performance of an object detector is not affected by the anonymization method. For more details regarding this experiment, please refer to our [coming soon]().\n\n## Citation\nIf you publish work that uses Zenseact Open Dataset, please cite: [coming soon]()\n\n```\n@misc{zod2021,\n  author = {TODO},\n  title = {Zenseact Open Dataset},\n  year = {2023},\n  publisher = {TODO},\n  journal = {TODO},\n```\n\n## Contact\nFor questions about the dataset, please [Contact Us](mailto:opendataset@zenseact.com).\n\n## Contributing\nWe welcome contributions to the development kit. If you would like to contribute, please open a pull request.\n\n## License\n**Dataset**:\nThis dataset is the property of Zenseact AB (© 2023 Zenseact AB) and is licensed under [CC BY-SA 4.0](https://creativecommons.org/licenses/by-sa/4.0/). Any public use, distribution, or display of this dataset must contain this notice in full:\n\n> For this dataset, Zenseact AB has taken all reasonable measures to remove all personally identifiable information, including faces and license plates. To the extent that you like to request the removal of specific images from the dataset, please contact [privacy@zenseact.com](mailto:privacy@zenseact.com).\n\n\n**Development kit**:\nThis development kit is the property of Zenseact AB (© 2023 Zenseact AB) and is licensed under [MIT](https://opensource.org/licenses/MIT).\n',
    'author': 'Zenseact',
    'author_email': 'opendataset@zenseact.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'https://zod.zenseact.com',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'extras_require': extras_require,
    'entry_points': entry_points,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
