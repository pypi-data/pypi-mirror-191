"""setup for this project"""
import os
from setuptools import setup, find_packages

current_directory = os.path.dirname(os.path.abspath(__file__))
try:
    with open(os.path.join(current_directory, '../README.md'), encoding='utf-8') as f:
        LONG_DESCRIPTION = f.read()
except FileNotFoundError:
    LONG_DESCRIPTION = ''

setup(
    name='taxi_ops_backend',
    version='0.0.3',
    packages=find_packages(where='taxi_ops_backend',
                           include=['core', 'core.*', 'db', 'db.*', "service", "service.*"]),
    url='https://github.com/abhinavofficial/IITM-ACSEFeb22-Capstone-TaxiOps',
    license='',
    author='Group 1 - IITM-ACSE-Feb22',
    author_email='',
    description='Taxi Ops Backend for capstone project',
    long_description=LONG_DESCRIPTION,
    long_description_content_type='text/markdown',
    classifiers=[
        "Programming Language :: Python :: 3",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.8',
    package_dir={'': 'taxi_ops_backend'},
    install_requires=[
        "pymongo==4.3.3",
        "dataclasses==0.6",
        "dataclasses_json==0.5.7",
        "geojson~=3.0.0"
    ]
)
