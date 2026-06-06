from setuptools import setup, find_packages

setup(
    name="agentsentry",
    version="0.1.0",
    description="Audit AI agent config files for dangerous permissions and risky tool combinations",
    author="Nandini Bhuva",
    packages=find_packages(),
    install_requires=[
        "rich>=13.0.0",
        "pyyaml>=6.0",
    ],
    entry_points={
        "console_scripts": [
            "agentsentry=agentsentry.cli:main",
        ],
    },
    python_requires=">=3.9",
)
