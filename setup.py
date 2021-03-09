  
import setuptools
import os

with open("README.md", "r") as fh:
    long_description = fh.read()

version = os.environ.get("VERSION","0.0.0")
setuptools.setup(
    name="fast-pony-crud", # Replace with your own username
    version=version,
    author="MakeHax",
    author_email="info@makehax.com",
    description="Tool for creating crud routes from pony database object",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/juanborbon93/fast_pony_crud",
    packages=setuptools.find_packages(),
    install_requires=[
        "pony==0.7.14",
        "pydantic==1.8",
        "fastapi==0.63.0"
    ],
    classifiers=[
        "Programming Language :: Python :: 3",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.7',
)