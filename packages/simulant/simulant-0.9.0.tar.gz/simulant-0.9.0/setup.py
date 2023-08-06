from setuptools import setup, find_packages

with open("README.md", "r") as readme_file:
    readme = readme_file.read()

requirements = ["Pillow", "Xlib", "numpy", "opencv-python",]

setup(
    name="simulant",
    version="0.9.0",
    author="zavx0z",
    author_email="zavx0z@yahoo.com",
    description="A package emulating human",
    long_description=readme,
    long_description_content_type="text/markdown",
    url="https://bitbucket.org/zavx0z/simulant",
    packages=find_packages(),
    install_requires=requirements,
    classifiers=[
        "Programming Language :: Python :: 3.10",
        "License :: OSI Approved :: GNU General Public License v3 (GPLv3)",
    ],
)
