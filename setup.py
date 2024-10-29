from setuptools import setup, find_packages

with open("requirements.txt") as f:
    install_requires = f.read().splitlines()

setup(
    name="terra_lab",
    version="0.1",
    packages=find_packages(),
    install_requires=install_requires, 
    entry_points={
        "console_scripts": [
            "terra_lab=terra_lab.main:main",
        ],
    },
)
