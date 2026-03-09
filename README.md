# 🌐 Network Anomaly Detector

A **modern, beautiful Python tool** for detecting network anomalies including routing loops, packet loss, and latency issues.

🎯 **Supports**: Windows, Linux, and macOS  
📦 **Pure Python** - No external tools required!  
✨ **Modern TUI/CLI** - Interactive, stunning interface  

---

## ⚡ Quick Start (Choose Your OS)

### Windows 🪟
```cmd
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
# Run as Administrator:
python main.py --interactive
```

### Linux / macOS 🐧 🍎
```bash
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
sudo python main.py --interactive
```

---

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

## 📋 Platform-Specific Setup

### 🪟 Windows Setup

1. **Ensure Python is installed**:
   ```cmd
   python --version
   ```

2. **Clone the repository**:
   ```cmd
   git clone <repo-url>
   cd Networking
   ```

3. **Create virtual environment** (recommended):
   ```cmd
   python -m venv venv
   venv\Scripts\activate
   ```

4. **Install dependencies**:
   ```cmd
   pip install -r requirements.txt
   ```

5. **Run with Administrator privileges**:
   ```cmd
   # Right-click Command Prompt or PowerShell → "Run as administrator"
   python main.py --interactive
   ```

**✨ Note**: Windows uses pure Python libraries (psutil, numpy, scipy) for network monitoring - **no external tools required**!

### 🐧 Linux Setup

1. **Install Python and development tools**:
   ```bash
   sudo apt-get update
   sudo apt-get install python3 python3-pip python3-dev libpcap-dev build-essential
   ```

2. **Clone the repository**:
   ```bash
   git clone <repo-url>
   cd Networking
   ```

3. **Create virtual environment** (recommended):
   ```bash
   python3 -m venv venv
   source venv/bin/activate
   ```

4. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

5. **Run with sudo for packet capture**:
   ```bash
   sudo python main.py --interactive
   ```

**Optional**: Enable packet capture without sudo:
   ```bash
   sudo setcap cap_net_raw=ep /usr/bin/python3
   python main.py
   ```

### 🍎 macOS Setup

1. **Install Homebrew** (if not already installed):
   ```bash
   /bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"
   ```

2. **Install dependencies**:
   ```bash
   brew install python3 libpcap
   ```

3. **Clone the repository**:
   ```bash
   git clone <repo-url>
   cd Networking
   ```

4. **Create virtual environment** (recommended):
   ```bash
   python3 -m venv venv
   source venv/bin/activate
   ```

5. **Install Python packages**:
   ```bash
   pip install -r requirements.txt
   ```

6. **Run with sudo**:
   ```bash
   sudo python main.py --interactive
   ```

---

## ⚙️ Platform-Specific Information

### 🪟 Windows
- Uses **pure Python** network monitoring (psutil library)
- **No Npcap/WinPcap required** for basic analysis
- Admin privileges needed for detailed network statistics
- Automatic fallback to pure Python if advanced packet capture unavailable
- All features work with just Python standard library + requirements

**Features available**:
- ✓ Network interface monitoring
- ✓ Packet loss detection
- ✓ Latency analysis
- ✓ Connection statistics

### 🐧 Linux
- Uses Scapy for packet capture (requires root/sudo)
- Direct access to network stack
- Full IPv4 and IPv6 support
- Detailed packet-level analysis
- Optional: Enable capabilities to run without sudo

---

## ⚠️ Privilege Requirements

| OS | Required | How to Run |
|---|:---:|---|
| **Windows** | Admin | Right-click Command Prompt/PowerShell → "Run as administrator" |
| **Linux** | Root/Sudo | `sudo python main.py` or enable capabilities |
| **macOS** | Root/Sudo | `sudo python main.py` |

**Without proper privileges:**
- ❌ Advanced packet-level analysis unavailable
- ⚠️ Falls back to basic statistics only (Windows)
- ⚠️ Packet capture fails (Linux/macOS)

---

## 📦 Dependencies

All dependencies are pure Python and cross-platform compatible:

```ini
scapy>=2.5.0              - Packet manipulation (Linux/macOS)
numpy>=1.21.0             - Numerical analysis
pandas>=1.3.0             - Data processing
scipy>=1.7.0              - Scientific computing
psutil>=5.9.0             - System & network monitoring
rich>=13.0.0              - Beautiful terminal output
typer>=0.9.0              - Modern CLI framework
questionary>=2.0.0        - Interactive prompts
```

**Windows**: Works with pure Python - no system libraries needed!  
**Linux/macOS**: May require `libpcap-dev` (see platform setup above)

Install all dependencies:
```bash
pip install -r requirements.txt
```

---

## 🔄 Virtual Environment Setup (Recommended)

### Windows:
```cmd
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
```

### Linux/macOS:
```bash
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

The virtual environment folder (`venv/`) is **automatically excluded from Git** via `.gitignore`.

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
