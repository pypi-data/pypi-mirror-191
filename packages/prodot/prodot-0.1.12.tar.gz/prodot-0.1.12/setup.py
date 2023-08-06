# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['prodot', 'prodot.json_tools']

package_data = \
{'': ['*']}

install_requires = \
['jsonpath-ng>=1.5.3,<2.0.0']

setup_kwargs = {
    'name': 'prodot',
    'version': '0.1.12',
    'description': '',
    'long_description': '# Prodot\n\nA new way to deal with dictionaries and lists in python.\nTreat data like classes, or by reading/writing data with json paths\n```Python\n>>> from prodot import ProObject\n>>> my_obj = ProObject({\'foo\':{\'bar\':[\'eggs\']}})\n\n>>> my_obj.foo.bar.n1.get_value()\n\'eggs\'\n\n>>> my_obj[\'$.foo.bar.[0]\'].get_value()\n\'eggs\n```\n\n# Getting started\n\n## install\n```\npip install prodot\n```\n\n## Usage\n\nImport the pro object from the prodot library. You can create a new empty dictionary, or start with a filled one\n\n```Python\n# No parameters instances an empty dictionary\n>>> my_new_obj = ProObject() \n\n# The pro object can be initialized with a dictionary\n>>> my_dict_obj = ProObject({"foo":["bar","eggs"]})\n\n# The pro object can also initialize with a list\n>>> my_list_obj = ProObject([ [1,2,3], ["a","b","c"], [{"foo":"bar"}, {"bar":"eggs"}] ])\n\n```\n\n### Dot notation usage\nBy using the pro-object you can use the dictionary as a class\n\n```Python\n>>> my_json = {\n...     "userData": {\n...         "name": "John",\n...         "age": "38",\n...         "shoppingCart":[\n...             {"cellphone": 999.99},\n...             {"notebook": 2999.99},\n...             {"wireless keyboard": 299.99}\n...         ]\n...     }\n... }\n\n>>> my_new_obj = ProObject(my_json)\n\n>>> shoppingCart = my_new_obj.userData.shoppingCart\n```\n\nThe ProObject will return another instance of the ProObject with the main_object attribute as being the selected path.\n\n```Python\n>>> type(shoppingCart)\n<class \'prodot.pro_object.ProObject\'>\n```\n\nTo get the raw value of the object, you can use the `.get_value()` function.\n\n```Python\n>>> shoppingCart.get_value()\n[{"cellphone": 999.99}, {"notebook": 2999.99}, {"wireless keyboard": 299.99}]\n\n# or by using the get_value directly at the path\n>>> my_new_obj.userData.shoppingCart.get_value()\n[{"cellphone": 999.99}, {"notebook": 2999.99}, {"wireless keyboard": 299.99}]\n\n>>> type(shoppingCart.get_value())\n<class \'dict\'>\n```\n\nYou can also add new information to the instancied object\n\n```Python\n# n3 means list index 3 (will be added as 4th item)\n>>> my_new_obj.userData.shoppingCart.n3 = {"monitor": 699.99}\n>>> my_new_obj.userData.shoppingCart.get_value()\n[{"cellphone": 999.99}, {"notebook": 2999.99}, {"wireless keyboard": 299.99}, {"monitor": 399.99}]\n```\nPython doesn\'t accept list indexes to be used as a class attribute. For solve this problem, list indexes start with the `n` letter (like n0, n1, ...)\n\n### Json path usage\n\nIf you prefere or need to use json paths, it is possible to write and retrieve information using json path strings.\n\n```Python\n>>> my_new_obj[\'$.userData.shoppingCart[4]\'] = {\'FunStation 6 Series T\':\'699,99\'}\n\n>>> my_new_obj[\'$.userData.shoppingCart\'].get_value()\n[{"cellphone": 999.99}, {"notebook": 2999.99}, {"wireless keyboard": 299.99}, {"monitor": 399.99}, {\'FunStation 6 Series T\':\'699,99\'}]\n```\n\nNote that by using a json path string, list indexes must not have `n` as their first value.\n\nYou can view all possible json_paths from object by using the `get_all_paths` attribute.\n\n```Python\n>>> my_new_obj.get_all_paths()\n<generator object PathObject.all_paths_from_main_object at 0x7f6a012b5c80>\n\n>>> list(my_new_obj.get_all_paths())\n[\'.userData\', \'.userData.name\', \'.userData.age\', \'.userData.shoppingCart\', \'.userData.shoppingCart[0]\', \'.userData.shoppingCart[0].cellphone\', \'.userData.shoppingCart[1]\', \'.userData.shoppingCart[1].notebook\', \'.userData.shoppingCart[2]\', \'.userData.shoppingCart[2].wireless keyboard\', \'.userData.shoppingCart[3]\', \'.userData.shoppingCart[3].monitor\', \'.userData.shoppingCart[4]\', \'.userData.shoppingCart[4].FunStation 6 Series T\']\n```\n\n',
    'author': 'Matheus Menezes Almeida',
    'author_email': 'mrotame@gmail.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
