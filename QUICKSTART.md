# Quick Start Guide

## Installation

### Linux/macOS

```bash
# Navigate to project directory
cd ~/Coding/Networking

# Install dependencies
pip install -r requirements.txt
```

### Windows

```cmd
# Navigate to project directory
cd C:\path\to\Networking

# Install dependencies
pip install -r requirements.txt
```

**Note for Windows**: Make sure you have Python installed. If not, download from [python.org](https://python.org)

## Virtual Environment Setup

### Linux/macOS

```bash
# Create virtual environment (one-time setup)
python3 -m venv venv

# Activate virtual environment
source venv/bin/activate

# Or use the provided script
bash activate.sh
```

### Windows

```cmd
# Create virtual environment (one-time setup)
python -m venv venv

# Activate virtual environment
venv\Scripts\activate

# Or double-click the provided script
activate.bat
```

## Basic Usage

### Windows ✨ (No Admin Mode Needed!)

```cmd
# Make sure virtual environment is activated
venv\Scripts\activate

# Run detector (pure Python - works immediately!)
python main.py

# With custom parameters
python main.py --interface "Ethernet" --timeout 15

# View all options
python main.py --help
```

**No Npcap or external tools required!** Uses pure Python libraries only.

### Linux/macOS

```bash
# Make sure virtual environment is activated
source venv/bin/activate

# Run with sudo (required for detailed packet capture and analysis)
sudo python main.py

# Or run with custom parameters
sudo python main.py --interface eth0 --timeout 15 --packets 200

# Custom thresholds
sudo python main.py --latency-threshold 200 --loss-threshold 10
```

**Note**: On some systems, you may need to deactivate venv before using sudo:
```bash
deactivate
sudo python -m anomaly_detector.detector
```

## First Run Checklist

### Windows ✨ (No External Tools Needed!)
1. ✅ Install Python from python.org (if not already installed)
2. ✅ Install dependencies: `pip install -r requirements.txt`
3. ✅ Create virtual environment: `python -m venv venv`
4. ✅ Activate venv: `venv\Scripts\activate` or run `activate.bat`
5. ✅ Run: `python main.py` (No admin mode needed!)
6. ✅ Review results in console output

### Linux/macOS
1. ✅ Install dependencies: `pip install -r requirements.txt`
2. ✅ Create virtual environment: `python3 -m venv venv`
3. ✅ Activate venv: `source venv/bin/activate` or `bash activate.sh`
4. ✅ Run with sudo: `sudo python main.py`
5. ✅ Review results in console output

## What Gets Detected

The tool automatically detects:

1. **Routing Loops**
   - Packets bouncing between routers
   - Inconsistent TTL (Time-To-Live) values
   - Circular routing patterns

2. **Packet Loss**
   - Missing packets in flows
   - Large timing gaps between packets
   - Loss percentage calculation

3. **Latency Anomalies**
   - High average latency
   - Sudden latency spikes
   - Network jitter (inconsistent delays)

## Output Interpretation

### Console Output Example
```
FINAL REPORT: 3 total anomalies detected

Severity Breakdown:
  🔴 CRITICAL: 0
  🟠 HIGH: 1
  🟡 MEDIUM: 2

Recommendations:
  - Check network topology for routing loops
  - Investigate path quality and network load
```

### Anomaly Details

Each detected anomaly includes:
- **Type**: Category (TTL_VARIANCE, TIMING_GAP, HIGH_LATENCY)
- **Source/Destination**: Affected IP addresses
- **Severity**: CRITICAL, HIGH, or MEDIUM
- **Description**: Human-readable explanation
- **Metrics**: Specific values (latency_ms, loss_percentage, etc.)

## Troubleshooting

### Windows

#### Issue: Permission Denied / Admin Error
```cmd
# Run Command Prompt as Administrator
# Right-click Command Prompt and select "Run as Administrator"
# Then activate venv and run the program

venv\Scripts\activate
python main.py
```

#### Issue: Npcap Not Found
- Download from https://npcap.com/
- Run installer with administrator
- Restart Python after installation

#### Issue: Network interface not found
```cmd
# List available interfaces
python -c "from scapy.all import get_if_list; print(get_if_list())"
```

#### Issue: "No module named 'pcap'"
- Install Npcap from https://npcap.com/
- Restart your machine after installation

### Linux/macOS

#### Issue: Permission Denied
```bash
# Run with elevated privileges
sudo python main.py

# Or (Linux only - give specific capabilities)
sudo setcap cap_net_raw,cap_net_admin=eip /usr/bin/python3
```

#### Issue: No packets captured
- Check interface name: `ifconfig` or `ip addr`
- Try without specifying interface: `sudo python main.py`
- Disable firewall temporarily
- Ensure interface is up: `ip link show eth0`

### Both Platforms

#### Issue: Too many/few anomalies detected
- Adjust thresholds in `config.py`
- Increase sample size: `--packets 200`
- Increase capture time: `--timeout 20` 

#### Issue: Virtual environment not activating
- Windows: Make sure you're in the correct directory and run `venv\Scripts\activate.bat`
- Linux/macOS: Run `source venv/bin/activate` (note the `source` command)

## Next Steps

1. **Review README.md** for detailed documentation
2. **Run examples.py** to see different use cases
3. **Customize config.py** for your network baseline
4. **Run unit tests**: `python -m pytest tests/`
5. **Integrate** into your monitoring pipeline

## Common Commands

### Linux/macOS

```bash
# Basic detection (10 seconds)
sudo python main.py

# Extended monitoring (30 seconds, more packets)
sudo python main.py --timeout 30 --packets 300

# Continuous loop
python examples.py 5

# Run unit tests
python -m unittest tests.test_detectors

# Programmatic usage
python examples.py 4
```

### Windows

```cmd
# Activate virtual environment first
venv\Scripts\activate

# Basic detection (10 seconds, requires Admin)
python main.py

# Extended monitoring (30 seconds, more packets)
python main.py --timeout 30 --packets 300

# Continuous loop
python examples.py 5

# Run unit tests
python -m unittest tests.test_detectors

# Programmatic usage
python examples.py 4
```

## Dependencies

- **scapy**: Raw packet manipulation
- **numpy**: Numerical operations
- **scipy**: Statistical analysis
- **pandas**: Data handling
- **matplotlib**: Visualization (future)
- **pyyaml**: Configuration management

All included in `requirements.txt`

## Files Overview

| File | Purpose |
|------|---------|
| `main.py` | Command-line entry point |
| `examples.py` | Usage examples and demos |
| `config.py` | Configuration defaults |
| `anomaly_detector/` | Main package directory |
| `anomaly_detector/detector.py` | Main orchestrator |
| `anomaly_detector/packet_analyzer.py` | Packet capture |
| `anomaly_detector/loop_detector.py` | Loop detection |
| `anomaly_detector/loss_detector.py` | Loss detection |
| `anomaly_detector/latency_detector.py` | Latency analysis |
| `tests/test_detectors.py` | Unit tests |
| `README.md` | Full documentation |
| `requirements.txt` | Python dependencies |

## Getting Help

- Check `README.md` for detailed documentation
- Review `examples.py` for code examples
- Run `python main.py --help` for CLI options
- Check `config.py` for tunable parameters
- Review source code comments for implementation details

---

Ready to start? Run: `sudo python main.py`
