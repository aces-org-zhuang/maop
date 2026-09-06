from setuptools import setup, find_packages

setup(
    name="skill-trigger-tester",
    version="1.0.0",
    packages=find_packages(),
    python_requires=">=3.7",
    install_requires=[
        # Add any dependencies here if needed
    ],
    entry_points={
        "console_scripts": [
            "skill-trigger-test=skill_trigger_tester.cli.main:main",
        ],
    },
)
