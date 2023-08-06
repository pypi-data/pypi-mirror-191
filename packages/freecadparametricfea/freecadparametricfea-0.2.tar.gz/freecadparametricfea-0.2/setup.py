# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['freecadparametricfea']

package_data = \
{'': ['*']}

install_requires = \
['numpy>=1.24.1,<2.0.0',
 'pandas>=1.5.2,<2.0.0',
 'plotly>=5.12.0,<6.0.0',
 'pyside2>=5.15.2.1,<6.0.0.0',
 'tqdm>=4.64.1,<5.0.0']

setup_kwargs = {
    'name': 'freecadparametricfea',
    'version': '0.2',
    'description': 'A flexible parametric FEA library based on FreeCAD',
    'long_description': '# freecadparametricfea\n\n A flexible parametric FEA library based on [FreeCAD](https://www.freecadweb.org/), currently supporting FreeCAD 0.20. \n \n If you have 20 minutes I recommend the video tutorial on the [@engineeringmaths Youtube channel](https://www.youtube.com/watch?v=cwtgB4KpdJo).\n\n> **Warning**\n> this project is very early release, and should not be used for any serious structural analysis. It is aimed at hobbyists and makers\n\n## Quickest start\nCreate a Python 3.8 virtual environment:\n\n`pipenv --python 3.8`\n\nInstall the latest version from pypi:\n\n`pipenv install freecadparametricfea`\n\nthen run any of the examples inside [the examples folder](examples/)\n\n## Quick start\n\nCreate a FreeCAD part and assign names to the constraints that you want to change. You need to set up a FEA analysis as well, I have tested this using CalculiX and GMsh .\n\nThen in a script, or on the command line, run:\n\n```python\nfrom FreecadParametricFEA import parametric as pfea\nimport numpy as np\n# you need to manually specify the path to FreeCAD on your system, for now:\nFREECAD_PATH = "C:/Program Files/FreeCAD 0.20/bin"\n\n# initialise a parametric FEA object\nfea = pfea(freecad_path=FREECAD_PATH)\n\n# load the FreeCAD model\nfea.set_model("your-part-here.fcstd")\n\n# list the parameters to sweep:\nfea.set_variables(\n    [\n        {\n            "object_name": "CutsSketch", # the object where to find the constraint\n            "constraint_name": "NotchDistance", # the constraint name that you assigned \n            "constraint_values": np.linspace(10, 30, 5), # the values you want to check\n        },\n        {\n            "object_name": "CutsSketch",\n            "constraint_name": "NotchDiam",\n            "constraint_values": np.linspace(5, 9, 5),\n        },\n    ]\n)\n\n# setup the FEA analysis - we need to know the CalculiX results object and the solver name\nfea.setup_fea(fea_results_name="CCX_Results", solver_name="SolverCcxTools")\n\n# run and save the results (will return a Pandas DataFrame)\nresults = fea.run_parametric()\n\n# plot the results\nfea.plot_fea_results()\n```\n\n## Feeling fancy\n\n### Custom outputs\nThe default is to export the max Von Mises stress and max displacement values. You can also specify your own values and data reduction function like this:\n\n```python\nfea.set_outputs([\n        {\n            "output_var": "vonMises",\n            "reduction_fun": np.median,\n        },\n        {\n            "output_var": "vonMises",\n            "reduction_fun": lambda v: np.percentile(v, 95),\n            "column_label": "95th percentile"\n        }\n    ])\n```\n\n### Exporting data\n\nYou can export individual ParaView files using:\n\n```python\nresults = fea.run_parametric(export_results=True, output_folder="path/to/my/results")\n```\n\n\nOr just save the results dataframe in a .csv:\n\n```python\nfea.save_fea_results("results.csv")\n```\n\n... or even take a look at the parameters matrix before running any analysis:\n\n```python\nresults = fea.run_parametric(dry_run=True)\n```\n\n# Limitations and caveats\n\nAs of 0.1.2:\n * only netgen meshes are supported\n\n# Contributing\nI have created this for hobby and personal use, as I was interested in learning more about FreeCAD and writing Python modules. There are a lot of things that I would like to fix, if you want to get involved have a look at the [open issues](https://github.com/da-crivelli/freecad-parametric-fea/issues/) and send me a message if you have any questions.\n\n\n',
    'author': 'Davide Crivelli,',
    'author_email': 'da.crivelli@gmail.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'https://github.com/da-crivelli/freecad-parametric-fea',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8.10,<3.9.0',
}


setup(**setup_kwargs)
