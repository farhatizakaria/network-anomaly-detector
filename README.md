# 🌐 Network Anomaly Detector

A **modern, beautiful Python tool** for detecting network anomalies including routing loops, packet loss, and latency issues.

🎯 **Supports**: Windows, Linux, and macOS  
📦 **Pure Python** - No external tools required!  
✨ **Modern TUI/CLI** - Interactive, stunning interface  

---

## ✨ Features

### 🔄 Routing Loop Detection
- Detects circular routing patterns using TTL (Time To Live) variance analysis
- Identifies potentially problematic network paths

### 📉 Packet Loss Analysis
- Monitors packet sequence numbers for missing packets
- Quantifies connection quality issues
- Cross-platform compatible

### ⚡ Latency Anomaly Detection
- Statistical analysis using Z-scores
- Identifies latency spikes and jitter
- Real-time performance monitoring

---

## 🚀 Quick Start

### Prerequisites
- **Python 3.7+**
- **Administrator/Root privileges** (for packet capture)
  - Linux/macOS: `sudo python main.py`
  - Windows: Run cmd/PowerShell as Administrator

### Installation

```bash
# Clone the repository
git clone <repo-url>
cd Networking

# Install dependencies
pip install -r requirements.txt

# Run with interactive mode (recommended)
python main.py --interactive

# Or run with default settings
python main.py
```

---

## 📖 Usage

### 🎮 Interactive Mode
Recommended for most users - provides guided prompts and beautiful visualization:

```bash
python main.py --interactive
```

Features:
- 📋 Menu-driven interface
- 🎨 Colorful output with emojis
- ⚙️ Custom parameter configuration
- ❓ Built-in help system

### 💻 Command-Line Mode

```bash
# Monitor with default settings
python main.py

# Custom interface monitoring
python main.py --interface eth0

# Extended analysis duration
python main.py --timeout 30 --packets 500

# Full custom configuration
python main.py \
  --interface eth0 \
  --timeout 20 \
  --packets 200 \
  --latency-threshold 150 \
  --loss-threshold 3.0
```

### 📊 Output

The tool displays results in beautiful, organized tables:

```
🔄 ROUTING LOOPS DETECTED
┌─────┬──────────────┬──────────────────┐
│ ID  │ Path         │ TTL Variance     │
├─────┼──────────────┼──────────────────┤
│ 1   │ 192.168.1.1  │ 2.45             │
└─────┴──────────────┴──────────────────┘

📉 PACKET LOSS EVENTS
┌───────┬──────────┬────────────────────┐
│ Event │ Loss %   │ Packets Analyzed   │
├───────┼──────────┼────────────────────┤
│ 1     │ 8.50%    │ 200                │
└───────┴──────────┴────────────────────┘

⚡ LATENCY ANOMALIES
┌──────────┬────────────────┬──────────┐
│ Anomaly  │ Value (ms)     │ Severity │
├──────────┼────────────────┼──────────┤
│ Spike 1  │ 250.45         │ HIGH     │
└──────────┴────────────────┴──────────┘
```

---

## 🛠️ All Command Options

```
--interface, -i         Network interface to monitor (e.g., eth0, en0)
                       Default: auto-detect

--timeout, -t          Capture duration in seconds
                       Range: 1-300 seconds
                       Default: 10

--packets, -p          Number of packets to capture
                       Range: 10-10000
                       Default: 100

--latency-threshold    Latency threshold (milliseconds)
                       Range: 10-5000 ms
                       Default: 100 ms

--loss-threshold       Packet loss threshold (percentage)
                       Range: 0.1-100 %
                       Default: 5.0 %

--interactive          Launch interactive menu mode
```

---

## 📋 Platform-Specific Information

### Linux & macOS
- Uses Scapy for packet capture
- Requires root/sudo privileges
- Supports both IPv4 and IPv6
- Direct packet analysis from network stack

**Setup:**
```bash
sudo python main.py
# or enable packet capture without sudo:
# sudo setcap cap_net_raw=ep /usr/bin/python3
```

### Windows
- Uses pure Python libraries (psutil) for monitoring
- Run cmd/PowerShell as Administrator
- Note: Some advanced packet analysis features may be limited without Npcap/Winpcap

**Setup:**
```cmd
# Run as Administrator
python main.py
```

