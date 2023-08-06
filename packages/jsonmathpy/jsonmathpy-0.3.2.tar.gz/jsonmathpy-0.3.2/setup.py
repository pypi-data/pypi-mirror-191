from setuptools import setup, find_packages

setup(
    name='jsonmathpy',
    version='0.3.2',
    packages=find_packages(include=["src"]),
    description='A package used to parse strings into math json objects.',
    author='Ashley Cottrell',
    author_email='cottrellashley@gmail.com',
    install_requires=['regex', 'more_itertools', 'numpy', 'sympy']
)