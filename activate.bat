@echo off
REM Virtual Environment Activation Script for Windows
REM Run this script to activate the virtual environment

echo Activating virtual environment...
call venv\Scripts\activate.bat

echo Virtual environment activated!
echo.
echo You can now run the Network Anomaly Detector:
echo   - For detection:  python main.py
echo   - For examples:   python examples.py 1
echo   - For tests:      python -m unittest tests.test_detectors
echo.
echo Note: Run Command Prompt as Administrator for packet capture!
echo.
cmd /k
