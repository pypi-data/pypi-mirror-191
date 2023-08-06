from setuptools import setup
import pathlib

dirParent = pathlib.Path(__file__).parent.resolve()

long_description = (dirParent / "README.md").read_text(encoding="utf-8")

setup(
      # name package
      name='expp',

      # version pakage
      version='1.0.1',

      # short description package
      description='The Extension Pure Python',

      long_description=long_description,

      packages=['expp'],

      author='XXIMDE',
      author_email='xximde@gmail.com',

      license='MIT',

      classifiers=[

      'Development Status :: 3 - Alpha',

      'Intended Audience :: Developers',
      'Topic :: Software Development :: Build Tools',

      'License :: OSI Approved :: MIT License',

      'Programming Language :: Python :: 2.7',
      'Programming Language :: Python :: 3',
      'Programming Language :: Python :: 3.6',
      'Programming Language :: Python :: 3.7',
      'Programming Language :: Python :: 3.8',
      'Programming Language :: Python :: 3.9',
      'Programming Language :: Python :: 3.10',

      ],

      keywords='extended pure development',

      zip_safe=False)
