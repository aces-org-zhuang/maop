#!/usr/bin/env python3
"""
setup.py - 代码仓onboard技能生成器脚本包
"""

from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="code-repo-onboard-skill-generator",
    version="1.0.0",
    author="OpenClaw Skills",
    author_email="skills@openclaw.ai",
    description="为指定代码仓生成onboard skill的工具集",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/openclaw/skills/code-repo-onboard-skill-generator",
    packages=find_packages(),
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "Topic :: Software Development :: Documentation",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.7",
    install_requires=[
        "PyYAML>=6.0",
        "Jinja2>=3.0",
        "requests>=2.28",
    ],
    entry_points={
        "console_scripts": [
            "analyze-repo=code_repo_onboard.analyze_repo:main",
            "generate-skill=code_repo_onboard.generate_skill:main",
            "validate-skill=code_repo_onboard.validate_skill:main",
        ],
    },
)