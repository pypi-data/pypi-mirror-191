# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['nextbrain']

package_data = \
{'': ['*']}

setup_kwargs = {
    'name': 'nextbrain',
    'version': '0.1.5',
    'description': 'Convenient access to the NextBrain API from python',
    'long_description': "# NextBrain\nConvenient access to the [NextBrain](https://nextbrain.ai) API from python\n\n## Installation\n```bash\npip install nextbrain\n```\n\nIf you want to use the async version you need to install `asyncio` and `aiohttp`:\n\n```bash\npip install asyncio aiohttp\n```\n\n## Normal usage\n\n### All steps in one.\n```python\nfrom nextbrain import NextBrain\nfrom typing import Any, List\n\ndef main():\n    nb = NextBrain('<YOUR-ACCESS-TOKEN-HERE>')\n\n    # You can create your custom table and predict table by your own from any source\n    table: List[List[Any]] = nb.load_csv('<PATH-TO-YOUR-TRAINING-CSV>')\n    predict_table: List[List[Any]] = nb.load_csv('<PATH-TO-YOUR-PREDICTING-CSV>')\n\n    model_id, response = nb.upload_and_predict(table, predict_table, '<YOUR-TARGET-COLUMN>')\n    # model_id is also returned in order to predict multiple times against same model\n    print(response)\n\nif __name__ == '__main__':\n    main()\n```\n\n### Step by step\n```python\nfrom nextbrain import NextBrain\nfrom typing import Any, List\n\ndef main():\n    nb = NextBrain('<YOUR-ACCESS-TOKEN-HERE>')\n\n    # You can create your custom table and predict table by your own from any source\n    table: List[List[Any]] = nb.load_csv('<PATH-TO-YOUR-TRAINING-CSV>')\n    # Upload the model to NextBrain service\n    model_id: str = nb.upload_model(table)\n    # Train the model\n    # You can re-train a previous model\n    nb.train_model(model_id, '<YOUR-TARGET-COLUMN>')\n\n    predict_table: List[List[Any]] = nb.load_csv('<PATH-TO-YOUR-PREDICTING-CSV>')\n    # You can predict multiple using the same model (don't need to create a new model each time)\n    response = nb.predict_model(model_id, predict_table[0], predict_table[1:])\n    print(response)\n\nif __name__ == '__main__':\n    main()\n```\n\n## Async usage\n\n### All steps in one.\n```python\nfrom nextbrain import AsyncNextBrain\nfrom typing import Any, List\n\nasync def main():\n    nb = AsyncNextBrain('<YOUR-ACCESS-TOKEN-HERE>')\n\n    # You can create your custom table and predict table by your own from any source\n    table: List[List[Any]] = nb.load_csv('<PATH-TO-YOUR-TRAINING-CSV>')\n    predict_table: List[List[Any]] = nb.load_csv('<PATH-TO-YOUR-PREDICTING-CSV>')\n\n    model_id, response = await nb.upload_and_predict(table, predict_table, '<YOUR-TARGET-COLUMN>')\n    # model_id is also returned in order to predict multiple times against same model\n    print(response)\n\nif __name__ == '__main__':\n    import asyncio\n    asyncio.run(main())\n```\n\n### Step by step\n```python\nfrom nextbrain import AsyncNextBrain\nfrom typing import Any, List\n\nasync def main():\n    nb = AsyncNextBrain('<YOUR-ACCESS-TOKEN-HERE>')\n\n    # You can create your custom table and predict table by your own from any source\n    table: List[List[Any]] = nb.load_csv('<PATH-TO-YOUR-TRAINING-CSV>')\n    # Upload the model to NextBrain service\n    model_id: str = await nb.upload_model(table)\n    # Train the model\n    # You can re-train a previous model\n    await nb.train_model(model_id, '<YOUR-TARGET-COLUMN>')\n\n    predict_table: List[List[Any]] = nb.load_csv('<PATH-TO-YOUR-PREDICTING-CSV>')\n    # You can predict multiple using the same model (don't need to create a new model each time)\n    response = await nb.predict_model(model_id, predict_table[0], predict_table[1:])\n    print(response)\n\nif __name__ == '__main__':\n    import asyncio\n    asyncio.run(main())\n```",
    'author': 'Softpoint Consultores S.L.',
    'author_email': 'info@softpoint.es',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'https://github.com/NextBrain-ai/nextbrain-python',
    'packages': packages,
    'package_data': package_data,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
