from setuptools import setup, find_packages


setup(
    name="tech-link-finder",
    version="1.0.1",
    description="Minimal tech link discovery CLI (HN + GitHub)",
    author="OpenClaw Team",
    packages=find_packages(),
    python_requires=">=3.9",
    install_requires=[
        "requests>=2.31.0",
    ],
    entry_points={
        "console_scripts": [
            "tech-link-finder=tech_link_finder.cli:main",
        ]
    },
)
