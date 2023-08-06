"""setup for this project"""
import os
from setuptools import setup, find_packages

current_directory = os.path.dirname(os.path.abspath(__file__))
print(f"current directory is {current_directory}")
try:
    with open(os.path.join(current_directory, 'README.md'), encoding='utf-8') as f:
        LONG_DESCRIPTION = f.read()
        print(LONG_DESCRIPTION)
except FileNotFoundError:
    LONG_DESCRIPTION = ''

packages_to_install = find_packages()
print(packages_to_install)

setup(
    name='taxi_ops_backend',
    version='0.0.7',
    packages=packages_to_install,
    url='https://github.com/abhinavofficial/IITM-ACSEFeb22-Capstone-TaxiOps',
    license='',
    author='Abhinav Kumar',
    author_email='apache.abhinav.official@outlook.com',
    description='Taxi Ops Backend for capstone project',
    long_description=LONG_DESCRIPTION,
    long_description_content_type='text/markdown',
    classifiers=[
        "Programming Language :: Python :: 3",
        "Operating System :: OS Independent",
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
    ],
    python_requires='>=3.8',
    # package_dir={'': 'taxi_ops_backend'},
    install_requires=[
        "pymongo==4.3.3",
        "dataclasses==0.6",
        "dataclasses_json==0.5.7",
        "geojson~=3.0.0"
    ]
)
