# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['msgpack_serializer']

package_data = \
{'': ['*']}

install_requires = \
['django>=3.2,<5', 'msgpack>=1.0.4,<2.0.0']

setup_kwargs = {
    'name': 'django-msgpack-serializer',
    'version': '1.0.0',
    'description': 'A MsgPack serializer for Django.',
    'long_description': '==================\nmsgpack_serializer\n==================\n\nProvides a msgpack_ serializer/deserializer for Django models instances.\n\n------------\nInstallation\n------------\n\nAdd the module `msgpack_serializer.serializer` to your `SERIALIZATION_MODULES` setting:\n\n::\n\n    SERIALIZATION_MODULES = {\n        "msgpack" : "msgpack_serializer.serializer",\n    }\n\n-----\nUsage\n-----\n\nTo serialize:\n\n::\n\n    from django.core import serializers\n\n    msgpack_serializer = serializers.get_serializer("msgpack")()\n    data = msgpack_serializer.serialize(my_objects)  # returns bytes\n\n\nTo deserialize:\n\n::\n\n    from django.core import serializers\n\n    deserialized_objects = serializers.deserialize(\'msgpack\', data)\n    objs = [deserialized.object for deserialized in deserialized_objects]\n\n.. _msgpack: http://msgpack.org\n',
    'author': 'Flavio Curella',
    'author_email': 'flavio.curella@gmail.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'https://github.com/fcurella/django-msgpack-serializer',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8.1,<4.0.0',
}


setup(**setup_kwargs)
