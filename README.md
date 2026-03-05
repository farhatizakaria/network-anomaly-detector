# Network Anomaly Detector

A comprehensive Python tool for detecting network anomalies including routing loops, packet loss, and latency issues.

**Supports**: Windows, Linux, and macOS

## 📋 Platform Setup Guides

⚡ **New to this project?** Start here:

- **Windows Users**: See [WINDOWS_SETUP.md](WINDOWS_SETUP.md) for detailed instructions
- **Linux/macOS Users**: See [LINUX_SETUP.md](LINUX_SETUP.md) for detailed instructions
- **All Platforms**: See [PLATFORMS.md](PLATFORMS.md) for overview

For a quick start, see [QUICKSTART.md](QUICKSTART.md)

## Features Continued

### Platform-Specific Detection

**Linux/macOS**:
- Routing loop detection (TTL variance analysis)
- Packet loss analysis (sequence inspection)
- Latency spikes and jitter (statistical analysis)
- Circular routing detection

**Windows**:
- Packet loss detection (interface counters)
- Bandwidth anomaly detection
- Connection state analysis
- DNS/Connectivity latency testing
- System network statistics

*Windows uses pure Python libraries (psutil) for monitoring - no external tools required!*



## Installation

### Windows

1. **Install Python** (if not already installed): https://python.org
2. Clone or download this repository
3. Open Command Prompt and navigate to the project directory
4. Install dependencies:
   ```cmd
   pip install -r requirements.txt
   ```
   
**✨ No external tools required! Uses pure Python libraries only.**

### Linux/macOS

```bash
# Install dependencies
pip install -r requirements.txt
```

### Requirements
- Python 3.7+
- Scapy (packet manipulation)
- NumPy (numerical analysis)
- Pandas (data analysis)
- SciPy (statistical analysis)
- Matplotlib (visualization)
- PyYAML (configuration)

**Note**: Packet capture requires root/admin privileges.

## Usage

### Windows (Pure Python - No External Tools!) ✨

```cmd
# Activate virtual environment
venv\Scripts\activate

# Basic usage (no admin needed!)
python main.py

# Specify network interface
python main.py --interface "Ethernet"

# Set custom parameters
python main.py --timeout 15

# View options
python main.py --help
```

**Note**: No Npcap, Wireshark, or external tools required!

### Linux/macOS

```bash
# Activate virtual environment
source venv/bin/activate

# Run with sudo for detailed analysis
sudo python main.py

# Specify interface
sudo python main.py --interface eth0

# Set custom parameters
sudo python main.py --timeout 15 --packets 200
```

### Programmatic Usage

```python
from anomaly_detector import AnomalyDetector
from anomaly_detector.platform_utils import PlatformInfo

# Check platform information
print(f"Running on: {PlatformInfo.get_system()}")
print(f"Admin/Root: {PlatformInfo.require_admin()}")

# Create detector
detector = AnomalyDetector(interface='eth0', config={
    'packet_count': 100,
    'latency_threshold_ms': 100,
    'loss_threshold': 5.0
})

# Run analysis
results = detector.analyze(timeout=10)

# Access results
loops = results['loops']
losses = results['losses']
latencies = results['latencies']

# Process results
for loop in loops:
    print(f"Loop detected: {loop['description']}")
```

## Modules

### packet_analyzer.py
Captures and analyzes raw network packets using Scapy. Provides statistics and packet grouping by flow.

**Key Classes:**
- `PacketAnalyzer`: Main packet capture and analysis class

### loop_detector.py
Detects routing loops through:
- TTL variance analysis for each src-dst pair
- Circular routing pattern detection
- Bidirectional flow intensity analysis

**Key Classes:**
- `LoopDetector`: Identifies routing loops and circular paths

### loss_detector.py
Detects packet loss through:
- Timing gap analysis (missing packets create larger delays)
- Sequence number gap detection
- Baseline comparison against expected rates

**Key Classes:**
- `PacketLossDetector`: Identifies packet loss events

### latency_detector.py
Detects latency anomalies through:
- High latency detection (above absolute threshold)
- Latency spike detection (statistical outliers)
- Jitter detection (high variance in latency)

