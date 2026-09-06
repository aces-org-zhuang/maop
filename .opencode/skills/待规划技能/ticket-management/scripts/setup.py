from setuptools import setup, find_packages

setup(
    name="ticket-management-cli",
    version="2.0.0",
    description="完整工单管理系统命令行工具，支持6种工单类型和AI技能集成",
    author="OpenClaw Team",
    author_email="team@openclaw.ai",
    packages=find_packages(),
    package_dir={'': '.'},
    python_requires=">=3.7",
    install_requires=[
        "argparse>=1.4.0",
        "pathlib>=1.0.0",
    ],
    entry_points={
        "console_scripts": [
            "ticket-cli=ticket_management.cli_simple:main",
        ],
    },
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
    ],
    keywords="ticket-management, workflow, ai-skills, automation, productivity",
)