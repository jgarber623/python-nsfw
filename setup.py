from setuptools import setup

short_description = 'A Python package for analyzing images using Caffe and Yahoo’s open_nsfw models.'

with open('README.md') as f:
    long_description = f.read()

setup(
    name='nsfw',
    version='0.1.0',
    description=short_description,
    long_description=long_description,
    long_description_content_type='text/markdown',
    url='https://github.com/jgarber623/python-nsfw',
    author='Jason Garber',
    author_email='jason@sixtwothree.org',
    license='MIT',
    packages=['nsfw'],
    python_requires='>=3',
    platforms=['any'],
)