**Key Classes:**
- `LatencyDetector`: Comprehensive latency analysis

### detector.py
Main orchestrator that combines all detectors and generates reports.

**Key Classes:**
- `AnomalyDetector`: Main API for anomaly detection

## Anomaly Types

### Routing Loops
- **TTL_VARIANCE**: Inconsistent TTL values between same src-dst pairs indicate looping packets
- **CIRCULAR_ROUTING**: Bidirectional flows indicating circular routing

### Packet Loss
- **TIMING_GAP**: Large gaps in packet timing suggest lost packets
- Estimated loss percentage computed from gap sizes

### Latency Issues
- **HIGH_LATENCY**: Average latency exceeds threshold
- **LATENCY_SPIKE**: Individual packets have significantly delayed delivery
- **HIGH_JITTER**: High variance in packet arrival times

## Configuration

Edit `config.py` to customize detection parameters:

```python
LOOP_DETECTION = {
    'ttl_variance_threshold': 3,      # TTL std dev threshold
    'circle_threshold': 0.8,           # Circular routing intensity
}

LATENCY_DETECTION = {
    'threshold_ms': 100,               # High latency threshold
    'zscore_threshold': 2.5,           # Spike detection sensitivity
}

LOSS_DETECTION = {
    'loss_threshold': 5.0,             # Loss percentage threshold
}
```

## Output

The tool provides:
1. **Console Report**: Real-time detection results with severity levels
2. **Detailed Anomaly List**: Complete information for each detected anomaly
3. **Summary Statistics**: Total anomalies, severity breakdown, and recommendations

### Severity Levels

- 🔴 **CRITICAL**: Immediate investigation required
- 🟠 **HIGH**: Significant network issues
- 🟡 **MEDIUM**: Minor anomalies to monitor

## Examples

### Example 1: Detecting a Routing Loop

```python
from anomaly_detector import AnomalyDetector

detector = AnomalyDetector()
results = detector.analyze(timeout=15)

for loop in results['loops']:
    if loop['type'] == 'TTL_VARIANCE':
        print(f"Loop between {loop['source']} and {loop['destination']}")
        print(f"TTL variance: {loop['ttl_std']:.2f}")
```

### Example 2: Monitoring Link Quality

```python
detector = AnomalyDetector(config={'latency_threshold_ms': 150})
results = detector.analyze(timeout=10)

total_loss = sum(e['loss_percentage'] for e in results['losses'])
print(f"Total packet loss: {total_loss:.1f}%")
```

## Limitations

- **All Platforms**: Requires admin/root privileges for detailed monitoring
- Accuracy depends on sample size (more packets = better analysis)
- Unable to analyze encrypted traffic (can only see packet headers on Linux/macOS)
- May have false positives in unstable network conditions
- TTL analysis only works for IPv4 traffic (Linux/macOS only)
- **Windows**: Routing loop detection not available (uses different approach - see Features)

## Future Enhancements

- [ ] IPv6 support
- [ ] Persistent data storage and trending
- [ ] Network topology mapping
- [ ] TCP sequence number analysis
- [ ] Visualization dashboards
- [ ] Alert notifications (email, Slack, PagerDuty)
- [ ] Machine learning for adaptive thresholds
- [ ] Partial packet capture support

## Troubleshooting

### Permission Denied
```bash
# Run with sudo
sudo python main.py

# Or give specific capabilities (Linux)
sudo setcap cap_net_raw,cap_net_admin=eip /usr/bin/python3
```

### No Packets Captured
- Check if interface name is correct: `ifconfig` / `ipconfig`
- Disable firewall temporarily
- Try the default interface without specifying one

### Too Many False Positives
- Adjust thresholds in `config.py`
- Increase sample size (--packets parameter)
- Run on a stable baseline first

## License

MIT License

## Contributing

Contributions are welcome! Areas for improvement:
- Additional anomaly detection methods
- Performance optimization
- Extended protocol support
- Visualization tools

---

**Note**: This tool is for network monitoring and diagnostics. Ensure you have proper authorization before monitoring network traffic.
