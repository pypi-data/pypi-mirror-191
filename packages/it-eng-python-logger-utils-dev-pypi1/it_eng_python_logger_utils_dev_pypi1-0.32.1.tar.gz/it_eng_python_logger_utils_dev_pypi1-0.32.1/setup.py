from setuptools import find_packages, setup

with open("README.md", "r") as fh:
    long_description = fh.read()

setup(
    name="it_eng_python_logger_utils_dev_pypi1",
    version="0.32.1",
    author="Dinnermonster",
    author_email="it-engineering@github.com",
    description="A logger util helper for Azure app insights and structured logging",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/it-eng-packages/packages/it_eng_python_logger_utils",
    packages=['it_eng_python_logger_utils_dev_pypi1'],

    install_requires=[
        "opencensus-ext-requests",
        "opencensus-ext-azure",
        "requests",
    ],
    classifiers=[
        "Programming Language :: Python :: 3.7",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.7',
)
