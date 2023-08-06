# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['q2report', 'q2report.q2engine', 'q2report.q2printer']

package_data = \
{'': ['*']}

install_requires = \
['pillow>=9.4.0,<10.0.0']

setup_kwargs = {
    'name': 'q2report',
    'version': '0.1.19',
    'description': '',
    'long_description': '# The light Python report builder.\nConverts data into formatted text (**HTML**, **DOCX**, **XLSX**):\n```python\ndata = {\'data_source1\':[{\'col1\': \'value row1\', ....}, ...],\n        \'data_source2\':[{\'col_1\': \'valie_row1\', ....}, ...],\n        }\n```\nAvailable formatting (styling options):\n```json  \n"style": {\n    "font-family": "Arial",\n    "font-size": "10pt",\n    "font-weight": "normal",\n    "border-width": "0 0 0 0",\n    "padding": "0.05cm 0.05cm 0.05cm 0.05cm",\n    "text-align": "left",\n    "vertical-align": "top"\n  }\n\n```\n## Concept\nThe report definition consists of sections (Report, Pages, Columns, Rows, Cells).  \nEach section inherits style from previous and may override some styling options.  \n*see examples in folder **test_data***\n```python\nReport:  # contains basic style\n    Pages:  # page & margins sizes\n        Columns:  # columns widths - exact, % or autowidth\n            Rows:  # rows heights - auto, exact, min or max\n                   # can be linked to data and then have header, footer and grouping subsections\n                   # \n                Cells  # contains simple text and data links - {col1}\n                       # and aggregate functions - {sum:coll}\n                       # support html formatting with <b> <i> <u> <br>\n                       # cells may be merged (span)\n            Rows:\n                Cells\n            ....\n        Columns:\n            ....\n    Pages:\n        ....\n    ....\n```',
    'author': 'Andrei Puchko',
    'author_email': 'andrei.puchko@gmx.de',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
