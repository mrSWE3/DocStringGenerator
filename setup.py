from setuptools import setup, find_packages

setup(
    name='DocStringGenerator',
    version='1',
    packages=find_packages(),
    install_requires=[],
    entry_points={
        "console_scripts": [
            "docstrgen=DocStringGenerator.main:main",
        ],
    },
)
