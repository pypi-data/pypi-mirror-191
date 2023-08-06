# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['pynumaflow',
 'pynumaflow.function',
 'pynumaflow.function.generated',
 'pynumaflow.sink',
 'pynumaflow.sink.generated',
 'pynumaflow.tests',
 'pynumaflow.tests.function',
 'pynumaflow.tests.sink']

package_data = \
{'': ['*']}

install_requires = \
['google-api-core>=2.11.0,<3.0.0',
 'google-cloud>=0.34.0,<0.35.0',
 'grpcio-tools>=1.48.1,<2.0.0',
 'grpcio>=1.48.1,<2.0.0',
 'protobuf>=3.20.0,<3.21.0']

setup_kwargs = {
    'name': 'pynumaflow',
    'version': '0.3.3',
    'description': 'Provides the interfaces of writing Python User Defined Functions and Sinks for NumaFlow.',
    'long_description': '# Python SDK for Numaflow\n\nThis SDK provides the interface for writing [UDFs](https://numaflow.numaproj.io/user-guide/user-defined-functions/) \nand [UDSinks](https://numaflow.numaproj.io/user-guide/sinks/user-defined-sinks/) in Python.\n\n## Implement a User Defined Function (UDF)\n\n\n### Map\n\n```python\nfrom pynumaflow.function import Messages, Message, Datum, UserDefinedFunctionServicer\n\n\ndef my_handler(key: str, datum: Datum) -> Messages:\n    val = datum.value\n    _ = datum.event_time\n    _ = datum.watermark\n    messages = Messages(Message.to_vtx(key, val))\n    return messages\n\n\nif __name__ == "__main__":\n    grpc_server = UserDefinedFunctionServicer(map_handler=my_handler)\n    grpc_server.start()\n```\n\n### Reduce\n\n```python\nimport asyncio\nfrom typing import Iterator\nfrom pynumaflow.function import Messages, Message, Datum, Metadata, UserDefinedFunctionServicer\n\n\nasync def my_handler(key: str, datums: Iterator[Datum], md: Metadata) -> Messages:\n    interval_window = md.interval_window\n    counter = 0\n    async for _ in datums:\n        counter += 1\n    msg = (\n        f"counter:{counter} interval_window_start:{interval_window.start} "\n        f"interval_window_end:{interval_window.end}"\n    )\n    return Messages(Message.to_vtx(key, str.encode(msg)))\n\n\nif __name__ == "__main__":\n    grpc_server = UserDefinedFunctionServicer(reduce_handler=my_handler)\n    asyncio.run(grpc_server.start())\n    asyncio.run(*grpc_server.cleanup_coroutines)\n```\n\n### Sample Image\nA sample UDF [Dockerfile](examples/function/forward_message/Dockerfile) is provided \nunder [examples](examples/function/forward_message).\n\n## Implement a User Defined Sink (UDSink)\n\n```python\nfrom typing import Iterator\nfrom pynumaflow.sink import Datum, Responses, Response, UserDefinedSinkServicer\n\n\ndef my_handler(datums: Iterator[Datum]) -> Responses:\n    responses = Responses()\n    for msg in datums:\n        print("User Defined Sink", msg.value.decode("utf-8"))\n        responses.append(Response.as_success(msg.id))\n    return responses\n\n\nif __name__ == "__main__":\n    grpc_server = UserDefinedSinkServicer(my_handler)\n    grpc_server.start()\n```\n\n### Sample Image\n\nA sample UDSink [Dockerfile](examples/sink/log/Dockerfile) is provided \nunder [examples](examples/sink/log).\n',
    'author': 'NumaFlow Developers',
    'author_email': 'None',
    'maintainer': 'Avik Basu',
    'maintainer_email': 'avikbasu93@gmail.com',
    'url': 'None',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8,<3.11',
}


setup(**setup_kwargs)
