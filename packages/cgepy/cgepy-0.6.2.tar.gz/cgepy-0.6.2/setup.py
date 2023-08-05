# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['cgepy', 'cgepy.unstable']

package_data = \
{'': ['*']}

setup_kwargs = {
    'name': 'cgepy',
    'version': '0.6.2',
    'description': 'Tools for developing graphical programs inside the console.',
    'long_description': '### cgepy // 6.2\n***\ncgePy, or cge, is a text-based graphics engine that can operate in the console or terminal.\\\nCurrently with zero dependencies, a simple system that can suit many needs, and easily tweaked settings, cgePy will allow you to turn complex ideas into reality.\n\n***\n\n### How it works:\n\ncgePy currently operates on 24-bit ansi escape codes. Esentially what\'s happening when you create a grid is you have `gridsize` items of `background + "  "` being appended to a list. (`self.ctx`)\\\nEach of these items on the list should always be two characters long, resulting in the grid becoming a perfect square, not rectangle.\\\nAnd no, just because squares are rectangles doesn\'t mean it could be three or one characters.\n\n`background` is set to `BLUE` (aka `cgepy.BLUE`) by default, with `BLUE` being `\\x1b[0;44m` for a background. The advantage of this is that we can put text inside a grid since we aren\'t relying on colored fullblock charactes, and that we can have much more flexibility. Esentially, you can also cross these with other ansi codes to create more diverse coloring. \n\nAfter that, a function reads from the list and prints it in rows according to the square root of `gridsize`. Without that, you\'d be stuck with a basic 10x10 grid forever. The difference between cgePy and projects with similar concepts is that cgePy  **only needs one list**, while other projects might use several. A 5x5 list / cgePy "grid" might look like this:\n```py\n[\n    BLACK+"  ", BLACK+"  ", BLACK+"  ", BLACK+"  ", BLACK+"  ",\n    BLACK+"  ", WHITE+"  ", WHITE+"  ", WHITE+"  ", BLACK+"  ",\n    BLACK+"  ", WHITE+"  ", WHITE+"  ", WHITE+"  ", BLACK+"  ",\n    BLACK+"  ", WHITE+"  ", WHITE+"  ", WHITE+"  ", BLACK+"  ",\n    BLACK+"  ", BLACK+"  ", BLACK+"  ", BLACK+"  ", BLACK+"  "\n]\n```\n\nAnyways, for now, **that\'s all, folks!**\\\nSee you in the next release.',
    'author': 'catbox305',
    'author_email': 'lion712yt@gmail.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'packages': packages,
    'package_data': package_data,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
