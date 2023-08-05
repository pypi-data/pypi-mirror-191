# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['weather_update']

package_data = \
{'': ['*']}

install_requires = \
['requests>=2.28.2,<3.0.0']

setup_kwargs = {
    'name': 'weather-update',
    'version': '1.0.1',
    'description': '',
    'long_description': '# Weather Update Library\nA simple Python library to fetch the weather updates for a specified location.\n\n## Installation\n\nYou can install the library using pip:\n\n```bash\npip install weather-update\n```\n\n## Usage\n\nBefore you can use the library, you need to set your OpenWeatherMap API key. The library will prompt you to enter the API key the first time you run it. The API key will be stored in a configuration file for subsequent use.\n\nTo get the weather updates for a location, use the get_weather function:\n\n```python\nfrom weather_update.weather import get_weather\n\nweather = get_weather("London,UK")\nprint(f"Weather in London: {weather[\'weather\'][0][\'description\']}, {weather[\'main\'][\'temp\']}°C")\n```\n\n## API Reference\n\n* `get_weather(location: str) -> dict`\nGet the weather updates for the specified location.\n\n    Arguments\n\n    * `location`: str -- location for which the weather updates are needed\n\n    Returns\n\n    A dictionary containing the weather updates for the specified location.\n\n* `set_api_key()`\n\nSet the OpenWeatherMap API key in the configuration file. The library will prompt you to enter the API key if it has not been set already.',
    'author': 'Ashutosh Krishna',
    'author_email': 'ashutoshbritish@gmail.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.9,<4.0',
}


setup(**setup_kwargs)
