# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['arcaflow_plugin_sdk']

package_data = \
{'': ['*']}

install_requires = \
['PyYAML>=5.4,<6.0', 'cbor2>=5.4.3,<6.0.0']

setup_kwargs = {
    'name': 'arcaflow-plugin-sdk',
    'version': '0.10.1',
    'description': 'Plugin SDK for Python for the Arcaflow workflow engine',
    'long_description': '# Python SDK for the Arcaflow workflow engine (WIP)\n\n## How this SDK works\n\nIn order to create an Arcaflow plugin, you must specify a **schema** for each step you want to support. This schema describes two things:\n\n1. What your input parameters are and what their type is\n2. What your output parameters are and what their type is\n\nNote, that you can specify **several possible outputs**, depending on what the outcome of your plugin execution is. You should, however, never raise exceptions that bubble outside your plugin. If you do, your plugin will crash and Arcaflow will not be able to retrieve the result data, including the error, from it.\n\nWith the schema, the plugin can run in the following modes:\n\n1. CLI mode, where a file with the data is loaded and the plugin is executed\n2. GRPC mode (under development) where the plugin works in conjunction with the Arcaflow Engine to enable more complex workflows\n\nFor a detailed description please see [the Arcalot website](https://arcalot.github.io/arcaflow/creating-plugins/python/).\n\n---\n\n## Requirements\n\nIn order to use this SDK you need at least Python 3.9.\n\n---\n\n## Run the example plugin\n\nIn order to run the [example plugin](example_plugin.py) run the following steps:\n\n1. Checkout this repository\n2. Create a `venv` in the current directory with `python3 -m venv $(pwd)/venv`\n3. Activate the `venv` by running `source venv/bin/activate`\n4. Run `pip install -r requirements.txt`\n5. Run `./example_plugin.py -f example.yaml`\n\nThis should result in the following placeholder result being printed:\n\n```yaml\noutput_id: success\noutput_data:\n  message: Hello, Arca Lot!\n```\n\n---\n\n## Generating a JSON schema file\n\nArcaflow plugins can generate their own JSON schema for both the input and the output schema. You can run the schema generation by calling:\n\n```\n./example_plugin.py --json-schema input\n./example_plugin.py --json-schema output\n```\n\nIf your plugin defines more than one step, you may need to pass the `--step` parameter.\n\n**Note:** The Arcaflow schema system supports a few features that cannot be represented in JSON schema. The generated schema is for editor integration only.\n\n\n## Generating documentation\n1. Checkout this repository\n2. Create a `venv` in the current directory with `python3 -m venv $(pwd)/venv`\n3. Activate the `venv` by running `source venv/bin/activate`\n4. Run `pip install -r requirements.txt`\n5. Run `pip install sphinx`\n6. Run `pip install sphinx-rtd-theme`\n7. Run `sphinx-apidoc -o docs/ -f -a -e src/ --doc-project "Python SDK for Arcaflow"`\n8. Run `make -C docs html`\n\n\n---\n\n## Developing your plugin\n\nWe have a detailed guide on developing Python plugins on [the Arcalot website](https://arcalot.github.io/arcaflow/creating-plugins/python/).',
    'author': 'Arcalot Contributors',
    'author_email': 'None',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'https://github.com/arcalot/arcaflow-plugin-sdk-python',
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.9,<4.0',
}


setup(**setup_kwargs)
