import sys
from setuptools import setup, find_packages

setup(
    name="pb-amarder",
    version='0.2.5',
    author='Alex Marder',
    # author_email='notlisted',
    description="Custom progress status, primarily for iterators.",
    url="https://gitlab.com/alexander_marder/pb-amarder",
    packages=find_packages(),
    zip_safe=False,
    include_package_data=True,
    python_requires='>3.6'
)
