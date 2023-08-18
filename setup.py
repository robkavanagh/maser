from setuptools import setup, find_packages
import os
import codecs
import re
long_description = 'Python package to simulate electron cyclotron maser instability emission from exoplanets and stars.'

here = os.path.abspath(os.path.dirname(__file__))


def read(*parts):
    with codecs.open(os.path.join(here, *parts), 'r') as fp:
        return fp.read()


def find_version(*file_paths):
    version_file = read(*file_paths)
    version_match = re.search(r"^__version__ = ['\"]([^'\"]*)['\"]", version_file, re.M)
    if version_match:
        return version_match.group(1)
    raise RuntimeError("Unable to find version string.")


# DEPENDENCIES
# 1. What are the required dependencies?
with open('requirements.txt') as f:
    install_requires = f.read().splitlines()
# 2. What dependencies required to run the unit tests? (i.e. `pytest --remote-data`)
tests_require = ['pytest', 'pytest-cov', 'pytest-remotedata']

setup(name='maser',
      version=find_version("src", "maser", "__init__.py"),
      description='Python package to simulate electron cyclotron maser instability emission from exoplanets and stars.',
      long_description=long_description,
      author='Rob Kavanagh',
      author_email='kavanagh@astron.nl',
      url='https://github.com/robkavanagh/maser',
      package_dir={'': 'src'},
      packages=find_packages(where='src'),
      package_data={},
      include_package_data=False,
      install_requires=install_requires,
      tests_require=tests_require,
      extras_require={'tests': tests_require},
      license='MIT',
      classifiers=[
          "Topic :: Scientific/Engineering",
          "Intended Audience :: Science/Research",
          "Intended Audience :: Developers",
          "Development Status :: 4 - Beta",
          "License :: OSI Approved :: MIT License",
          "Operating System :: OS Independent",
          "Programming Language :: Python"
      ]
      )