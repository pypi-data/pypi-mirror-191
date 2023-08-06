# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['lug']

package_data = \
{'': ['*']}

install_requires = \
['cloudpickle>=2.2.0,<3.0.0',
 'docker>=6.0.0,<7.0.0',
 'importlib-metadata==4.13',
 'toolchest-client>=0.11.11,<0.12.0']

setup_kwargs = {
    'name': 'lug',
    'version': '0.3.5',
    'description': 'Run Python functions locally or in the cloud.',
    'long_description': '# Lug\n\n<p align="center">\n    <a href="https://pypi.python.org/pypi/lug/" alt="PyPI version">\n        <img alt="PyPI" src="https://img.shields.io/pypi/v/lug?labelColor=212121&color=304FFE"></a>\n    <a href="https://github.com/trytoolchest/lug/" alt="Build">\n        <img src="https://img.shields.io/circleci/build/gh/trytoolchest/lug/main?label=build&token=3eb013dde86ed79996a768ab325cd30ea3a1c993&labelColor=212121&color=304FFE" /></a>\n</p>\n\n**Lug** is an open source package that allows you to move the execution of specific Python functions to different \nenvironments on each call. This means that instead of deploying a function permanently to a specific environment \n(e.g. your local computer or a cloud-based server), you can choose where you want to run the function at the time of \nexecution. This flexibility allows you to optimize your resource consumption and cost for the needs of the specific \nfunction.\n\nLug is particularly useful for computational science, where researchers and scientists often have programs that are \nchallenging to install and run. Lug automatically detects and packages pip-installed dependencies and local modules, \nand you can even attach a sidecar Docker image for the command-line programs that need their own image – making it \nsimple to debug and scale your code.\n\nCheck out the full docs at [lug.dev](https://lug.dev)\n\n## Highlights\n\n- 📦 Automatic dependency detection and propagation\n- 🐳 Attach function-scoped sidecar Docker images\n- ☁️ Execute on your computer, the cloud, or on your own servers\n\n\n## Prerequisites\n\n- macOS or Linux\n- [Docker Engine](https://docs.docker.com/engine/install/), if you\'re using Lug Docker Sidecar functions\n\n## Install\n\n[Install Docker Engine and the CLI](https://docs.docker.com/engine/install/), if you don\'t have it.\n\n### With pip:\n\n`pip install lug`\n\n## Get started \n\nThere are two ways to use Lug:\n\n1. Creating a Lug Hybrid function that executes on your computer or in the cloud.\n2. Creating a Lug Docker Sidecar function, which is the same as a Lug Hybrid function but with a function-scoped Docker \nimage.\n\nOn this readme, we\'ll just create a short Lug Hybrid function, but there\'s more detail in the [docs](https://lug.dev).\n\n### Quick start:\n\nLet\'s create a simple Python function that tells us how many CPUs our system has:\n\n```python\nimport lug\nimport multiprocessing\n\n@lug.hybrid(cloud=False)\ndef num_cpus():\n    return multiprocessing.cpu_count()\n\nprint(num_cpus())\n```\n\nThis function will execute locally and print the number of CPUs on the system. To run on the cloud, first [generate a \nToolchest API key](https://dash.trytoolchest.com/) and set `key` to your Toolchest API key and `cloud=True`:\n\n```python\nimport lug\nimport multiprocessing\n\n@lug.hybrid(cloud=True, key="YOUR_KEY_HERE")\ndef num_cpus():\n    return multiprocessing.cpu_count()\n\nprint(num_cpus())\n```\n\nThis function will execute on the cloud and print the number of CPUs on the cloud-based server.\n\nFor more detail, check out the docs at [lug.dev](https://lug.dev)\n\n## Open-source roadmap\n\n- [x] Run a Python function in a local container\n- [x] Maintain Python major.version in function and in container\n- [x] Serialize and deserialize Python function and Python dependencies\n- [x] `os.system()`, `subprocess.run()`, and `subprocess.Popen()` redirect to a user-specified container\n- [x] Local files passed to as input go to `./input/` in remote Docker container\n- [x] Remote files written to `./output/` in the container are written to local output Path\n- [x] Runs locally\n- [x] Run in the cloud with [Toolchest](https://github.com/trytoolchest/toolchest-client-python)\n- [x] Stream live `stdout` during remote cloud execution\n- [x] `pip`-based environment propagation\n- [ ] `conda`-based environment propagation (help needed)\n\n## License\n\nLug is licensed under the Apache License 2.0',
    'author': 'Justin Herr',
    'author_email': 'justin@trytoolchest.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'https://lug.dev',
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8,<3.12',
}


setup(**setup_kwargs)
