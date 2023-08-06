# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['toodledo']

package_data = \
{'': ['*']}

install_requires = \
['marshmallow>=3.18,<4.0', 'requests-oauthlib>=1.0,<2.0', 'requests>=2.20,<3.0']

setup_kwargs = {
    'name': 'toodledo',
    'version': '1.3.0',
    'description': 'Python wrapper for the Toodledo v3 API which is documented at http://api.toodledo.com/3/',
    'long_description': 'Overview\n========\n\nPython wrapper for the Toodledo v3 API which is documented at\nhttp://api.toodledo.com/3/. Available on PyPI at\nhttps://pypi.org/project/toodledo/.\n\nThis fork is being actively maintained by Jonathan Kamens\n<jik@kamens.us>. Thanks to Rehan Khwaja for creating this library.\n\nUsage\n=====\n\nIf you\'re using this library to build a web app that will be used by\nmultiple people, you need to be familiar with how to use OAuth2 for\nauthentication between your web app and Toodledo. Explaining how to do\nthat is beyond the scope of this document.\n\nTo use the library, you need to register an app in your Toodledo\naccount. This can be done at\nhttps://api.toodledo.com/3/account/doc_register.php. You will need the\nclient ID and client secret for your app shown on the registration\npage to connect to the API.\n\nIf you\'re using this library to build a private script you\'re running\nyourself, you will probably want to use the\n``CommandLineAuthorization`` function in the library to authenticate\nthe first time. Something like this:\n\n.. code-block:: python\n\n  import os\n  from toodledo import TokenStorageFile, CommandLineAuthorization\n  \n  tokenFilePath = "fill in path to token file"\n  clientId = "fill in your app client ID"\n  clientSecret = "fill in your app client secret"\n  scope = "basic tasks notes folders write"\n  tokenStorage = TokenStorageFile(tokenFilePath)\n\n  if not os.path.exists(tokenFilePath):\n      CommandLineAuthorization(clientId, clientSecret, scope, tokenStorage)\n\nIt will prompt you to visit a URL, which will prompt you to log into\nToodledo if you\'re not already logged in, then click a "SIGN IN"\nbutton. The sign in will fail since you presumably specified a bogus\nredirect URL when registering the app, but you can then copy the\nfailed URL from your browser back into the script to complete the\nauthentication process.\n\nOnce you\'ve authenticated, you create an API instance like this:\n\n.. code-block:: python\n\n  toodledo = Toodledo(\n    clientId=clientId,\n    clientSecret=clientSecret,\n    tokenStorage=tokenStorage, \n    scope=scope)\n\nAnd here\'s how you call the API:\n\n.. code-block:: python\n                \n  account = toodledo.GetAccount()\n\n  allTasks = toodledo.GetTasks(params={})\n\nSee `this more extensive example\n<https://gist.github.com/jikamens/bad36fadfa73ee4f0ac1269ab3025f67>`_\nof using the API in a script.\n\nUsing the task cache\n--------------------\n\nIn addition to close-to-the-metal access to the API endpoints, this\nlibrary also implements a `TaskCache` class that you can use to cache\ntasks persistently in a file which is updated incrementally when\nthings change in Toodledo. Import the class and look at its help\nstring for more information.\n\nWhen you\'re using a cache, you can call `AddTasks`, `EditTasks`, and\n`DeleteTasks` through the cache object rather than directly through\nthe API object; otherwise the cache won\'t reflect the changes you make\nuntil you call `update()` explicitly on the cache. If you\'re making a\nbunch of updates in a row, you might want to them directly through the\nAPI and then call `update()` to minimize the number of API calls to\nthe server.\n\nWhen you\'re using the cache, instead of using `GetTasks` you will\nprobably want to read tasks through the cache, which you can do simply\nby treating the cache object as a list of available tasks.\n\nDeveloping the library\n======================\n\nThe library uses ``poetry`` for managing packages, building, and\npublishing. You can do ``poetry install`` at the top level of the\nsource tree to install all of the needed dependencies to build and run\nthe library. ``poetry build`` builds packages, and ``poetry publish``\npublishes them to PyPI.\n\nAll the code in the library is both pylint and flake8 clean, and any\nPRs that are submitted should maintain that. Run ``poetry run pylint\n*.py tests toodledo`` and ``poetry run flake8`` to check everything.\n\nTo run the tests, set the following environment variables:\n\n- TOODLEDO_TOKEN_STORAGE - path to a json file which will contain the\n  credentials\n- TOODLEDO_CLIENT_ID - your client id (see\n  https://api.toodledo.com/3/account/doc_register.php)\n- TOODLEDO_CLIENT_SECRET - your client secret (see\n  https://api.toodledo.com/3/account/doc_register.php)\n\nThen generate the credentials json file by running\n\n.. code-block:: bash\n\n  poetry run python generate-credentials.py\n\nThen run the tests by executing\n\n.. code-block:: bash\n\n  poetry run pytest\n\nin the root directory.\n\nPlease ensure that all the tests pass in any PRs you submit.\n',
    'author': 'Jonathan Kamens',
    'author_email': 'jik@kamens.us',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'https://github.com/jikamens/toodledo-python',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.7.2',
}


setup(**setup_kwargs)
