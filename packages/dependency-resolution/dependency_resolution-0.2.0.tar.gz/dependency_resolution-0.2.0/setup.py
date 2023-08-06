# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['dependency_resolution']

package_data = \
{'': ['*']}

setup_kwargs = {
    'name': 'dependency-resolution',
    'version': '0.2.0',
    'description': 'A simple dependency resolution library using container concepts',
    'long_description': '# Dependency Resolution\n\n## How to use\n\n```python\nfrom dependency_resolution import ProviderCache\n\nclass Image:\n  def __init__(self, file: str):\n    self.file = file\n\n\nclass ImageProcessor:\n  def __init__(self, image: Image):\n    self.image = image\n\n  def sharpen(self):\n    pass\n\n\ndef init_image():\n  instance = ProviderCache.get_instance()\n  instance += Image("image.png")\n  # Can also be done like this\n  # instance[Image] = Image("image.png")\n\n\ndef init_processor():\n  instance = ProviderCache.get_instance()\n  instance += ImageProcessor(instance[Image])\n\n\ndef process_image():\n  instance = ProviderCache.get_instance()\n  processor = instance[ImageProcessor]\n  processor.sharpen()\n\n\nif __name__ == "__main__":\n  init_image()\n  init_processor()\n  process_image()\n```\n\n## Future Plans\n\n- [ ] Add autowire support\n- [ ] Add Providers to pass specific arguments to the constructor\n',
    'author': 'Saroopashree K',
    'author_email': 'saroopa25@gmail.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'packages': packages,
    'package_data': package_data,
    'python_requires': '>=3.8.0,<4.0.0',
}


setup(**setup_kwargs)
