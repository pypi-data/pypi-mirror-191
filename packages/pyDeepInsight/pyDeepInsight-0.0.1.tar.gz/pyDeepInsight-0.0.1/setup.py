from setuptools import setup, find_packages

from pyDeepInsight import __version__


with open("README.md", "r") as fh:
    long_description = fh.read()
with open("requirements.txt", "r") as fh:
    requirements = [line.strip() for line in fh]

setup(
    name="pyDeepInsight",
    version=__version__,
    description="Package implementing DeepInsight paper",
    project_urls={
        "Source": "https://www.nature.com/articles/s41598-019-47765-6",
        ## Not yet documentation
        # "Documentation": "https://bbatardiere.pages.mia.inra.fr/pyplnmodels/index.html",
    },
    author="Bastien Batardière",
    author_email="bastien.batardiere@gmail.com",
    long_description=long_description,
    packages=find_packages(),
    python_requires=">=3",
    keywords=[
        "python",
        "image",
        "data",
        "image to data",
        "convolutional neural network",
        "scRNAseq",
    ],
    install_requires=requirements,
    py_modules=[
        "pyDeepInsight.scaler",
        "pyDeepInsight.transformer",
    ],
    long_description_content_type="text/markdown",
    license="MIT",
    # See https://pypi.python.org/pypi?%3Aaction=list_classifiers
    classifiers=[
        # How mature is this project? Common values are
        #   3 - Alpha
        #   4 - Beta
        #   5 - Production/Stable
        "Development Status :: 3 - Alpha",
        # Indicate who your project is intended for
        "Intended Audience :: Science/Research",
        # Pick your license as you wish (should match "license" above)
        "License :: OSI Approved :: MIT License",
        # Specify the Python versions you support here. In particular, ensure
        # that you indicate whether you support Python 2, Python 3 or both.
        "Programming Language :: Python :: 3 :: Only",
    ],
)
