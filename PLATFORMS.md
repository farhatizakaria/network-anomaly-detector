# Platform Setup Guide

This project is fully compatible with **Windows**, **Linux**, and **macOS**.

Choose your platform below for detailed setup instructions:

## 🪟 Windows Setup

For detailed Windows setup instructions including Npcap installation:

👉 **[WINDOWS_SETUP.md](WINDOWS_SETUP.md)**

**Quick Summary:**
1. Install Python from [python.org](https://python.org)
2. Install Npcap from [npcap.com](https://npcap.com/) (required for packet capture)
3. Create virtual environment: `python -m venv venv`
4. Activate venv: `venv\Scripts\activate`
5. Install dependencies: `pip install -r requirements.txt`
6. Run as Administrator: `python main.py`

**Key Files:**
- `activate.bat` - Quick activation script
- `WINDOWS_SETUP.md` - Comprehensive Windows guide

## 🐧 Linux Setup

For detailed Linux setup instructions including libpcap configuration:

👉 **[LINUX_SETUP.md](LINUX_SETUP.md)**

**Quick Summary:**
1. Install Python: `sudo apt-get install python3 python3-venv`
2. Install libpcap: `sudo apt-get install libpcap-dev`
3. Create virtual environment: `python3 -m venv venv`
4. Activate venv: `source venv/bin/activate`
5. Install dependencies: `pip install -r requirements.txt`
6. Run with sudo: `sudo python main.py`

**Key Files:**
- `activate.sh` - Quick activation script
- `LINUX_SETUP.md` - Comprehensive Linux guide

## 🍎 macOS Setup

macOS is treated like Linux. Use the Linux guide but with these differences:

**Quick Summary:**
1. Install Python: `brew install python3` (or from [python.org](https://python.org))
2. Install libpcap: `brew install libpcap`
3. Create virtual environment: `python3 -m venv venv`
4. Activate venv: `source venv/bin/activate`
5. Install dependencies: `pip install -r requirements.txt`
6. Run with sudo: `sudo python main.py`

See [LINUX_SETUP.md](LINUX_SETUP.md) for detailed instructions (mostly same as Linux).

## Cross-Platform Features

The project includes several cross-platform utilities:

### 1. **Platform Detection**
```python
from anomaly_detector.platform_utils import PlatformInfo

print(PlatformInfo.get_system())  # Windows, Linux, Darwin
print(PlatformInfo.is_windows())  # True/False
print(PlatformInfo.is_linux())    # True/False
print(PlatformInfo.require_admin()) # Check for admin/root
```

### 2. **Automatic Platform Adaptation**
- Packet capture parameters automatically adjusted
- Error messages tailored to platform
- Admin privilege warnings on Windows

### 3. **Activation Scripts**
- `activate.bat` - Windows
- `activate.sh` - Linux/macOS

## Quick Comparison

| Feature | Windows | Linux | macOS |
|---------|---------|-------|-------|
| Setup | See [WINDOWS_SETUP.md](WINDOWS_SETUP.md) | See [LINUX_SETUP.md](LINUX_SETUP.md) | Use Linux guide |
| Packet Capture | Npcap required | libpcap required | libpcap (via brew) |
| Activation | `venv\Scripts\activate` | `source venv/bin/activate` | `source venv/bin/activate` |
| Run Detector | `python main.py` (as Admin) | `sudo python main.py` | `sudo python main.py` |
| Interface Example | `Ethernet`, `Wi-Fi` | `eth0`, `wlan0` | `en0`, `en1` |
| Setup Time | ~15 minutes | ~10 minutes | ~10 minutes |

## Troubleshooting by Platform

### Windows Issues?
→ See [WINDOWS_SETUP.md #Troubleshooting](WINDOWS_SETUP.md#troubleshooting)

### Linux Issues?
→ See [LINUX_SETUP.md #Troubleshooting](LINUX_SETUP.md#troubleshooting)

### Common Issues (All Platforms)

| Issue | Solution |
|-------|----------|
| "Permission Denied" | Use sudo (Linux/macOS) or run as Admin (Windows) |
| "No module named X" | Activate venv with `pip install -r requirements.txt` |
| "Network interface not found" | List interfaces in Python or with system tools |
| "Can't find Npcap/libpcap" | Install from [npcap.com](https://npcap.com) or `apt-get` |

## Getting Started (All Platforms)

1. **Read QUICKSTART.md** for quick reference
2. **Read platform-specific guide**:
   - Windows → [WINDOWS_SETUP.md](WINDOWS_SETUP.md)
   - Linux/macOS → [LINUX_SETUP.md](LINUX_SETUP.md)
3. **Create and activate venv**
4. **Install dependencies**: `pip install -r requirements.txt`
5. **Run examples**: `python examples.py 1-6`
6. **Run detector**: `python main.py` (with appropriate privileges)

## System Requirements

### Minimum
- Python 3.7+
- 2GB RAM
- 100MB disk space
- Network interface

### Recommended
- Python 3.10+
- 4GB RAM
- 500MB disk space
- Privileged access (admin/root)

## File Structure

```
├── anomaly_detector/
│   ├── __init__.py
│   ├── detector.py          # Main detector
│   ├── packet_analyzer.py   # Packet capture
│   ├── loop_detector.py     # Loop detection
│   ├── loss_detector.py     # Loss detection
│   ├── latency_detector.py  # Latency detection
│   └── platform_utils.py    # Cross-platform utilities ⭐
├── tests/
│   ├── __init__.py
│   └── test_detectors.py
├── main.py                   # CLI entry point
├── examples.py              # Usage examples
├── config.py                # Configuration
├── activate.bat             # Windows activation ⭐
├── activate.sh              # Linux/macOS activation ⭐
├── WINDOWS_SETUP.md         # Windows guide ⭐
├── LINUX_SETUP.md           # Linux guide ⭐
├── QUICKSTART.md            # Quick reference
├── README.md                # Full documentation
├── requirements.txt         # Dependencies
└── setup.py                 # Package setup
```

## Next Steps

1. **Choose your platform** above
2. **Follow the setup guide** for your OS
3. **Run examples**: `python examples.py 1`
4. **Read documentation**: Check README.md
5. **Customize config**: Edit config.py for your needs

## Support

- **Windows Users**: Check [WINDOWS_SETUP.md](WINDOWS_SETUP.md)
- **Linux/macOS Users**: Check [LINUX_SETUP.md](LINUX_SETUP.md)
- **Quick Questions**: Check [QUICKSTART.md](QUICKSTART.md)
- **Full Documentation**: Check [README.md](README.md)

---

**Status**: ✅ Fully cross-platform compatible
**Last Updated**: March 5, 2026
