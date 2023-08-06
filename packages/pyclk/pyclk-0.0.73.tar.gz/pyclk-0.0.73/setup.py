import os
from setuptools import setup, find_packages

def get_version_unsafe():
  with open("reqs.yaml", "r") as f:
    lines = f.readlines()
    for id,line in enumerate(lines):
      if line.startswith("version"):
        return lines[id+1].strip().replace("\\n", "")

version = get_version_unsafe()

with open("version.py", "w") as f:
  f.write("__version__ = '{}'\n".format(version))

with open("README.md", "r") as fh:
  long_description = fh.read()


if __name__ == "__main__":
  print("Running setup.py")
  setup(
    name='pyclk',
    license='MIT',
    author='Sebastian Tuyu',
    long_description=long_description,
    long_description_content_type='text/markdown',
    author_email='contact@sebastiantuyu.com',
    keywords='monorepo cli package manger',
    description='Python package to manage monorepo cli',
    version=version,
    scripts=[
      'cli.py',
      'version.py'
    ],
    install_requires=[
      'pyyaml',
      'spinners'
    ],
    entry_points={
      'console_scripts': [
        'pyclk = cli:main'
      ]
    },
    packages=find_packages()
  )