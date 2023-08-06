# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['pushable']

package_data = \
{'': ['*']}

setup_kwargs = {
    'name': 'pushable',
    'version': '0.1.4',
    'description': 'Convert iterators into peekable, pushable iterators',
    'long_description': '## Package Description\n\n[![CircleCI](https://dl.circleci.com/status-badge/img/gh/sfkleach/pushable/tree/main.svg?style=svg)](https://dl.circleci.com/status-badge/redirect/gh/sfkleach/pushable/tree/main) [![Documentation Status](https://readthedocs.org/projects/pushable/badge/?version=latest)](https://pushable.readthedocs.io/en/latest/?badge=latest)\n\nThis is a Python package that provides a simple class Pushable that creates "pushable" iterators by wrapping an inner iterator/iterable. Pushable iterators act like dynamically expanding queues, allowing you to peek ahead or push items back onto the queue.\n\n\n## Basic Usage\n\nWe can turn any iterable/iterator into a pushable iterator using the constructor.\n```\ncount_up = Pushable( range( 0, 5 ) )\n```\n\nWe can use it like an ordinary iterator:\n```\nprint( next( count_up ) )\n# Prints 0\n```\n\nOr we can look-ahead to see what is coming:\n```\nwhats_up_next = count_up.peek()\nprint( whats_up_next )\n# Print 1\nprint( next( count_up ) )\n# Also prints 1 because peek does not remove the item from the internal queue.\n```\n\nWe can even push back items onto it:\n```\ncount_up.push("cat")\ncount_up.push("dog")\nprint( list( count_up ) )\n# Prints \'dog\', \'cat\', 2, 3, 4\n```\n\n## Examples\n\nFrom an iterator such as a file-object, which will iterate over the lines in a file, create a peekable/pushable iterator. This can be useful for example when we want to know if the iterator still has contents or want a sneak peek at what is coming.\n\n```py\nfrom pushable import Pushable\n\ndef read_upto_two_blank_lines( filename ):\n    with open( filename ) as file:\n        plines = Pushable( file )\n        # Pushable iterators can be used as booleans in the natural way.\n        while plines:\n            line = next( plines )\n            # peekOr makes it safe to look ahead.\n            if line == \'\\n\' and plines.peekOr() == \'\\n\':\n                # Two blank lines encountered.\n                break\n            else:\n                yield line        \n```\n\nIt is also useful to perform "macro-like" transformation.\n\n```py\nfrom pushable import Pushable\n\ndef translate( text, translations ):\n    ptokens = Pushable( text.split() )\n    while ptokens:\n        token = next(ptokens)\n        if token in translations:\n            ptokens.multiPush( *translations[token].split() )\n        else:\n            yield token\n\nprint( \' \'.join( translate( \'My name is MYNAME\', {\'MYNAME\':\'Fred Bloggs\'} ) ) ) \n# Prints: My name is Fred Bloggs\n```\n\n### More Complex Uses\n\nIn addition to peeking and popping items, which risks raising a\n`StopIteration` exception if there\'s nothing left on the internal queue, we\ncan utilise `peekOr` and `popOr` to deliver a default value instead. The \ndefault value is passed as an optional parameter and falls back to None.\n\nWe can also peek and pop multiple values using `multiPeekOr` and `multiPopOr`, \nwhich return generators. These support skipping over values so that you can\nget the 2nd and 3rd value without getting the first e.g.\n\n```py\n(second, third) = Pushable("pqr").multiPop(skip=1, count=2)\nprint( second, third )\n# Prints: q r\n```\n\nLastly, we can push multiple items with `multiPush`:\n```py\ncount_up.multiPush("cat", "dog", "rabbit")\nprint( list( count_up ) )\n# Prints: [\'cat\', \'dog\', \'rabbit\']\n```\n\nFor a full set of available methods see [the documentation](https://pushable.readthedocs.io/en/latest/pushable.html).\n',
    'author': 'Stephen Leach',
    'author_email': 'sfkleach@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://pushable.readthedocs.io/en/latest/',
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'python_requires': '>=3.10,<4.0',
}


setup(**setup_kwargs)
