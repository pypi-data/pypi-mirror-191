import setuptools
import glob

with open("README.md", "r") as fh:
    long_description = fh.read()

with open("requirements.txt", "r") as fh:
    install_requires = fh.read()


__version__ = "0.1.0"

setuptools.setup(
    name="nse_ab_quantlib",
    version=__version__,
    author="Jaskirat Singh",
    author_email="jaskiratsingh1208@gmail.com",
    description="Way of Testing option selling strategies in NSE",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/jaskirat1208/backtest-platform",
    scripts=glob.glob('main/*.py'),
    packages=setuptools.find_packages(),
    install_requires=install_requires,
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
    ],
)