# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['sfdevtools',
 'sfdevtools.app',
 'sfdevtools.devTools',
 'sfdevtools.grpc_protos',
 'sfdevtools.observability',
 'sfdevtools.observability.logging_json',
 'sfdevtools.observability.logstash',
 'sfdevtools.storage',
 'sfdevtools.storage.objectStorage',
 'sfdevtools.storage.relationalDBStorage']

package_data = \
{'': ['*']}

install_requires = \
['boto3>=1.26.61,<2.0.0',
 'grpcio-tools==1.43.0',
 'grpcio==1.43.0',
 'nanoid>=2.0.0,<3.0.0',
 'pandas>=1.5.3,<2.0.0']

setup_kwargs = {
    'name': 'sfdevtools',
    'version': '1.17.0',
    'description': '',
    'long_description': '## How to publish to pypi\n```bash\n# set up pypi token\npoetry config pypi-token.pypi my-token\n\n# build the project\npoetry build\n\n# publish the project\npoetry publish\n\n# DONE\n```\n\n## Generate source code from protobuf\n```bash\n$ poetry add grpcio-tools\n$ poetry add grpcio\n$ cd sfdevtools/\n$ poetry run python -m grpc_tools.protoc -I ./grpc_protos --python_out=./grpc_protos/ --grpc_python_out=./grpc_protos/ ./grpc_protos/peacock.proto\n```\n\n## Demo example\n### Double check lock for singleton\n```python\nimport sfdevtools.observability.log_helper as lh\nimport logging\nlogger = lh.init_logger(logger_name="sfdevtools_logger", is_json_output=False)\n# create class X\nclass X(SDC):\n    pass\n\n# create class Y\nclass Y(SDC):\n    pass\n\nA1, A2 = X.instance(), X.instance()\nB1, B2 = Y.instance(), Y.instance()\n\nassert A1 is not B1\nassert A1 is A2\nassert B1 is B2\n\nlogger.info(\'A1 : {}\'.format(A1))\nlogger.info(\'A2 : {}\'.format(A2))\nlogger.info(\'B1 : {}\'.format(B1))\nlogger.info(\'B2 : {}\'.format(B2))\n```\n\n### Send log to logstash\n```python\nlogger = lh.init_logger(logger_name="connection_tester_logger"\n                        , is_json_output=False\n                        , is_print_to_console=True\n                        , is_print_to_logstash=True\n                        , logstash_host="<the host name>"\n                        , logstash_port=5960\n                        , logstash_user_tags=["Test001", "Test002"])\nlogger.info("Test Message from test")\nlogger.error("Test Message from test")\nlogger.warning("Test Message from test")\n```\n',
    'author': 'SulfredLee',
    'author_email': 'sflee1112@gmail.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
