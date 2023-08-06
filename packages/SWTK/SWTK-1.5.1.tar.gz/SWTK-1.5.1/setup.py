from setuptools import setup, find_packages
import os
import sys
setup(
    name='SWTK',
    version='1.5.1',
    description='Sort txt file from weirdest line to last from cli. Meant to be used for Logs. An experimental Unsupervised Learning Log Anomaly Detection toolkit. YOU ARE BEAUTIFUL! This will sort the input based on weirdness. Now with a malware detection feature!',
    url='https://github.com/nileshkhetrapal/SWTK',
    author='Nilesh Khetrapal',
    packages=find_packages(),
    scripts=['bin/SWTK'],
    install_requires=[
        'numpy',
        'scipy',
        'matplotlib',
        'requests',
        'argparse'])

