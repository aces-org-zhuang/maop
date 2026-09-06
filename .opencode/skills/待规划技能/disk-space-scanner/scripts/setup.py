#!/usr/bin/env python3
"""
Setup script for disk-space-scanner Python CLI tool
"""

from setuptools import setup, find_packages

setup(
    name='disk_space_scanner',
    version='1.0.0',
    description='Disk space scanner and analyzer',
    author='OpenClaw',
    author_email='openclaw@example.com',
    packages=find_packages(),
    package_data={
        'disk_space_scanner': ['*.py'],
    },
    install_requires=[
        'click>=8.0.0',
    ],
    entry_points={
        'console_scripts': [
            'disk-space-scanner=disk_space_scanner.disk_space_scanner:cli',
        ],
    },
    classifiers=[
        'Development Status :: 4 - Beta',
        'Intended Audience :: System Administrators',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.7+',
    ],
    python_requires='>=3.7',
)
