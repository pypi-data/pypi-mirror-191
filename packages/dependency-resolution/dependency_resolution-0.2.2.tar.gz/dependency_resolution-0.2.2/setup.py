# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['dependency_resolution']

package_data = \
{'': ['*']}

setup_kwargs = {
    'name': 'dependency-resolution',
    'version': '0.2.2',
    'description': 'A simple dependency resolution library using container concepts',
    'long_description': '# Dependency Resolution\n\n## How to use\n\n### ProviderCache Usage\n\nWhen autowiring is not required use ProviderCache for a simple implementation.\n\nBecause autowiring is not involved there are algorithms to determine the order of initialization. And therefore ProviderCache is faster.\n\n```python\nfrom dependency_resolution import ProviderCache\n\nclass Image:\n  def __init__(self, file: str):\n    self.file = file\n\nclass ImageProcessor:\n  def __init__(self, image: Image):\n    self.image = image\n\n  def sharpen(self):\n    pass\n\ndef init_image():\n  cache = ProviderCache.get_instance()\n  cache += Image("image.png")\n  # Can also be done like this\n  # cache[Image] = Image("image.png")\n\ndef init_processor():\n  cache = ProviderCache.get_instance()\n  cache += ImageProcessor(cache[Image])\n\ndef process_image():\n  cache = ProviderCache.get_instance()\n  processor = cache[ImageProcessor]\n  processor.sharpen()\n\nif __name__ == "__main__":\n  init_image()\n  init_processor()\n  process_image()\n```\n\n### AutoWiredCache Usage\n\nWhen autowiring is required use AutoWiredCache.\n\nAutoWiredCaches accept just the types of the dependencies and will automatically resolve them (given required deps are already present in the Cache or can be created using other deps).\n\n```python\nfrom dependency_resolution import AutoWiredCache\n\nclass ImageDriver:\n  def __init__(self, proc: ImageProcessor, image: Image):\n    self.proc = proc\n    self.image = image\n\n  def edit_and_save(self):\n    pass\n\ndef init_image():\n  cache = AutoWiredCache.get_instance()\n  cache += Image("image.png")\n  # Can also be done like this\n  # cache[Image] = Image("image.png")\n\ndef init_processor_and_driver():\n  cache = AutoWiredCache.get_instance()\n  cache += ImageProcessor\n  cache += ImageDriver\n\ndef process_image():\n  cache = AutoWiredCache.get_instance()\n  driver = cache[ImageDriver]\n  driver.edit_and_save()\n\nif __name__ == "__main__":\n  init_image()\n  init_processor()\n  process_image()\n```\n\n`AutoWiredContainer` also supports lazy evaluation of dependencies. When a new type is added to the cache, it is not initialized immediately and as a result any missing deps will be ignored at that moment.\n\nTherefore, `init_processor_and_driver` function from the above example can be as follows\n\n```python\ndef init_processor_and_driver():\n  cache = AutoWiredCache.get_instance()\n  cache += ImageDriver\n  cache += ImageProcessor\n```\n\nWhen the `ImageDriver` object is obtained from the cache (`cache[ImageDriver]`), the `ImageProcessor` object will be created first following which the `ImageDriver` object will be created.\n\n## Future Plans\n\n- [x] Add autowire support\n- [ ] Add Providers to pass specific arguments to the constructor\n- [ ] Add support for deleting or removing provided instances in both `ProviderCache` and `AutoWiredCache`\n',
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
