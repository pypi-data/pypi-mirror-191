# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['nekontrol', 'nekontrol.interactive']

package_data = \
{'': ['*']}

install_requires = \
['appdirs>=1.4.4,<2.0.0',
 'click>=8.1.3,<9.0.0',
 'natsort>=8.2.0,<9.0.0',
 'requests>=2.28.2,<3.0.0',
 'termcolor>=2.2.0,<3.0.0']

entry_points = \
{'console_scripts': ['nk = nekontrol.interactive.cli:cli']}

setup_kwargs = {
    'name': 'nekontrol',
    'version': '0.2.1',
    'description': 'A program for testing kattis solutions with input and output.',
    'long_description': '# nekontrol - Control your kattis solutions\n\nThis is a simple program that compiles, runs and tests your kattis solutions\nagainst local and sample input and output.\n\n## Demo\n\n![Demo](https://raw.githubusercontent.com/Quaqqer/nekontrol/main/res/demo.svg)\n\n## Features\n\n- Automatically downloads sample input and output\n- Discovers local sample input and output\n- Compiles your source code and runs it with local and sample input and output\n- Ignores debug messages - ignores lines starting with "dbg" or "debug" and\n  inline messages "(dbg...)" and "(debug...)". If debug lines are discovered\n  then you are notified in the output so that you don\'t submit something that is\n  incorrect.\n\nThe current supported languages are:\n\n- C++ (requires `c++` in your path)\n- Rust (requirest `rustc` in your path)\n- Python (requires python in your path)\n- Haskell (requires `ghc` in your path)\n- Lua (requires `lua` in your path)\n- JavaScript (Node) (requires `node` in your path)\n\n> **Note**\n> Nekontrol will try to find a way to run your program, but it is not guranteed\n> that the program it uses matches the version that kattis has. For instance\n> kattis runs python with pypy 3.8. Nekontrol will try to run it with pypy 3.8,\n> but will fall back to other versions if it cannot be found.\n\nAdding more languages is left as an exercise for the reader.\n\n## Usage\n\nSimply run `nk <source file>` and it should hopefully compile (if needed)\nand run!\n\n- `nk` assumes that the name of the source files matches the name of the\n  problem (found in the url, ex. https://open.kattis.com/problems/<b>hello</b>).\n  If this assumption is incorrect, you can specify the problem with\n  `--problem <problem name>`. Local files are still matched with the filename\n  regardless of the problem specified.\n- Input and output files should follow the format `<filename>.in` or\n  `<filename>.<number>.in` and corresponding outputs are named `<filename>.ans`\n  etc. where `<filename>` comes from `nk <filename>.cpp` for instance.\n\n> **Note**\n> Multiple files are not supported as of yet\n\n## Requirements\n\n- The requirements of this program is only having python 3.10 or newer as well\n  pip\n- A half decent terminal, almost anything other than cmd.exe on windows will\n  work\n\n## Install or update\n\nTo install or update, run the following.\n\n```sh\npip install -U nekontrol\n```\n\nNow it should hopefully work, enjoy!\n\n### Nix\n\nThere is a flake for Nix users, but if you use Nix I trust you know how to use\nflakes.\n\n## Other\n\n- If you are thinking "nekontrol is a kinda weeby name", I ask you: have you\n  ever tried coming up with an original name?\n',
    'author': 'Emanuel S',
    'author_email': 'emanuel@empa.xyz',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'https://github.com/Quaqqer/nekontrol',
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.10,<4.0',
}


setup(**setup_kwargs)
