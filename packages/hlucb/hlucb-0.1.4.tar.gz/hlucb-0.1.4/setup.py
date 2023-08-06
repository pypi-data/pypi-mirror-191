# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['hlucb']

package_data = \
{'': ['*']}

install_requires = \
['numpy>=1.24.2,<2.0.0']

setup_kwargs = {
    'name': 'hlucb',
    'version': '0.1.4',
    'description': 'Hamming-LUCB algorithm implementation',
    'long_description': '# Hamming-LUCB\n\nThe `hlucb` package is a Python implementation of the paper [Approximate ranking from pairwise comparisons](http://proceedings.mlr.press/v84/heckel18a.html).\n\n> Heckel, R., Simchowitz, M., Ramchandran, K., & Wainwright, M. (2018, March). Approximate ranking from pairwise comparisons. In International Conference on Artificial Intelligence and Statistics (pp. 1057-1066). PMLR.\n\n## Installation\n\n`hlucb` is installable with pip:\n\n```bash\n$ pip install hlucb\n```\n\n## Usage\n\n### Ranking with a comparator\n\n```python\nfrom hlucb import HammingLUCB\n\nitems = [4, 1, 2, 6, 5, 8, 9, 3]\nk = 5\nh = 2\ndelta = 0.9\n\ndef compare(item_a: int, item_b: int) -> bool:\n    return item_a > item_b\n\nscores, bounds = HammingLUCB.from_comparator(items, k, h, delta, compare, seed=42)\n\nprint("Scores: ", scores)\nprint("Bounds: ", bounds)\n```\n\n### Ranking with a generator\n\n```python\nfrom hlucb import HammingLUCB\n\nitems = [4, 1, 2, 6, 5, 8, 9, 3]\nn = len(items)\nk = 5\nh = 2\ndelta = 0.9\n\ngenerator = HammingLUCB.get_generator(n, k, h, delta, seed=42)\nscores = None\nbounds = None\nfor (i, j), (scores, bounds) in generator:\n    comparison = items[i] > items[j]\n    generator.send(comparison)\n\nprint("Scores: ", scores)\nprint("Bounds: ", bounds)\n```\n\n## Intuition\n\nThe Hamming-LUCB algorithm approximately ranks $n$ items, estimates the score of each item, and provides confidence bounds for each score. The intuition behind the approximate ranking is that it\'s easier to compare items with very different scores, so it should be possible to separate high-scoring items from low-scoring items with few comparisons and high confidence even if the exact ranking is not discovered.\n\nThe sets of high- and low-scoring items are designated $S_1$ and $S_2$ respectively. Hamming-LUCB extracts $S_1$ and $S_2$ such that all items in $S_1$ are expected to have higher scores than all items in $S_2$.\n\nParameters:\n\n- $n$ - the total number of items\n- $k$ - the number of items to extract as high-scoring items\n- $h$ - half the margin between $S_1$ and $S_2$\n- $\\delta$ - confidence parameter for the probability of achieving $h$-Hamming accuracy\n\nDefinitions:\n\n- The Hamming distance between two sets: $D_H(S_1, S_2) = \\lvert (S_1 \\cup S_2) \\setminus (S_1 \\cap S_2) \\rvert$\n- A ranking $\\hat{S_1}$, $\\hat{S_2}$ is $h$-Hamming accurate if: $D_H(\\hat{S_l}, S_l) \\leq 2h$ for\n  - $\\lvert \\hat{S_l} \\rvert = \\lvert S_l \\rvert$\n  - $l \\in \\{1, 2\\}$\n- A ranking algorithm is $(h, \\delta)$-accurate if the ranking returned is $h$-Hamming accurate with probability at least $1 - \\delta$.\n',
    'author': 'Chris Gregory',
    'author_email': 'christopher.b.gregory@gmail.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'https://github.com/gregorybchris/hlucb',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8.1',
}


setup(**setup_kwargs)
