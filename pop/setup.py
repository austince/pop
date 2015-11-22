__author__ = 'austin'

from setuptools import setup
from pip.req import parse_requirements


def readme():
    """

    :return:
    """
    with open('README.md') as f:
        return f.read()


def requirements():
    """

    :return:
    """
    install_reqs = parse_requirements('requirements.txt')
    return [str(req.req) for req in install_reqs]

setup(name='pop',
      version='0.1',
      description='Package for popping',
      long_description=readme(),
      url='http://github.com/austincawley/pop',
      author='Austin Cawley-Edwards',
      author_email='austin.cawley@gmail.com',
      license='MIT',
      packages=['pop'],
      classifiers=['Development Status :: 3 - Alpha'],
      keywords="popcorn dad",
      install_requires=requirements(),
      zip_safe=False
      )
