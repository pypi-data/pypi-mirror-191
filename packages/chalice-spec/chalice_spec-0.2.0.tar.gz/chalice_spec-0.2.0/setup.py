# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['chalice_spec']

package_data = \
{'': ['*']}

install_requires = \
['apispec>=5.2.2,<6.0.0']

setup_kwargs = {
    'name': 'chalice-spec',
    'version': '0.2.0',
    'description': 'Chalice x APISpec x Pydantic plug-ins',
    'long_description': '# chalice-spec\n\n[![Python package](https://github.com/TestBoxLab/chalice-spec/actions/workflows/test.yml/badge.svg)](https://github.com/TestBoxLab/chalice-spec/actions/workflows/test.yml)\n[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)\n\n**Chalice × APISpec × Pydantic plug-ins**\n\nCombines the power of Chalice, APISpec, and Pydantic to make AWS Chalice apps easily documented\n\n## Installation\n\nFirst, add chalice-spec:\n\n```shell\npoetry add chalice_spec\n```\n\nWe consider Chalice, APISpec, and Pydantic "peer dependencies." We only include them as dev\ndependencies in our codebase, and you may need to install them in yours if you haven\'t\nalready.\n\n```shell\npoetry add chalice apispec pydantic\n```\n\n## Setup\n\nFirst, instantiate your APISpec object with *both* the Pydantic and Chalice plug-ins, assuming\nyou need the functionality of each. While the Pydantic plugin can be used alone, you currently must use\nthe Pydantic plugin with the Chalice plugin.\n\n```python\napp = Chalice(app_name="hello_world")\nspec = APISpec(chalice_app=app,\n               ...,\n               plugins=[PydanticPlugin(), ChalicePlugin()])\n```\n\nIf you use:\n```python\nChalicePlugin(generate_default_docs=True)\n```\nthe plugin will generate empty docs (with empty request and response schemas) for every endpoint that you\'ve defined in your app. This can be useful as a starting point / overview while developing.\n\n## Usage\n\nTo document your API, use your existing Pydantic models and add kwargs to Chalice decorators.\n\n**Before:**\n```python\n@app.route(\'/\', methods=["POST"])\ndef example():\n    body = MySchema.parse_obj(app.current_request.json_body)\n```\n\n**After:**\n```python\n@app.route(\'/\', methods=["POST"], docs=Docs(\n    post=Operation(request=MySchema)\n))\ndef example():\n    body = MySchema.parse_obj(app.current_request.json_body)\n```\n\nIf you have multiple methods supported, you may have something like:\n\n```python\n@app.route(\'/\', methods=["POST", "PUT"],\n           docs=Docs(\n               post=Operation(request=MyCreateSchema, response=MyReadSchema),\n               put=Operation(request=MyEditSchema, response=MyReadSchema)\n           )\ndef example():\n    # code goes here\n    pass\n```\n\n### API\n\n- [ ] TODO: this section coming soon!\n',
    'author': 'Jake Wood',
    'author_email': 'jake@testbox.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'https://github.com/TestBoxLab/chalice-spec',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
