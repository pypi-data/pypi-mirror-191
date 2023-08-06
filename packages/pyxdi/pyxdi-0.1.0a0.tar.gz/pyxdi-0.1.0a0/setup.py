# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': '.'}

packages = \
['pyxdi']

package_data = \
{'': ['*']}

install_requires = \
['anyio[asyncio]>=3.6.2,<4.0.0',
 'mkdocs-material[docs]>=9.0.12,<10.0.0',
 'mkdocs[docs]>=1.4.2,<2.0.0']

setup_kwargs = {
    'name': 'pyxdi',
    'version': '0.1.0a0',
    'description': 'Dependence Injection library',
    'long_description': '# Pyxdi (in dev)\n\n`Pyxdi` is a modern, lightweight and async-friendly Python Dependency Injection library that leverages type annotations ([PEP 484](https://peps.python.org/pep-0484/))\nto effortlessly manage dependencies in your applications, inspired by the functionality of [pytest fixtures](https://docs.pytest.org/en/7.2.x/explanation/fixtures.html).\n\n[![CI](https://github.com/antonrh/pyxdi/actions/workflows/ci.yml/badge.svg)](https://github.com/antonrh/pyxdi/actions/workflows/ci.yml)\n[![codecov](https://codecov.io/gh/antonrh/pyxdi/branch/main/graph/badge.svg?token=67CLD19I0C)](https://codecov.io/gh/antonrh/pyxdi)\n[![Documentation Status](https://readthedocs.org/projects/pyxdi/badge/?version=latest)](https://pyxdi.readthedocs.io/en/latest/?badge=latest)\n[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)\n\n---\nDocumentation\n\nhttp://pyxdi.readthedocs.io/\n\n---\n\n## Installing\n\nInstall using `pip`:\n\n```bash\npip install pyxdi\n```\n\nor using `poetry`:\n\n```bash\npoetry add pyxdi\n```\n\n## Quick Example\n\n*app.py*\n\n```python\nimport pyxdi\n\npyxdi.init()\n\n\n@pyxdi.provider\ndef message() -> str:\n    return "Hello, world!"\n\n\n@pyxdi.inject\ndef say_hello(message: str = pyxdi.dep) -> None:\n    print(message)\n\n\nif __name__ == "__main__":\n    say_hello()\n```\n\n---\n\n## TODO\n* Unit tests\n* Autowiring\n* Documentation\n* Examples\n* Pypi package\n',
    'author': 'Anton Ruhlov',
    'author_email': 'antonruhlov@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/antonrh/pyxdi',
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.7,<3.12',
}


setup(**setup_kwargs)
