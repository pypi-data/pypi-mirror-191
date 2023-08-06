# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['color_bottles', 'color_bottles.frontend']

package_data = \
{'': ['*']}

install_requires = \
['colorama>=0.4.6,<0.5.0']

extras_require = \
{'pygame': ['pygame>=2,<3']}

entry_points = \
{'console_scripts': ['color-bottles = color_bottles.play_game:run',
                     'color-bottles-console = '
                     'color_bottles.frontend.console_front:run_game',
                     'color-bottles-pygame = '
                     'color_bottles.frontend.pygame_front:run_game']}

setup_kwargs = {
    'name': 'color-bottles-puzzle',
    'version': '0.0.4',
    'description': 'Water color sort puzzle game',
    'long_description': '## Color bottles puzzle\n\n 🌡️ Watter color sort puzzle game 🧪\n\n### Install and play:\n```\npip install color-bottles-puzzle\n\ncolor-bottles\n```\n\n### 📈 Objective\nMake bottles full with one color or empty -> 📊\n\n### 📌 Rules\nYou can pour color water from one bottle to another only if destination bottle is not full, is empty or have same color on top.\n \n## 🕹️ Controls (Console frontend)\nTo pour from bottle `3` to bottle `7` just type `3 7` and enter.  \nIf number of bottles less then 10, you can ommit the space 💥   \nAlso you can pour multiple times by 1 hit 🔥 - just type in a row \nlike `5718` or `5 7 1 8` - will pour `5` to `7` and then `1` to `8`   \n🔴 To exit - type `q`   \n🔮 Good luck !!  \n\nExamples of a game (monospaced font in console work just fine):\n\n```\n🔮 Good luck !!\n\n\n    |⬛️|    |🟦|    |⬛️|    |🟧|    |🟫|    |🟩|    |🟪|    |  |    |  |  \n    |⬛️|    |🟩|    |🟫|    |🟪|    |🟩|    |🟥|    |🟫|    |  |    |  |  \n    |🟧|    |🟫|    |🟥|    |🟧|    |🟧|    |🟪|    |🟦|    |  |    |  |  \n    |🟩|    |🟥|    |🟦|    |🟥|    |⬛️|    |🟪|    |🟦|    |  |    |  |  \n      0       1       2       3       4       5       6       7       8\n\n 🎮 your turn:  0 7   2 7   3 0   4 2   5 4   6 3\n\n    |  |    |🟦|    |🟫|    |🟪|    |🟩|    |  |    |  |    |  |    |  |  \n    |🟧|    |🟩|    |🟫|    |🟪|    |🟩|    |🟥|    |🟫|    |⬛️|    |  |  \n    |🟧|    |🟫|    |🟥|    |🟧|    |🟧|    |🟪|    |🟦|    |⬛️|    |  |  \n    |🟩|    |🟥|    |🟦|    |🟥|    |⬛️|    |🟪|    |🟦|    |⬛️|    |  |  \n      0       1       2       3       4       5       6       7       8\n\n 🎮 your turn:  6 8   2 8   5 2   3 5 \n\n    |  |    |🟦|    |  |    |  |    |🟩|    |🟪|    |  |    |  |    |  |  \n    |🟧|    |🟩|    |🟥|    |  |    |🟩|    |🟪|    |  |    |⬛️|    |🟫|  \n    |🟧|    |🟫|    |🟥|    |🟧|    |🟧|    |🟪|    |🟦|    |⬛️|    |🟫|  \n    |🟩|    |🟥|    |🟦|    |🟥|    |⬛️|    |🟪|    |🟦|    |⬛️|    |🟫|  \n      0       1       2       3       4       5       6       7       8\n\n 🎮 your turn:  \n\n```\n\n### Frontend\n\nThere is a `core` module (water sort rules logic) of color bottles that is frontend agnostic.\nThats why we have 2 frontends for now \n 1. `console` - using `print()` - default\n 2. `pygame` - using pygame GUI \n\nTo run game with pygame GUI, install package with pygame extras:\n```\npython3 -m venv env\nsource env/bin/activate\npip install "color-bottles-puzzle[pygame]"\n\ncolor-bottles\n```\n\n### Roadmap\n - [ ] Test for game logic\n - [ ] Test console game\n - [ ] Solver\n - [ ] Levels\n - [ ] More frontend\n - [ ] Github actions CI',
    'author': 'Stepan Dvoiak',
    'author_email': 'dvoiak.stepan@gmail.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'https://github.com/oyvsyo/color-bottles-puzzle',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'extras_require': extras_require,
    'entry_points': entry_points,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
