from os import path

from setuptools import setup

this_directory = path.abspath(path.dirname(__file__))
with open(path.join(this_directory, 'readme.md'), encoding='utf-8') as f:
    long_description = f.read()

setup(
    name='u-trainer',
    version='1.0.9',
    packages=['utrainer'],
    url='https://github.com/geasyheart/u-trainer',
    license='MIT',
    author='yuzhang',
    author_email='geasyheart@163.com',
    description='trainer',
    long_description=long_description,
    long_description_content_type='text/markdown',
)
