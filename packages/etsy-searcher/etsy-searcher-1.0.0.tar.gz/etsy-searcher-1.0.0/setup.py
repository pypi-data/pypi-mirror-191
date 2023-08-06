import setuptools
from setuptools import find_packages

setuptools.setup(
    name="etsy-searcher",
    version="1.0.0",
    author="Esat Yılmaz",
    author_email="esatyilmaz3500@gmail.com",
    description="Etsy Search API",
    packages=find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3.9",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.9',
    install_requires=[
        "pydantic", "requests"
    ]
)
