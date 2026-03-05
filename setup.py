"""Setup configuration for Network Anomaly Detector."""

from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="network-anomaly-detector",
    version="1.0.0",
    author="Network Monitoring Team",
    description="Detect network anomalies including loops, packet loss, and latency issues",
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
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Topic :: System :: Networking :: Monitoring",
        "Development Status :: 4 - Beta",
    ],
    python_requires=">=3.7",
    install_requires=[
        "scapy>=2.5.0",
        "numpy>=1.21.0",
        "pandas>=1.3.0",
        "matplotlib>=3.4.0",
        "scipy>=1.7.0",
        "pyyaml>=5.4.0",
    ],
    entry_points={
        "console_scripts": [
            "network-anomaly-detector=anomaly_detector.detector:main",
        ],
    },
)
