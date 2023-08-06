# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['klocmod']

package_data = \
{'': ['*']}

extras_require = \
{'yaml': ['pyyaml>=6.0,<7.0']}

setup_kwargs = {
    'name': 'klocmod',
    'version': '0.3.0',
    'description': 'A simple module providing facilities to localize small programs via textual files.',
    'long_description': 'klocmod -- Kozalo\'s Localization Module\n======================================\n\n*Screw you, gettext! I don\'t wanna bother of compiling strings into binary files!*\n\n[![Build Status](https://github.com/kozalosev/klocmod/actions/workflows/ci-build.yml/badge.svg)](https://github.com/kozalosev/klocmod/actions/workflows/ci-build.yml)\n[![Documentation Status](https://readthedocs.org/projects/klocmod/badge/?version=latest)](https://klocmod.readthedocs.io/en/latest/?badge=latest)\n\nThis module provides a very simple, suboptimal way for localizing your scripts, bots or applications. The advantage is\nits simplicity: to supply some sets of different string literals for different languages, you just need a simple JSON,\nYAML or INI file (or even a dict) fed to the library. After that, the only thing you should take care of is to get an\ninstance of the dictionary for a specific language and extract messages from it by key values.\n\nAll you mostly want is the `LocalizationsContainer` class. In particular, its static method \n`LocalizationsContainer.from_file()` that reads a localization file and returns an instance of the factory. The factory\nis supposed to produce instances of the `LanguageDictionary` class. Most likely, you will encounter instances of its\nsubclass -- the `SpecificLanguageDictionary` class (the base class is only used as a fallback that returns passed key\nvalues back).\n\n\nInstallation\n------------\n\n```bash\n# basic installation\npip install klocmod\n# or with YAML files support enabled\npip install klocmod[YAML]\n```\n\n\nExamples of localization files\n------------------------------\n\n### JSON (language first)\n\n```json\n{\n  "en": {\n    "yes": "yes",\n    "no": "no"\n  },\n  "ru-RU": {\n    "yes": "да",\n    "no": "нет"\n  }\n}\n```\n\n### JSON (phrase first)\n\n```json\n{\n  "yes": {\n    "en": "yes",\n    "ru-RU": "да"\n  },\n  "no": {\n    "en": "no",\n    "ru-RU": "нет"\n  }\n}\n```\n\n### INI\n\n```ini\n[DEFAULT]\nyes = yes\nno = no\n\n[ru-RU]\nyes = да\nno = нет\n```\n\n### YAML\n\nRequires an extra dependency: *PyYAML*.\n\n```yaml\n# language first\nen:\n  yes: yes\n  no: no\nru-RU:\n  yes: да\n  no: нет\n---\n# phrase first\nyes:\n  en: yes\n  ru-RU: да\nno:\n  en: no\n  ru-RU: нет\n```\n\n\nCode example\n------------\n\n```python\nfrom klocmod import LocalizationsContainer\n\nlocalizations = LocalizationsContainer.from_file("localization.json")\nru = localizations.get_lang("ru")\n# or\nen = localizations.get_lang()    # get default language\n# then\nprint(ru[\'yes\'])    # output: да\n# alternative ways to get a specific phrase:\nlocalizations.get_phrase("ru-RU", "no")\nlocalizations[\'ru-RU\'][\'no\']\n```\n',
    'author': 'Leonid Kozarin',
    'author_email': 'kozalo@sadbot.ru',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'https://kozalo.ru/#post-1541257200',
    'packages': packages,
    'package_data': package_data,
    'extras_require': extras_require,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
