# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['olympipe', 'olympipe.pipes']

package_data = \
{'': ['*']}

setup_kwargs = {
    'name': 'olympipe',
    'version': '1.0.2',
    'description': 'A powerful parallel pipelining tool',
    'long_description': '# Olympipe\n\n![coverage](https://gitlab.com/gabraken/olympipe/badges/master/coverage.svg?job=tests)![status](https://gitlab.com/gabraken/olympipe/badges/master/pipeline.svg)\n\n![Olympipe](https://gitlab.com/gabraken/olympipe/-/raw/master/Olympipe.png)\n\n\nThis project will make pipelines \neasy to use to improve parallel computing using the basic multiprocessing module. This module uses type checking to ensure your data process validity from the start.\n\n## Basic usage\n\nEach pipeline starts from an interator as a source of packets (a list, tuple, or any complex iterator). This pipeline will then be extended by adding basic `.task(<function>)`. The pipeline process join the main process when using the `.wait_for_results()` or `.wait_for_completion()` functions.\n\n```python\n\nfrom olympipe import Pipeline\n\ndef times_2(x: int) -> int:\n    return x * 2\n\np = Pipeline(range(10))\n\np1 = p.task(times_2) # Multiply each packet by 2\n# or \np1 = p.task(lambda x: x * 2) # using a lambda function\n\nres = p1.wait_for_results()\n\nprint(res) # [0, 2, 4, 6, 8, 10, 12, 14, 16, 18]\n\n```\n\n\n## Filtering\n\nYou can choose which packets to `.filter(<keep_function>)` by passing them a function returning True or False when applied to this packet.\n\n```python\n\nfrom olympipe import Pipeline\n\np = Pipeline(range(20))\np1 = p.filter(lambda x: x % 2 == 0) # Keep pair numbers\np2 = p1.batch(2) # Group in arrays of 2 elements\n\nres = p2.wait_for_results()\n\nprint(res) # [[0, 2], [4, 6], [8, 10], [12, 14], [16, 18]]\n\n```\n\n## In line formalization\n\nYou can chain declarations to have a more readable pipeline.\n\n```python\n\nfrom olympipe import Pipeline\n\nres = Pipeline(range(20)).filter(lambda x: x % 2 == 0).batch(2).wait_for_results()\n\nprint(res) # [[0, 2], [4, 6], [8, 10], [12, 14], [16, 18]]\n\n```\n\n## Debugging\n\nInterpolate `.debug()` function anywhere in the pipe to print packets as they arrive in the pipe.\n\n```python\nfrom olympipe import Pipeline\n\np = Pipeline(range(20))\np1 = p.filter(lambda x: x % 2 == 0).debug() # Keep pair numbers\np2 = p1.batch(2).debug() # Group in arrays of 2 elements\n\np2.wait_for_completion()\n```\n\n## Pipeline forking\n\nFor the time being, you have to adapt the code a little bit if you wish to get several outputs for a same pipeline. [This section might be updated soon]\n\n```python\nfrom olympipe import Pipeline\n\np1 = Pipeline(range(10))\np2 = p1.filter(lambda x: x % 2 == 0)\np3 = p1.filter(lambda x: x % 2 == 1)\n\nq2 = p2.prepare_output_buffer()\nq3 = p3.prepare_output_buffer()\n\nres3 = p3.wait_for_results(q3)\nres2 = p2.wait_for_results(q2)\n\nprint(res3) # [1, 3, 5, 7, 9]\nprint(res2) # [0, 2, 4, 6, 8]\n\n```\n\n## Real time processing (for sound, video...)\n\nUse the `.temporal_batch(<seconds_float>)` pipe to aggregate packets received at this point each <seconds_float> seconds.\n\n```python\nimport time\nfrom olympipe import Pipeline\n\ndef delay(x: int) -> int:\n    time.sleep(0.1)\n    return x\n\np = Pipeline(range(20)).task(delay) # Wait 0.1 s for each queue element\np1 = p.filter(lambda x: x % 2 == 0) # Keep pair numbers\np2 = p1.temporal_batch(1.0) # Group in arrays of 2 elements\n\nres = p2.wait_for_results()\n\nprint(res) # [[0, 2, 4, 6, 8], [10, 12, 14, 16, 18], []]\n```\n\n## Using classes in a pipeline\n\nYou can add a stateful class instance to a pipeline. The method used will be typecheked as well to ensure data coherence. You just have to use the `.class_task(<Class>, <Class.method>, ...)` method where Class.method is the actual method you will use to process each packet.\n\n```python\nitem_count  = 5\n\nclass StockPile:\n    def __init__(self, mul:int):\n        self.mul = mul\n        self.last = 0\n        \n    def pile(self, num: int) -> int:\n        out = self.last\n        self.last = num * self.mul\n        return out\n        \n\np1 = Pipeline(range(item_count))\n\np2 = p1.class_task(StockPile, StockPile.pile, [3])\n\nres = p2.wait_for_results()\n\nprint(res) # [0, 0, 3, 6, 9]\n\n```\n\n\nThis project is still an early version, feedback is very helpful.',
    'author': 'Gabriel Kasser',
    'author_email': 'gabriel.kasser@gmail.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'https://gitlab.com/gabraken/olympipe',
    'packages': packages,
    'package_data': package_data,
    'python_requires': '>=3.7.2,<4.0',
}


setup(**setup_kwargs)