---

## ⚠️ Requirements & Privileges

| OS | Requirement | How to Run |
|---|---|---|
| **Linux/macOS** | Root/sudo | `sudo python main.py` |
| **Windows** | Admin | Right-click cmd/PowerShell → "Run as administrator" |

Without proper privileges:
- ❌ Packet capture will fail
- ❌ Real-time analysis unavailable
- ⚠️ Only basic statistics available

---

## 📦 Dependencies

```
scapy>=2.5.0              - Packet manipulation
numpy>=1.21.0             - Numerical analysis
pandas>=1.3.0             - Data processing
scipy>=1.7.0              - Scientific computing
psutil>=5.9.0             - System monitoring
rich>=13.0.0              - Beautiful terminal output
typer>=0.9.0              - Modern CLI framework
questionary>=2.0.0        - Interactive prompts
```

Install all dependencies:
```bash
pip install -r requirements.txt
```

---

## 🔍 How It Works

### Detection Pipeline

1. **Packet Capture**
   - Captures raw network packets from specified interface
   - Builds packet statistics database

2. **Analysis Modules**
   ```
   Packets → Loop Detector → Loss Detector → Latency Detector → Results
   ```

3. **Results Aggregation**
   - Combines all detections
   - Color-codes severity levels
   - Generates visual reports

---

## 🎨 Features Highlights

### 🌈 Beautiful Terminal UI
- Color-coded alerts and statuses
- Unicode borders and emojis
- Progress bars with real-time updates
- Organized data tables

### 🎯 Smart Defaults
- Auto-detect network interface
- Intelligent threshold setting
- Platform-aware configuration

### 🔄 Real-Time Monitoring
- Live progress indicators
- Animated analysis feedback
- Instant result display

---

## ❓ FAQ & Troubleshooting

### "No packets captured"
- Ensure you have **admin/root privileges**
- Verify interface name: `ip link show` (Linux) or `ipconfig` (Windows)
- Check if interface is active and has traffic

### "Permission denied"
- **Linux/macOS**: Run with `sudo`
- **Windows**: Run cmd/PowerShell as Administrator

### "Timeout waiting for packets"
- Network interface may be idle
- Try monitoring during active traffic
- Increase `--packets` for larger sample

### "All results are green but network seems slow"
- Increase analysis duration: `--timeout 30`
- Use larger packet sample: `--packets 500`
- Adjust threshold sensitivity

---

## 📝 Project Structure

```
Networking/
├── main.py                      # Modern TUI/CLI entry point
├── requirements.txt             # Python dependencies
├── config.py                    # Configuration defaults
├── README.md                    # This file
├── PLATFORMS.md                 # Platform-specific details
├── setup.py                     # Package setup
└── anomaly_detector/
    ├── __init__.py
    ├── detector.py              # Main detector orchestrator
    ├── packet_analyzer.py       # Packet capture & parsing
    ├── loop_detector.py         # Routing loop detection
    ├── loss_detector.py         # Packet loss detection
    ├── latency_detector.py      # Latency spike detection
    ├── platform_utils.py        # Cross-platform utilities
    ├── windows_monitor.py       # Windows-specific monitoring
    └── pure_python_monitor.py   # Pure Python fallback
```

---

## 🧪 Testing

Run the test suite:

```bash
python -m pytest tests/
```

---

## 📄 License

MIT License - See LICENSE file for details

---

## 🤝 Contributing

Contributions are welcome! Please:
1. Fork the repository
2. Create a feature branch
3. Commit your changes
4. Push to the branch
5. Open a Pull Request

---

## 💡 Tips for Best Results

✅ **Do:**
- Run with elevated privileges
- Monitor during periods of network activity  
- Use longer timeout for larger datasets
- Adjust thresholds based on your baseline

❌ **Don't:**
- Run on heavily congested networks without filtering
- Use with dropped privilege levels
- Expect results from inactive interfaces

---

## 🐛 Reporting Issues

Found a bug? Have a feature request?

Please include:
- Your operating system and Python version
- Command line arguments used
- Output or error messages
- Network environment description

---

**🎉 Enjoy beautiful network monitoring!**

For more details, see [PLATFORMS.md](PLATFORMS.md) for platform-specific information.
