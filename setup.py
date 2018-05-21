from setuptools import setup

short_description = "A Python package for analyzing images using Caffe and Yahoo's open_nsfw models."

with open("README.md") as f:
    long_description = f.read()

setup(
    name="nsfw",
    version="0.3.2",
    description=short_description,
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/jgarber623/python-nsfw",
    author="Jason Garber",
    author_email="jason@sixtwothree.org",
    license="MIT",
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
    package_data={
        "nsfw": [
            "deploy.prototxt",
            "resnet_50_1by2_nsfw.caffemodel",
        ]
    },
    entry_points={
        "console_scripts": [
            "nsfwcheck = nsfw.cli:check",
        ]
    },
    platforms=["any"],
)
