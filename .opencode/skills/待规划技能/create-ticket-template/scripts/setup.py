#!/usr/bin/env python3
"""
Ticket Template IPO - Setup
"""

from setuptools import setup, find_packages

setup(
    name="ticket-template-ipo",
    version="1.0.0",
    description="Ticket template creation tool with IPO structure",
    packages=find_packages(),
    python_requires=">=3.7",
    entry_points={
        "console_scripts": [
            "ticket-template-ipo=ticket_template_ipo.main:main",
        ],
    },
)
