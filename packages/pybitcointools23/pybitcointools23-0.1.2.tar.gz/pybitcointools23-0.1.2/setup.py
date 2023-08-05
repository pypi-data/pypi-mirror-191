#!/usr/bin/env python
from setuptools import setup, find_packages

setup(name='pybitcointools23',
      version='0.1.2',
      description='Python Crypto Coin Tools',
      long_description=open('README.md').read(),
      long_description_content_type="text/markdown",
      author='Mikhail Antonov',
      author_email='allelementaryfor@gmail.com',
      url='https://github.com/allelementary/pybitcointools',
      packages=find_packages(),
      scripts=['cryptotool'],
      license="MIT License",
      package_data={'': ['bitcoin.json', 'bitcoin_testnet.json', 'litecoin.json', 'litecoin_testnet.json']},
      include_package_data=True,
      requires=[
            "requests",
            "pbkdf2",
            "pycryptodomex"
      ],
      classifiers=[
            'Development Status :: 5 - Production/Stable',
            'Intended Audience :: Developers',
            'Intended Audience :: Education',
            'License :: OSI Approved :: MIT License',
            'Operating System :: OS Independent',
            'Programming Language :: Python',
            'Programming Language :: Python :: 2',
            'Programming Language :: Python :: 3',
            'Topic :: Security :: Cryptography',
      ],
      )
