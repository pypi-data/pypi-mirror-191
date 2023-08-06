from setuptools import setup, find_packages
from pathlib import Path


__version__ = '3.0.4'

base_dir = Path(__file__).parent

setup(name='vk_maria',
      version=__version__,
      description='vk bot api framework',
      long_description=open((base_dir / 'README.rst').as_posix(), encoding='utf-8').read(),
      long_description_content_type="text/markdown",
      url='https://github.com/lxstvayne/vk_maria',
      keywords='vk bot tools',
      packages=find_packages(exclude=('tests', 'docs')),
      install_requires=[
          'requests>=2.20.1',
          'loguru>=0.5.3',
          'pydotdict>=3.3.11'
      ],
      requires_python='>=3.7',
      classifiers=[
          'Environment :: Console',
          'Programming Language :: Python :: 3.7',
          'Programming Language :: Python :: 3.8',
          'Programming Language :: Python :: 3.9',
          'Programming Language :: Python :: 3.10',
          'Topic :: Software Development :: Libraries :: Application Frameworks'
      ],
      author='lxstvayne',
      author_email='lxstv4yne@gmail.com',
      zip_safe=False)
