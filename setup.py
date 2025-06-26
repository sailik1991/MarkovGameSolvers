from setuptools import setup, find_packages

setup(
    name="MarkovGameSolvers",
    version="0.1.0",
    packages=find_packages(),
    install_requires=[
        "numpy>=1.21.0",
        "nashpy>=0.0.41",
        "pulp>=3.2.1",
        "scipy>=1.16.0",
    ],
    author="Sailik Sengupta",
    author_email="",
    description="Solvers for Markov Games",
    keywords="markov games, game theory, reinforcement learning",
    url="https://github.com/sailik1991/MarkovGameSolvers",
    python_requires=">=3.6",
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Science/Research",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
    ],
)