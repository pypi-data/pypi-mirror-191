# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['kgx',
 'kgx.cli',
 'kgx.graph',
 'kgx.graph_operations',
 'kgx.parsers',
 'kgx.sink',
 'kgx.source',
 'kgx.utils']

package_data = \
{'': ['*']}

install_requires = \
['Click',
 'SPARQLWrapper>=1.8.2,<2.0.0',
 'Sphinx',
 'bmt>=1.0.0,<2.0.0',
 'cachetools>=5.0.0,<6.0.0',
 'deprecation>=2.1.0,<3.0.0',
 'docker>=5.0.3,<6.0.0',
 'docutils>=0.18.1,<0.19.0',
 'ijson>=3.1.3,<4.0.0',
 'jsonlines>=3.1.0,<4.0.0',
 'jsonstreams>=0.6.0,<0.7.0',
 'linkml-runtime>=1.4,<2.0',
 'linkml>=1.4,<2.0',
 'mypy',
 'neo4j>=4.4.10,<5.0.0',
 'networkx',
 'ordered-set>=4.0.2,<5.0.0',
 'pandas>=1.0.3,<2.0.0',
 'prefixcommons>=0.1.4,<0.2.0',
 'prologterms>=0.0.6,<0.0.7',
 'pytest',
 'python-dateutil>=2.8.1,<3.0.0',
 'pyyaml',
 'rdflib>=6.0.0,<7.0.0',
 'recommonmark',
 'shexjsg',
 'sphinx-click',
 'sphinx-rtd-theme',
 'stringcase>=1.2.0,<2.0.0',
 'terminaltables>=3.1.0,<4.0.0',
 'tox-docker',
 'tox>=3.28.0,<4.0.0',
 'validators>=0.20.0,<0.21.0']

