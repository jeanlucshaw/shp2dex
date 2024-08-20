from setuptools import setup, find_packages
import os

# Function to read the requirements.txt file
def read_requirements():
    with open('requirements.txt') as req_file:
        return req_file.read().splitlines()
setup(
    name='shp2dex',
    version='0.1.0',
    description='A utility for converting shapefiles to dex format',
    author='Jean-Luc Shaw',
    author_email='your-email@example.com',  # Replace with actual email
    url='https://github.com/jeanlucshaw/shp2dex',
    packages=["shp2dex"],  # Automatically finds packages in the repository
    install_requires=read_requirements(),
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.6',  # Specify the minimum Python version if necessary
)