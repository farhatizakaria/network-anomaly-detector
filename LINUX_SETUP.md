# Linux Setup Guide

This guide provides detailed instructions for setting up the Network Anomaly Detector on Linux.

## Prerequisites

### System Requirements

- Linux operating system (Ubuntu, Debian, Fedora, CentOS, etc.)
- Python 3.7 or higher
- Root/sudo access for packet capture
- libpcap development libraries

## Installation Steps

### Step 1: Install Python and Dependencies

#### Ubuntu/Debian:

```bash
# Update package manager
sudo apt-get update
sudo apt-get upgrade

# Install Python and pip
sudo apt-get install python3 python3-pip python3-venv

# Install libpcap (required for Scapy)
sudo apt-get install libpcap-dev

# Optional but useful
sudo apt-get install git
```

#### Fedora/CentOS/RHEL:

```bash
# Update package manager
sudo dnf update

# Install Python and pip
sudo dnf install python3 python3-pip

# Install libpcap (required for Scapy)
sudo dnf install libpcap-devel

# Optional but useful
sudo dnf install git
```

### Step 2: Create Project Directory

```bash
# Create directory
mkdir -p ~/Coding/Networking
cd ~/Coding/Networking
```

If you're cloning from git:

```bash
git clone https://github.com/yourusername/network-anomaly-detector.git
cd network-anomaly-detector
```

### Step 3: Create Virtual Environment

```bash
# Create virtual environment
python3 -m venv venv

# Activate virtual environment
source venv/bin/activate

# Or use the simple script
bash activate.sh
```

You should see `(venv)` at the start of your command prompt.

### Step 4: Install Dependencies

```bash
# Upgrade pip
pip install --upgrade pip setuptools wheel

# Install all requirements
pip install -r requirements.txt
```

## Running the Detector

### Method 1: Using sudo (Recommended)

```bash
# First, activate venv if not already activated
source venv/bin/activate

# Run detector with sudo
sudo python main.py

# Note: You might need to deactivate first if you get permission issues
# deactivate
# sudo python main.py
```

### Method 2: Using Capabilities (Advanced)

For repeated use without typing sudo, grant Python specific capabilities:

```bash
# One-time setup
sudo setcap cap_net_raw,cap_net_admin=eip /usr/bin/python3

# Then run without sudo
python main.py
```

To remove capabilities:

```bash
sudo setcap -r /usr/bin/python3
```

### Method 3: Using Virtual Environment with Capabilities

```bash
# Find your venv Python executable
which python

# Grant capabilities to venv Python
sudo setcap cap_net_raw,cap_net_admin=eip ~/Coding/Networking/venv/bin/python3

# Now run without sudo
source venv/bin/activate
python main.py
```

## Finding Network Interfaces

### List all network interfaces:

```bash
# Method 1: Using ip command (modern)
ip addr show

# Method 2: Using ifconfig (classical)
ifconfig

# Method 3: Using Scapy directly
python -c "from scapy.all import get_if_list; print(get_if_list())"
```

### Common interface names:

- `eth0`, `eth1`, ... - Wired Ethernet
- `wlan0`, `wlan1`, ... - Wireless
- `docker0` - Docker
- `veth...` - Virtual Ethernet (containers)
- `lo` - Loopback

## Usage Examples

### Basic Detection

```bash
# Default settings (10 seconds capture)
sudo python main.py

# Longer capture (30 seconds)
sudo python main.py --timeout 30

# More packets
sudo python main.py --packets 300

# Specific interface
sudo python main.py --interface eth0
```

### Custom Thresholds

```bash
# High latency threshold
sudo python main.py --latency-threshold 200

# Higher packet loss threshold
sudo python main.py --loss-threshold 10

# Combined
sudo python main.py --timeout 20 --packets 200 --latency-threshold 150
```

### Running Examples

```bash
# Activate venv first (no sudo needed for examples)
source venv/bin/activate

# Run example 1 (basic detection)
python examples.py 1

# Run example 3 (custom thresholds)
python examples.py 3

# Run all with sudo if doing actual detection
sudo python examples.py 5  # Continuous monitoring
```

## Useful Commands

```bash
# Activate virtual environment
source venv/bin/activate

# Deactivate virtual environment
deactivate

# List installed packages
pip list

# Check for package updates
pip list --outdated

# Update a package
pip install --upgrade scapy

# View help
python main.py --help

# Check Python version
python --version

# Run tests
python -m unittest tests.test_detectors

# Run specific test
python -m unittest tests.test_detectors.TestLoopDetector
```

