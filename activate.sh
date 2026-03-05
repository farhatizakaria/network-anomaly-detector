#!/bin/bash
# Virtual Environment Activation Script for Linux/macOS
# Run this script to activate the virtual environment

echo "Activating virtual environment..."
source venv/bin/activate

echo "Virtual environment activated!"
echo ""
echo "You can now run the Network Anomaly Detector:"
echo "  - For detection:  python main.py (use 'sudo' for packet capture)"
echo "  - For examples:   python examples.py 1"
echo "  - For tests:      python -m unittest tests.test_detectors"
echo ""
