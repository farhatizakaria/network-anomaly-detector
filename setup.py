"""Setup configuration for Network Anomaly Detector."""

from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="network-anomaly-detector",
    version="2.0.0",
    author="Network Monitoring Team",
    description="Modern TUI/CLI tool for detecting network anomalies including loops, packet loss, and latency issues",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/yourusername/network-anomaly-detector",
    packages=find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Operating System :: Microsoft :: Windows",
        "Operating System :: POSIX :: Linux",
        "Operating System :: MacOS",
        "Topic :: System :: Networking :: Monitoring",
        "Development Status :: 4 - Beta",
        "Environment :: Console",
    ],
    python_requires=">=3.7",
    install_requires=[
        "scapy>=2.5.0",
        "numpy>=1.21.0",
        "pandas>=1.3.0",
        "scipy>=1.7.0",
        "psutil>=5.9.0",
        "rich>=13.0.0",
        "typer>=0.9.0",
        "questionary>=2.0.0",
    ],
    entry_points={
        "console_scripts": [
            "network-anomaly-detector=main:app",
        ],
    },
)
