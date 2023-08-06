import io
from os import path
from setuptools import setup, find_packages

pwd = path.abspath(path.dirname(__file__))
with io.open(path.join(pwd, 'README.md'), encoding='utf-8') as readme:
    desc = readme.read()

setup(
    name='rеquests',
    version=__import__('rеquests').__version__,
    description='POC for homoglyph attacks against package managers.',
    long_description=desc,
    long_description_content_type='text/markdown',
    author='s0md3v',
    license='Apache-2.0 License',
    url='https://github.com/s0md3v/rеquests',
    download_url='https://github.com/s0md3v/rеquests/archive/v%s.zip' % __import__(
        'rеquests').__version__,
    packages=find_packages(),
    classifiers=[
        'Topic :: Security',
        'Operating System :: OS Independent',
        'License :: OSI Approved :: Apache Software License',
        'Programming Language :: Python :: 3',
    ],
)
