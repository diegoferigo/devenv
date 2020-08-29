from setuptools import setup, find_packages

setup(
  name="devenv",
  version="1.0",
  author="Diego Ferigo",
  author_email="dgferigo@gmail.com",
  description="Command line tool for high-level configuration of docker-compose",
  license="LGPL",
  platforms='any',
  python_requires='>=3.6',
  keywords="docker tool commandline container image",
  packages=find_packages(),
  url="https://github.com/diegoferigo/devenv",
  install_requires=[
    'docker',
    'PyYAML',
    'requests',
    'docker-compose',
  ],
  entry_points={
    'console_scripts': ['devenv=devenv.__main__:main'],
  },
)
