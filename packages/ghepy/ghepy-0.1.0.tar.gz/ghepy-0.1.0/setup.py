# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['ghepy', 'ghepy.model']

package_data = \
{'': ['*']}

install_requires = \
['coolprop>=6.4.3.post1,<7.0.0',
 'folium>=0.14.0,<0.15.0',
 'numpy>=1.24.2,<2.0.0',
 'plotly>=5.13.0,<6.0.0',
 'requests>=2.28.2,<3.0.0',
 'vincent>=0.4.4,<0.5.0']

setup_kwargs = {
    'name': 'ghepy',
    'version': '0.1.0',
    'description': '(Greenhouse energy-python) is a python tool for evaluation of heating demand in greenhouses when data are not provided elsewhere.',
    'long_description': '<div align="center"> <img src="https://github.com/mehran-hmdpr/GHEpy/blob/main/GHEpy.png" width="300" height="300" >\n\n<div align="left">\n\n# GHEpy\n**GHEpy** (Greenhouse energy-python) is a python tool for evaluation of heating demand in greenhouses when data are not provided elsewhere. \n\n## Table of contents\n* [Description](#description)\n     * [Problem definition](#problem-definition)\n     * [Problem solution](#problem-solution)\n\n* [Dependencies and installation](#dependencies-and-installation)\n\n* [Examples and Tutorials](#examples-and-tutorials)\n\n* [Authors and contributors](#authors-and-contributors)\n\n* [License](#license)\n\n## Description\n**GHEpy** is a Python-based model implemented for greenhouses according to the energy balance equations. This calculation is intended as a guide for estimation purposes.\n\n\n\n#### Problem definition\nTo estimate the heating demand of a greenhouse **GHEpy** needs parameters like location, dimantions, and inside minimum temperature. The required dimentions for the model are shown below:\n\n\n          \n#### Problem solution\n  \nThe energy balance of a greenhouse can be calculated by:\n\n$Q̇_g (t)= Q̇_{con}(t)+ Q̇_l(t)+ Q̇_{trans}(t)+Q̇_{vent}(t)-Q̇_s(t)$\n\nWhere:\n  - $Q ̇_g (t)$ is the required heating energy to maintain greenhouse conditions.\n  - $Q̇_{con}(t)$ is energy transfer by conduction and convection mechanisms.\n  - $Q̇_l(t)$ is the energy exchange due to long-wave and short-wave radiations.\n  - $Q̇_{trans}(t)$ is the energy flow rate caused by crop transpiration.\n  - $Q̇_{vent}(t)$ is the heat flow rate due to mass transfer for ventilation\n  - $Q̇_s(t)$ is the solar irradiation energy transfer. \n\n\n  \n## Dependencies and installation\n**GHEpy** requires `numpy`, `plotly`, `CoolProp`, `folium`, `vincent`. The code is tested for Python 3, while compatibility of Python 2 is not guaranteed anymore. It can be installed using `pip` or directly from the source code.\n\n### Installing via PIP\nTo install the package just type:\n```bash\n> pip install GHEpy\n```\nTo uninstall the package:\n```bash\n> pip uninstall GHEpy\n```\n## Examples and Tutorials\n\n**GHEpy** has three main functions that can help you with calculating heating demand of a greenhouse to use any of them you need to have climate data. To acquire data, you just need to take a token from [renewable ninja platform](https://www.renewables.ninja/documentation/api).\n- First function is `energymodel` which gives you energy demand of the greenhouse in 8760 hours of a year. To use this function just type:\n  ```bash\n    >\n    from ghepy import model\n    token = "@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@" # Token code that you should get from renewable ninja database\n    lat = 52.225121 # latitude\n    lon = 36.681990 # longitude\n    T_i = 18 # minimum inside temperature\n    h = 3 # dimension\n    L = 100 # dimension\n    d = 100 # dimension\n\n    heating_demand = model.greenhouse.energymodel(token, lat, lon, T_i, h, L, d, G= 2, U = 4)\n\n    ```\n- The second funciton is `visualization` which gives you a figure of temperatures and energy demands during a year. An example of the result of this function can be seen here:\n  ```bash\n    >\n      from ghepy import model\n      token = "@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@" # Token code that you should get from renewable ninja database\n      lat = 52.225121 # latitude\n      lon = 36.681990 # longitude\n      T_i = 18 # minimum inside temperature\n      h = 3 # dimension\n      L = 100 # dimension\n      d = 100 # dimension\n\n      fig = model.greenhouse.visualization(token, lat, lon, T_i, h, L, d, G= 2, U = 4)\n      fig.show()\n\n    ```\n  The result would be something like this:\n  \n  \n  <div align="center"> <img src="https://github.com/mehran-hmdpr/GHEpy/blob/main/Visualization%20(2).png" width="600" height="400" >\n  <div align="left">\n  \n - The last function is `CDFmap` which shows the location of greenhouse and cumulative distribution of greenhouse heating demand. This can help you realize how long your greenhouse needs heating or cooing during a year.\n   ```bash\n    >\n      from ghepy import model\n      token = "aa643a1899ea2156807425008360759c4853484d" # Token code that you should get from renewable ninja database\n      lat = 52.225121 # latitude\n      lon = 36.681990 # longitude\n      T_i = 18 # minimum inside temperature\n      h = 3 # dimension\n      L = 100 # dimension\n      d = 100 # dimension\n\n      map = model.greenhouse.CDFmap(token, lat, lon, T_i, h, L, d, G= 2, U = 4)\n      map\n\n    ```\n    The result would be something like this:\n    <div align="center"> <img src="https://github.com/mehran-hmdpr/GHEpy/blob/main/CDF.png" width="900" height="506" >\n    <div align="left">\n    \n\n\n## Authors and contributors\n**GHEpy** is developed and mantained by\n* [Mehran Ahmadpour](mailto:mehran.hmdpr@gmail.com)\n\nunder the supervision of Prof. Ramin Roshandel.\n\nContact us by email for further information or questions about **GHEpy**, or suggest pull requests. Contributions improving either the code or the documentation are welcome!\nYou can find out more about my projects by visiting my [website](https://mehranahmadpour.mozellosite.com/).\n## License\n\nSee the [LICENSE](https://github.com/mehran-hmdpr/orcpy/blob/main/LICENSE) file for license rights and limitations (MIT).\n\n   \n',
    'author': 'Mehran Ahmadpour',
    'author_email': 'mehran.hmdpr@gmail.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
