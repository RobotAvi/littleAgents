from setuptools import setup, find_packages

setup(
    name="littleAgents",
    version="0.1.0",
    packages=find_packages(),
    install_requires=[
        "requests",
        "aiohttp",
        "pytest",
        "pytest-asyncio",
    ],
    python_requires=">=3.8",
)