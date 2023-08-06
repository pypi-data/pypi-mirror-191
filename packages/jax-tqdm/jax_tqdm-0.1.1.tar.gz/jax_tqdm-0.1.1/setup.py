# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['jax_tqdm']

package_data = \
{'': ['*']}

install_requires = \
['jax>=0.3.5', 'tqdm>=4.64.1,<5.0.0']

setup_kwargs = {
    'name': 'jax-tqdm',
    'version': '0.1.1',
    'description': 'Tqdm progress bar for JAX scans and loops',
    'long_description': '# JAX-tqdm\n\nAdd a [tqdm](https://github.com/tqdm/tqdm) progress bar to your JAX scans and loops.\n\n## Installation\n\nInstall with pip:\n\n```bash\npip install jax-tqdm\n```\n\n## Example usage\n\n### in `jax.lax.scan`\n\n```python\nfrom jax_tqdm import scan_tqdm\nfrom jax import lax\nimport jax.numpy as jnp\n\nn = 10_000\n\n@scan_tqdm(n)\ndef step(carry, x):\n    return carry + 1, carry + 1\n\nlast_number, all_numbers = lax.scan(step, 0, jnp.arange(n))\n```\n\n### in `jax.lax.fori_loop`\n\n```python\nfrom jax_tqdm import loop_tqdm\nfrom jax import lax\n\nn = 10_000\n\n@loop_tqdm(n)\ndef step(i, val):\n    return val + 1\n\nlast_number = lax.fori_loop(0, n, step, 0)\n```\n\n### Print Rate\n\nBy default, the progress bar is updated 20 times over the course of the scan/loop\n(for performance purposes, see [below](#why-jax-tqdm)). This\nupdate rate can be manually controlled with the `print_rate` keyword argument. For\nexample:\n\n```python\nfrom jax_tqdm import scan_tqdm\nfrom jax import lax\nimport jax.numpy as jnp\n\nn = 10_000\n\n@scan_tqdm(n, print_rate=2)\ndef step(carry, x):\n    return carry + 1, carry + 1\n\nlast_number, all_numbers = lax.scan(step, 0, jnp.arange(n))\n```\n\nwill update every other step.\n\n## Why JAX-tqdm?\n\nJAX functions are [pure](https://jax.readthedocs.io/en/latest/notebooks/Common_Gotchas_in_JAX.html#pure-functions),\nso side effects such as printing progress when running scans and loops are not allowed.\nHowever, the [host_callback module](https://jax.readthedocs.io/en/latest/jax.experimental.host_callback.html)\nhas primitives for calling Python functions on the host from JAX code. This can be used\nto update a Python tqdm progress bar regularly during the computation. JAX-tqdm\nimplements this for JAX scans and loops and is used by simply adding a decorator to the\nbody of your update function.\n\nNote that as the tqdm progress bar is only updated 20 times during the scan or loop,\nthere is no performance penalty.\n\nThe code is explained in more detail in this [blog post](https://www.jeremiecoullon.com/2021/01/29/jax_progress_bar/).\n\n## Developers\n\nDependencies can be installed with [poetry](https://python-poetry.org/) by running\n\n```bash\npoetry install\n```\n\n### Pre-Commit Hooks\n\nPre commit hooks can be installed by running\n\n```bash\npre-commit install\n```\n\nPre-commit checks can then be run using\n\n```bash\ntask lint\n```\n\n### Tests\n\nTests can be run with\n\n```bash\ntask test\n```\n',
    'author': 'Jeremie Coullon',
    'author_email': 'jeremie.coullon@gmail.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'https://github.com/jeremiecoullon/jax-tqdm',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