## Troubleshooting

### Issue: Permission Denied

**Solution**: Use sudo
```bash
sudo python main.py
```

Or grant capabilities (one-time setup):
```bash
sudo setcap cap_net_raw,cap_net_admin=eip /usr/bin/python3
```

### Issue: No module named 'scapy'

**Solution**: Make sure virtual environment is activated
```bash
source venv/bin/activate
pip install -r requirements.txt
```

### Issue: Libpcap not found

**Solution**: Install libpcap development files
```bash
# Ubuntu/Debian
sudo apt-get install libpcap-dev

# Fedora/CentOS
sudo dnf install libpcap-devel
```

### Issue: Network interface not found

**Solution**: List available interfaces
```bash
python -c "from scapy.all import get_if_list; print(get_if_list())"

# Or use system commands
ip link show
```

Then specify correct interface:
```bash
sudo python main.py --interface eth0
```

### Issue: "venv: command not found"

**Solution**: Use full path or install venv
```bash
# Ubuntu/Debian
sudo apt-get install python3-venv

# Or use python module
python3 -m venv venv
```

### Issue: No packets captured

Try these steps:

1. Verify interface is active:
   ```bash
   ip link show eth0
   
   # Should show "UP" state
   ```

2. Check if interface is in use:
   ```bash
   tcpdump -i eth0 -c 10
   ```

3. Try loopback as test:
   ```bash
   sudo python main.py --interface lo
   ```

4. Generate traffic while capturing:
   ```bash
   # In another terminal
   ping 8.8.8.8
   
   # While running detector
   sudo python main.py --interface eth0
   ```

5. Check firewall:
   ```bash
   # Temporarily disable firewall
   sudo ufw disable
   
   # Re-enable when done
   sudo ufw enable
   ```

## Advanced Configuration

### Persistent Capabilities

To make packet capture work without sudo:

```bash
# 1. Create a group for pcap users
sudo groupadd pcap

# 2. Add your user to the group
sudo usermod -a -G pcap $USER

# 3. Grant capabilities
sudo setcap cap_net_raw,cap_net_admin=eip /usr/bin/python3

# 4. Log out and log back in (or: newgrp pcap)

# 5. Test (no sudo needed)
python main.py
```

### Running as Service

For continuous monitoring, create a systemd service:

```bash
# Create service file
sudo nano /etc/systemd/system/network-anomaly.service
```

Paste:
```ini
[Unit]
Description=Network Anomaly Detector
After=network.target

[Service]
Type=simple
User=root
WorkingDirectory=/home/username/Coding/Networking
ExecStart=/home/username/Coding/Networking/venv/bin/python main.py
Restart=always
RestartSec=10

[Install]
WantedBy=multi-user.target
```

Then:
```bash
# Reload systemd
sudo systemctl daemon-reload

# Start service
sudo systemctl start network-anomaly

# Enable on boot
sudo systemctl enable network-anomaly

# Check status
sudo systemctl status network-anomaly

# View logs
sudo journalctl -u network-anomaly -f
```

## Performance Tips

### Optimize for Low-Resource Systems

```bash
# Reduce packet count for faster analysis
python main.py --packets 50 --timeout 5

# Run on specific interface to avoid overhead
python main.py --interface eth0
```

### Optimize for Deep Analysis

```bash
# Increase packet count for more data
sudo python main.py --packets 500 --timeout 60
```

## Next Steps

- Read [QUICKSTART.md](QUICKSTART.md) for quick reference
- Read [README.md](README.md) for full documentation
- Run examples with `python examples.py 1-6`
- Customize `config.py` for your network

## Getting Help

1. Check [Troubleshooting](#troubleshooting) section
2. Verify libpcap is installed: `pkg-config --modversion libpcap`
3. Test Scapy: `python -c "from scapy.all import sniff; print('OK')"`
4. Check permissions: `id` (should show pcap group if configured)
5. Try on loopback interface first: `python main.py --interface lo`

## Uninstalling

```bash
# Deactivate virtual environment
deactivate

# Remove venv
rm -rf venv

# Remove repository (if cloned)
cd ~
rm -rf Coding/Networking
```

---

**Last Updated**: March 5, 2026
**Tested on**: Ubuntu 22.04 LTS, Debian 12, Fedora 39
**Python Version**: 3.7+
**Libpcap Version**: 1.10+
