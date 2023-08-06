# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['labelme2yolov7segmentation']

package_data = \
{'': ['*']}

install_requires = \
['albumentations>=1.3.0,<2.0.0', 'click', 'numpy', 'pydantic', 'pyyaml']

entry_points = \
{'console_scripts': ['labelme2yolo = labelme2yolov7segmentation.__main__:main']}

setup_kwargs = {
    'name': 'labelme2yolov7segmentation',
    'version': '2.0.2',
    'description': '',
    'long_description': '# LabelMe2Yolov7Segmentation\n\nThis repository was designed in order to label images using [LabelMe](https://github.com/wkentaro/labelme) and transform to [YoloV7](https://github.com/WongKinYiu/yolov7) format for instance segmentation\n\n## Instalation\n\n`pip install labelme2yolov7segmentation`\n\n## Usage\n\nFirst of all, make your dataset with LabelMe, after that call to the following command\n\n`labelme2yolo --source-path /labelme/dataset --output-path /another/path`\n\nThe arguments are:\n\n* `--source-path`: That indicates the path where are the json output of LabelMe and their images, both will have been in the same folder\n* `--output-path`: The path where you will save the converted files and a copy of the images following the yolov7 folder estructure\n\n### Expected output\n\nIf you execute the following command:\n\n`labelme2yolo --source-path /labelme/dataset --output-path /another/datasets`\n\nYou will get something like this\n\n```bash\ndatasets\n├── images\n│   ├── train\n│   │   ├── img_1.jpg\n│   │   ├── img_2.jpg\n│   │   ├── img_3.jpg\n│   │   ├── img_4.jpg\n│   │   └── img_5.jpg\n│   └── val\n│       ├── img_6.jpg\n│       └── img_7.jpg\n├── labels\n│   ├── train\n│   │   ├── img_1.txt\n│   │   ├── img_2.txt\n│   │   ├── img_3.txt\n│   │   ├── img_4.txt\n│   │   └── img_5.txt\n│   └── val\n│       ├── img_6.txt\n│       └── img_7.txt\n├── labels.txt\n├── test.txt\n└── train.txt\n```\n\n## Donation\n\nIf you want to contribute you can make a donation at https://www.buymeacoffee.com/tlaloc, thanks in advance\n',
    'author': 'Tlaloc-Es',
    'author_email': 'dev@tlaloc-es.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'https://github.com/Tlaloc-Es/labelme2yolov7segmentation',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.10,<4.0',
}


setup(**setup_kwargs)
