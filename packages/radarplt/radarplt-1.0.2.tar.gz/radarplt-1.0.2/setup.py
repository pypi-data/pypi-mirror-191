# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['radarplt']

package_data = \
{'': ['*']}

install_requires = \
['matplotlib>=3.6.3,<4.0.0', 'pandas>=1.4.4,<2.0.0']

setup_kwargs = {
    'name': 'radarplt',
    'version': '1.0.2',
    'description': '',
    'long_description': '# Radar plot\nThis package creates radar plots. It can generate typical radar plots and \nplot ranges of values.\n\n- [Data formatting](#data-formatting)\n- [Basic usage](#basic-usage)\n- [Chaning ranges](#changing-ranges)\n- [Chaning labels](#changing-labels)\n- [Plotting target ranges](#plotting-target-ranges)\n\n![example 0](https://raw.githubusercontent.com/jdkern11/radar_plot/main/images/example_0.png)\n\n## Data formatting\nData you want to plot must have a tidy format. For instance, if I wanted to plot\nthree properties (let\'s say prop1, prop2, and prop3 with values \n12, 3.5, and 42 respectively) then you should load a csv file into a pandas \ndataframe that has the following format:\n\n| property | value | item  |\n| -------- | ----- | ----- |\n| prop1    | 12.0  | item1 |\n| prop2    | 3.5   | item1 |\n| prop3    | 42    | item1 |\n\nIf you wanted to plot several items (e.g., item1, item2, and item3)\nwith different values for the properties, then format the data like this:\n\n| property | value | item  |\n| -------- | ----- | ----- |\n| prop1    | 12.0  | item1 |\n| prop2    | 3.5   | item1 |\n| prop3    | 42    | item1 |\n| prop1    | 14.0  | item2 |\n| prop2    | 4.0   | item2 |\n| prop3    | 36    | item2 |\n| prop1    | 15    | item3 |\n| prop2    | 2     | item3 |\n| prop3    | 40    | item3 |\n\n## Basic Usage\nFollowing [that formatting scheme](#data-formatting), you can plot the data as follows\n```Python\nimport pandas as pd\nimport matplotlib.pyplot as plt\nimport radarplt\n\n# see tables above\ndf = pd.read_csv(\'example_data.csv\')\nfig, ax = radarplt.plot(\n    df,\n    label_column="property",\n    value_column="value",\n    hue_column="item",\n)\nlegend = ax.legend(loc=(0.9, 0.95))\nplt.tight_layout()\nplt.show()\n```\nResulting in the following image\n![example 1 plotted](https://raw.githubusercontent.com/jdkern11/radar_plot/main/images/example_1.png)\n\nAdditional lines are plotted at the .25, .50, and .75 marks on the image. The value at the\n.25 and .75 line for each property is labeled and values increase/decrease linearly\nbetween these points. For instance, the 0.5 mark for property 2 would be 4, the 1 \nmark would be 6 and the 0 mark would be 2.\n\n### Changing Ranges \nLet\'s say you don\'t like that the prop2 ranges from 1 to 6. To change\nthese value ranges create a dictionary of the ranges you want for each property and \npass it to the function via the `value_ranges` parameter.\nFor instance: \n```Python\nimport pandas as pd\nimport matplotlib.pyplot as plt\nimport radarplt\n\nvalue_ranges = {\n  "prop1": [0, 20],\n  "prop2": [0, 5],\n  "prop3": [0, 50],\n}\n\n# see tables above\ndf = pd.read_csv(\'example_data.csv\')\nfig, ax = radarplt.plot(\n    df,\n    label_column="property",\n    value_column="value",\n    hue_column="item",\n    value_ranges=value_ranges,\n)\nlegend = ax.legend(loc=(0.9, 0.95))\nplt.tight_layout()\nplt.show()\n```\nResulting in the following image\n![example 2 plotted](https://raw.githubusercontent.com/jdkern11/radar_plot/main/images/example_2.png)\n\n### Changing labels\nIf you don\'t want the labels for the properties to be the property names, \nyou can change those as well with the `plot_labels` parameter.\n\n```Python\nimport pandas as pd\nimport matplotlib.pyplot as plt\nimport radarplt\n\nvalue_ranges = {\n  "prop1": [0, 20],\n  "prop2": [0, 5],\n  "prop3": [0, 50],\n}\n\nplot_labels = {\n  "prop1": "$\\sigma^{2}$",\n  "prop2": "Property 2 (seconds)",\n  "prop3": "p3"\n}\n\n# see tables above\ndf = pd.read_csv(\'example_data.csv\')\nfig, ax = radarplt.plot(\n    df,\n    label_column="property",\n    value_column="value",\n    hue_column="item",\n    value_ranges=value_ranges,\n    plot_labels=plot_labels,\n)\nlegend = ax.legend(loc=(0.9, 0.95))\nplt.tight_layout()\nplt.show()\n```\nResulting in the following image\n![example 3 plotted](https://raw.githubusercontent.com/jdkern11/radar_plot/main/images/example_3.png)\n\n### Plotting target ranges\nIf you want to see if your items\' values fall within a certain range, you \ncan add those ranges as well\n```Python\nimport pandas as pd\nimport matplotlib.pyplot as plt\nimport radarplt\n\ntarget_ranges = {\n  "prop1": [10, 20],\n  "prop2": [0, 2],\n  "prop3": [25, 35]\n}\n\nvalue_ranges = {\n  "prop1": [0, 20],\n  "prop2": [0, 5],\n  "prop3": [0, 50],\n}\n\nplot_labels = {\n  "prop1": "$\\sigma^{2}$",\n  "prop2": "Property 2 (seconds)",\n  "prop3": "p3"\n}\n\n# see tables above\ndf = pd.read_csv(\'example_data.csv\')\nfig, ax = radarplt.plot(\n    df,\n    label_column="property",\n    value_column="value",\n    hue_column="item",\n    value_ranges=value_ranges,\n    plot_labels=plot_labels,\n)\nlegend = ax.legend(loc=(0.9, 0.95))\nplt.tight_layout()\nplt.show()\n```\n\nResulting in the following image\n![example 4 plotted](https://raw.githubusercontent.com/jdkern11/radar_plot/main/images/example_4.png)\n',
    'author': 'jdkern11',
    'author_email': 'josephdanielkern@gmail.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'https://github.com/jdkern11/radar_plot.git',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.9,<3.11',
}


setup(**setup_kwargs)
