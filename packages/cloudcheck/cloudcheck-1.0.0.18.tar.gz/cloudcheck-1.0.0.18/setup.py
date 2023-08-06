# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['cloudcheck']

package_data = \
{'': ['*']}

install_requires = \
['requests-cache>=0.9.7,<0.10.0', 'requests>=2.28.2,<3.0.0']

entry_points = \
{'console_scripts': ['cloudcheck = cloudcheck.cloudcheck:main']}

setup_kwargs = {
    'name': 'cloudcheck',
    'version': '1.0.0.18',
    'description': 'Check whether an IP address belongs to a cloud provider',
    'long_description': '# CloudCheck\n\nA simple Python utility to check whether an IP address belongs to a cloud provider.\n\n`cloud_providers.json` contains up-to-date lists of CIDRs for each cloud provider (updated weekly via CI/CD).\n\n## Installation\n~~~bash\npip install cloudcheck\n~~~\n\n## Usage - CLI\n~~~bash\n$ cloudcheck 168.62.20.37\n168.62.20.37 belongs to Azure (168.62.0.0/19)\n~~~\n\n## Usage - Python\n~~~python\nimport cloudcheck\n\nprovider, subnet = cloudcheck.check("168.62.20.37")\nprint(provider) # "Azure"\nprint(subnet) # IPv4Network(\'168.62.0.0/19\')\n~~~\n\n## Supported cloud providers\n- Amazon ([source](https://ip-ranges.amazonaws.com/ip-ranges.json)) \n- Azure ([source](https://www.microsoft.com/en-us/download/confirmation.aspx?id=56519))\n- Google ([source](https://www.gstatic.com/ipranges/cloud.json))\n- Oracle Cloud ([source](https://docs.cloud.oracle.com/en-us/iaas/tools/public_ip_ranges.json))\n- DigitalOcean ([source](http://digitalocean.com/geo/google.csv))\n',
    'author': 'TheTechromancer',
    'author_email': 'None',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