setup_kwargs = {
    'name': 'kgx',
    'version': '0.0.0',
    'description': 'A Python library and set of command line utilities for exchanging Knowledge Graphs (KGs) that conform to or are aligned to the Biolink Model.',
    'long_description': '# Knowledge Graph Exchange\n\n[![Python](https://img.shields.io/badge/python-3.9+-blue.svg)]()\n![Run tests](https://github.com/biolink/kgx/workflows/Run%20tests/badge.svg)[![Documentation Status](https://readthedocs.org/projects/kgx/badge/?version=latest)](https://kgx.readthedocs.io/en/latest/?badge=latest)\n[![Quality Gate Status](https://sonarcloud.io/api/project_badges/measure?project=biolink_kgx&metric=alert_status)](https://sonarcloud.io/dashboard?id=biolink_kgx)\n[![Maintainability Rating](https://sonarcloud.io/api/project_badges/measure?project=biolink_kgx&metric=sqale_rating)](https://sonarcloud.io/dashboard?id=biolink_kgx)\n[![Coverage](https://sonarcloud.io/api/project_badges/measure?project=biolink_kgx&metric=coverage)](https://sonarcloud.io/dashboard?id=biolink_kgx)\n[![PyPI](https://img.shields.io/pypi/v/kgx)](https://img.shields.io/pypi/v/kgx)\n[![Docker](https://img.shields.io/static/v1?label=Docker&message=biolink/kgx:latest&color=orange&logo=docker)](https://hub.docker.com/r/biolink/kgx)\n\nKGX (Knowledge Graph Exchange) is a Python library and set of command line utilities for exchanging\nKnowledge Graphs (KGs) that conform to or are aligned to the [Biolink Model](https://biolink.github.io/biolink-model/).\n\nThe core datamodel is a [Property Graph](https://neo4j.com/developer/graph-database/) (PG), represented\ninternally in Python using a [networkx MultiDiGraph model](https://networkx.github.io/documentation/stable/reference/classes/generated/networkx.MultiDiGraph.edges.html).\n\nKGX allows conversion to and from:\n\n * RDF serializations (read/write) and SPARQL endpoints (read)\n * Neo4j endpoints (read) or Neo4j dumps (write)\n * CSV/TSV and JSON (see [associated data formats](./data-preparation.md) and [example script to load CSV/TSV to Neo4j](./examples/scripts/load_csv_to_neo4j.py))\n * Reasoner Standard API format\n * OBOGraph JSON format\n\nKGX will also provide validation, to ensure the KGs are conformant to the Biolink Model: making sure nodes are\ncategorized using Biolink classes, edges are labeled using valid Biolink relationship types, and valid properties are used.\n\nInternal representation is a property graph, specifically a networkx MultiDiGraph.\n\nThe structure of this graph is expected to conform to the Biolink Model standard, as specified in the [KGX format specification](specification/kgx-format.md).\n\nIn addition to the main code-base, KGX also provides a series of [command line operations](https://kgx.readthedocs.io/en/latest/examples.html#using-kgx-cli).\n\n### Error Detection and Reporting\n\nNon-redundant JSON-formatted structured error logging is now provided in KGX Transformer, Validator, GraphSummary and MetaKnowledgeGraph operations.  See the various unit tests for the general design pattern (using the Validator as an example here):\n\n```python\nfrom kgx.validator import Validator\nfrom kgx.transformer import Transformer\n\nValidator.set_biolink_model("2.11.0")\n\n# Validator assumes the currently set Biolink Release\nvalidator = Validator()\n\ntransformer = Transformer(stream=True)\n\ntransformer.transform(\n    input_args = {\n        "filename": [\n            "graph_nodes.tsv",\n            "graph_edges.tsv",\n        ],\n        "format": "tsv",\n    },\n    output_args={\n        "format": "null"\n    },\n    inspector=validator,\n)\n\n# Both the Validator and the Transformer can independently capture errors\n\n# The Validator, from the overall semantics of the graph...\n# Here, we just report severe Errors from the Validator (no Warnings)\nvalidator.write_report(open("validation_errors.json", "w"), "Error")\n\n# The Transformer, from the syntax of the input files... \n# Here, we catch *all* Errors and Warnings (by not providing a filter)\ntransformer.write_report(open("input_errors.json", "w"))\n```\n\nThe JSON error outputs will look something like this:\n\n```json\n{\n    "ERROR": {\n        "MISSING_EDGE_PROPERTY": {\n            "Required edge property \'id\' is missing": [\n                "A:123->X:1",\n                "B:456->Y:2"\n            ],\n            "Required edge property \'object\' is missing": [\n                "A:123->X:1"\n            ],\n            "Required edge property \'predicate\' is missing": [\n                "A:123->X:1"\n            ],\n            "Required edge property \'subject\' is missing": [\n                "A:123->X:1",\n                "B:456->Y:2"\n            ]\n        }\n    },\n    "WARNING": {\n        "DUPLICATE_NODE": {\n          "Node \'id\' duplicated in input data": [\n            "MONDO:0010011",\n            "REACT:R-HSA-5635838"\n          ]\n        }\n    }\n}\n\n```\n\nThis system reduces the significant redundancies of earlier line-oriented KGX  logging text output files, in that graph entities with the same class of error are simply aggregated in lists of names/identifiers at the leaf level of the JSON structure.\n\nThe top level JSON tags originate from the `MessageLevel` class and the second level tags from the `ErrorType` class in the [error_detection](kgx/error_detection.py) module, while the third level messages are hard coded as `log_error` method messages in the code.  \n\nIt is likely that additional error conditions within KGX can be efficiently captured and reported in the future using this general framework.\n\n## Installation\n\nThe installation for KGX requires Python 3.9 or greater.\n\n\n### Installation for users\n\n\n#### Installing from PyPI\n\nKGX is available on PyPI and can be installed using\n[pip](https://pip.pypa.io/en/stable/installing/) as follows,\n\n```bash\npip install kgx\n```\n\nTo install a particular version of KGX, be sure to specify the version number,\n\n```bash\npip install kgx==0.5.0\n```\n\n\n#### Installing from GitHub\n\nClone the GitHub repository and then install,\n\n```bash\ngit clone https://github.com/biolink/kgx\ncd kgx\npython setup.py install\n```\n\n\n### Installation for developers\n\n#### Setting up a development environment\n\nTo build directly from source, first clone the GitHub repository,\n\n```bash\ngit clone https://github.com/biolink/kgx\ncd kgx\n```\n\nThen install the necessary dependencies listed in ``requirements.txt``,\n\n```bash\npip3 install -r requirements.txt\n```\n\n\nFor convenience, make use of the `venv` module in Python3 to create a\nlightweight virtual environment,\n\n```\npython3 -m venv env\nsource env/bin/activate\n\npip install -r requirements.txt\n```\n\nTo install KGX you can do one of the following,\n\n```bash\npip install .\n\n# OR \n\npython setup.py install\n```\n\n### Setting up a testing environment for Neo4j\n\nThis release of KGX supports graph source and sink transactions with the 4.3 release of Neo4j.\n\nKGX has a suite of tests that rely on Docker containers to run Neo4j specific tests.\n\nTo set up the required containers, first install [Docker](https://docs.docker.com/get-docker/)\non your local machine.\n\nOnce Docker is up and running, run the following commands:\n\n```bash\ndocker run -d --rm --name kgx-neo4j-integration-test \\\n            -p 7474:7474 -p 7687:7687 \\\n            --env NEO4J_AUTH=neo4j/test  \\\n            neo4j:4.3\n```\n\n```bash\ndocker run -d --rm --name kgx-neo4j-unit-test  \\\n            -p 8484:7474 -p 8888:7687 \\\n            --env NEO4J_AUTH=neo4j/test \\\n            neo4j:4.3\n```\n\n\n**Note:** Setting up the Neo4j container is optional. If there is no container set up\nthen the tests that rely on them are skipped.\n',
    'author': 'Deepak Unni',
    'author_email': 'deepak.unni3@gmail.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.9,<4.0',
}


setup(**setup_kwargs)
