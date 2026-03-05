
# Windows Setup Guide

This guide provides detailed instructions for setting up the Network Anomaly Detector on Windows.

## Prerequisites

### 1. Python Installation

1. Download Python from [python.org](https://www.python.org/downloads/)
2. Run the installer
3. **IMPORTANT**: Check "Add Python to PATH" during installation
4. Click "Install Now"

### 2. No External Tools Required! ✨

Unlike traditional packet capture tools, this detector uses **pure Python libraries**. 
**No Npcap, Wireshark, or any external tools needed!**

The detector will work out-of-the-box on Windows using only:
- Python standard library (socket, threading, os, subprocess)
- psutil (pure Python network monitoring)
- No system dependencies

## Project Setup

### Step 1: Create Project Directory

Open Command Prompt and create a directory for the project:

```cmd
mkdir %USERPROFILE%\Networking
cd %USERPROFILE%\Networking
```

### Step 2: Clone/Download the Project

Copy the anomaly_detector project files into this directory. You should have:
```
- anomaly_detector\
- tests\
- main.py
- examples.py
- requirements.txt
- activate.bat
- ... (other files)
```

### Step 3: Create Virtual Environment

```cmd
python -m venv venv
```

This creates a `venv` folder containing the isolated Python environment.

### Step 4: Activate Virtual Environment

```cmd
venv\Scripts\activate
```

Or simply double-click:
```
activate.bat
```

You should see `(venv)` at the start of your command prompt line.

### Step 5: Install Dependencies

```cmd
pip install -r requirements.txt
```

This will install:
- scapy (packet manipulation)
- numpy (numerical analysis)
- scipy (scientific computing)
- pandas (data analysis)
- matplotlib (visualization)
- pyyaml (configuration)

## Running the Detector

### Simple Usage (No Administrator Mode Needed!) ✨

The detector uses **pure Python**, so you don't need Administrator mode for basic monitoring:

```cmd
# Activate virtual environment
venv\Scripts\activate

# Run detector
python main.py

# Specify a network interface (optional)
python main.py --interface "Ethernet"

# Custom timeout
python main.py --timeout 20

# View all options
python main.py --help
```

### Finding Your Network Interface Name

To see available network interfaces:

```cmd
python -c "from anomaly_detector import PurePythonMonitor; m = PurePythonMonitor(); print(m.get_available_interfaces())"
```

Common interface names on Windows:
- `Ethernet`
- `Wi-Fi` 
- `Local Area Connection`
- `Wireless Network Connection`

## List of Common Windows Network Interfaces

| Interface Name | Description |
|---|---|
| Ethernet | Wired connection |
| Wi-Fi | Wireless connection |
| VirtualBox Host-Only Network | Virtual machine interface |
| Loopback | Local machine only |

## Examples

Run various examples:

```cmd
# Basic detection
python examples.py 1

# Custom interface
python examples.py 2

# Custom thresholds
python examples.py 3

# Detailed analysis
python examples.py 4

# Continuous monitoring
python examples.py 5

# Severity filtering
python examples.py 6
```

## Running Tests

```cmd
python -m unittest tests.test_detectors
```

## Troubleshooting

### Issue: "Permission Denied" or "You do not have sufficient privilege"

**Solution**: Run Command Prompt as Administrator (see "Administrator Mode Required" section above)

### Issue: "No module named 'psutil'"

**Solution**: Make sure virtual environment is activated and psutil is installed:
```cmd
venv\Scripts\activate
pip install psutil
```

### Issue: Network interface not found

**Solution**: List available interfaces:
```cmd
python -c "from anomaly_detector import PurePythonMonitor; m = PurePythonMonitor(); print(m.get_available_interfaces())"
```

Then use the correct interface name with `--interface` parameter.

### Issue: "python: command not found" or "'python' is not recognized"

**Solution**: Python was not added to PATH during installation. Either:

1. Download and reinstall Python, making sure to check "Add Python to PATH"
2. Or use the full path: `C:\Users\YourUsername\AppData\Local\Programs\Python\Python313\python.exe`

### Issue: Virtual environment won't activate

**Solution**: Make sure you're in the correct directory and use:
```cmd
venv\Scripts\activate.bat
```

Not:
```cmd
source venv\bin\activate  (This is for Linux/macOS)
```

### Issue: psutil returns error on some systems

**Solution**: Update psutil:
```cmd
pip install --upgrade psutil
```

## Useful Commands

```cmd
# Activate virtual environment
venv\Scripts\activate

# Deactivate virtual environment
deactivate

# List installed packages
pip list

# Update a package
pip install --upgrade scapy

# Uninstall and reinstall all requirements
pip uninstall -r requirements.txt -y
pip install -r requirements.txt

# Check Python version
python --version

# Check pip version
pip --version
```

## Advanced: Setting up Windows Terminal

If you prefer Windows Terminal (modern UI):

1. Download from Microsoft Store
2. Open Settings (Ctrl + ,)
3. Go to "Default Profile" and select PowerShell or Command Prompt
4. Create an admin profile for easy admin access

Then you can right-click and "Run as Administrator" from Windows Terminal.

## Next Steps

- Read [QUICKSTART.md](QUICKSTART.md) for quick reference
- Read [README.md](README.md) for detailed documentation
- Run `python examples.py` to see usage examples
- Check `config.py` to customize detection parameters

## Getting Help

If you encounter issues:

1. Check the [Troubleshooting](#troubleshooting) section above
2. Verify Npcap is installed: [npcap.com](https://npcap.com/)
3. Make sure you're running as Administrator
4. Check that all files were extracted correctly
5. Try reinstalling the virtual environment:
   ```cmd
   rmdir /s venv
   python -m venv venv
   venv\Scripts\activate
   pip install -r requirements.txt
   ```

---

**Last Updated**: March 5, 2026
**Python Version**: 3.10+
**Npcap Version**: 1.70+
