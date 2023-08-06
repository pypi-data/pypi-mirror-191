# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['dedup_me']

package_data = \
{'': ['*']}

setup_kwargs = {
    'name': 'dedup-me',
    'version': '0.2.0',
    'description': 'Deduplicate concurrent function calls.',
    'long_description': "[![PyPI version](https://badge.fury.io/py/dedup-me.svg)](https://badge.fury.io/py/dedup-me)\n\n# dedup_me\n\ndedup_me is a simple library for concurrent in-flight deduplication of functions.\nThis can be useful for e.g. API calls or DB access. Instead of querying the same data multiple times,\nthis library allows you to query once and share the result.\n\nNote: This library does not cache results. After the result is returned, new consumers will call the function(API, DB, ...) again.\n\n# Installation\n```shell\npip install dedup-me\n```\n\n# Usage\n\n## AsyncIO\n\n```python\nimport asyncio\nimport random\n\nfrom dedup_me import async_dedup\n\n# @async_dedup('static-key')  # if the arguments don't matter, you can use a static key\n@async_dedup(key = lambda x: f'dynamic-key-{x}')  # or pass in a key function that accepts all arguments\nasync def expensive_function(x: int) -> int:\n    print('expensive function called')\n    await asyncio.sleep(x)\n    return random.randint(0, 10)\n\n\nasync def main() -> None:\n    # call the function 10 times\n    # this should only print 'expensive function called' once\n    results = await asyncio.gather(\n        *(\n            expensive_function(1)\n            for _ in range(10)\n        )\n    )\n    print(results)\n    # all results should be the same\n    results_list = list(results)\n    assert results_list == [results_list[0]] * 10\n```\n\nAlternatively, without the decorator:\n```python\nimport asyncio\nimport random\n\nfrom dedup_me import AsyncDedup\n\n\nasync def expensive_function() -> int:\n    print('expensive function called')\n    await asyncio.sleep(1)\n    return random.randint(0, 10)\n\n\nasync def main() -> None:\n    dedup = AsyncDedup()\n    await asyncio.gather(\n        *(\n            # functions are grouped by the key, choose something that represents the function and its arguments\n            # the second argument must be a function without arguments that returns an awaitable\n            dedup.run('some-key', lambda: expensive_function())\n            for _ in range(10)\n        )\n    )\n```\n\n## Threads\n\nFor threading just use the `threading_dedup` decorator or `ThreadingDedup`.\n```python\nfrom time import sleep\nfrom dedup_me import threading_dedup, ThreadingDedup\n\n\n@threading_dedup('key')\ndef expensive_function() -> None:\n    sleep(1)\n\nexpensive_function()\n\n# or\ndedup = ThreadingDedup()\ndedup.run('key', lambda: sleep(1))\n```\n\n## Forcing a new execution\nYou can enforce a new execution by passing `force_new = True` to the `run` function.\nWhen using the decorator, you can add a callable that will receive all arguments and returns a boolean.\n",
    'author': 'Christopher Krause',
    'author_email': 'ottermata@pm.me',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'https://github.com/ottermata/dedup_me',
    'packages': packages,
    'package_data': package_data,
    'python_requires': '>=3.10,<4.0',
}


setup(**setup_kwargs)
