from setuptools import setup

short_description = "A Python package for analyzing images using Caffe and Yahoo's open_nsfw models."

with open("README.md") as f:
    long_description = f.read()

setup(
    name="nsfw",
    version="0.3.0",
    description=short_description,
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/jgarber623/python-nsfw",
    author="Jason Garber",
    author_email="jason@sixtwothree.org",
    license="MIT",
    entry_points={
        'console_scripts': [
            'nsfwcheck = nsfw.cli:check',
        ]
    },

    classifiers=[
        "Development Status :: 4 - Beta",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Topic :: Multimedia :: Graphics",
        "Topic :: Scientific/Engineering :: Image Recognition",
        "Topic :: Utilities",
    ],
    packages=["nsfw"],
    python_requires=">=3",
    platforms=["any"],
)
