# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['sphinxcontrib', 'sphinxcontrib.autoyaml']

package_data = \
{'': ['*']}

install_requires = \
['Sphinx>=3.5.1', 'ruamel.yaml>=0.16.12,<0.17.0']

setup_kwargs = {
    'name': 'sphinxcontrib-autoyaml',
    'version': '1.1.0',
    'description': 'Sphinx autodoc extension for documenting YAML files from comments',
    'long_description': '# sphinxcontrib-autoyaml\n\nThis Sphinx autodoc extension documents YAML files from comments. Documentation\nis returned as reST definitions, e.g.:\n\nThis document:\n\n```\n###\n# Enable Nginx web server.\nenable_nginx: true\n\n###\n# Enable Varnish caching proxy.\nenable_varnish: true\n```\n\nwould be turned into text:\n\n```\nenable_nginx\n\n   Enable Nginx web server.\n\nenable_varnish\n\n   Enable Varnish caching proxy.\n```\n\nSee `tests/examples/output/*.yml` and `tests/examples/output/*.txt` for\nmore examples.\n\n`autoyaml` will take into account only comments which first line starts with\n`autoyaml_doc_delimiter`.\n\n## Usage\n\nYou can use `autoyaml` directive, where you want to extract comments\nfrom YAML file, e.g.:\n\n```\nSome title\n==========\n\nDocumenting single YAML file.\n\n.. autoyaml:: some_yml_file.yml\n```\n\n## Options\n\nOptions available to use in your configuration:\n\n- *autoyaml_root*(`..`)\n  Look for YAML files relatively to this directory.\n- *autoyaml_doc_delimiter*(`###`)\n  Character(s) which start a documentation comment.\n- *autoyaml_comment*(`#`)\n  Comment start character(s).\n- *autoyaml_level*(`1`)\n  Parse comments from nested structures n-levels deep.\n\n## Installing\n\nIssue command:\n\n```\npip install sphinxcontrib-autoyaml\n```\n\nAnd add extension in your project\'s ``conf.py``:\n\n```\nextensions = ["sphinxcontrib.autoyaml"]\n```\n\n## Caveats\n\n### Mapping keys nested in sequences\n\nSequences are traversed as well, but they are not represented in output\ndocumentation. This extension focuses only on documenting mapping keys. It means\nthat structure like this:\n\n```yaml\nkey:\n  ###\n  # comment1\n  - - inner_key1: value\n      ###\n      # comment2\n      inner_key2: value\n  ###\n  # comment3\n  - inner_key3: value\n```\n\nwill be flattened, so it will appear as though inner keys exist directly under\n`key`. Duplicated key documentation will be duplicated in output as well. See\n`tests/examples/output/comment-in-nested-sequence.txt` and\n`tests/examples/output/comment-in-nested-sequence.yml` to get a better\nunderstanding how sequences are processed.\n\n### Complex mapping keys\n\nYAML allows for complex mapping keys like so:\n\n```yaml\n[1, 2]: value\n```\n\nThese kind of keys won\'t be documented in output, because it\'s unclear how they\nshould be represented as a string.\n\n### Flow-style entries\n\nYAML allows writing complex data structures in single line like JSON.\nDocumentation is generated only for the first key in such entry, so this:\n\n```yaml\n###\n# comment\nkey: {key1: value, key2: value, key3: value}\n```\n\nwould yield documentation only for `key`.\n',
    'author': 'Jakub Pieńkowski',
    'author_email': 'jakub+sphinxcontrib-autoyaml@jakski.name',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'https://github.com/Jakski/sphinxcontrib-autoyaml',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)
