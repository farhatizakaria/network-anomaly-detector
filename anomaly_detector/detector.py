"""Main anomaly detector that orchestrates all detection modules."""

from .packet_analyzer import PacketAnalyzer
from .loop_detector import LoopDetector
from .loss_detector import PacketLossDetector
from .latency_detector import LatencyDetector
from .platform_utils import PlatformInfo
from .windows_monitor import WindowsAnomalyDetector


class AnomalyDetector:
    """Main anomaly detector that combines all detection modules."""
    
    def __init__(self, interface=None, config=None):
        """
        Initialize the anomaly detector.
        
        Args:
            interface: Network interface to monitor (e.g., 'eth0')
            config: Configuration dictionary for detector parameters
        """
        self.interface = interface
        self.config = config or {}
        
        # Initialize sub-detectors
        self.packet_analyzer = PacketAnalyzer(
            interface=interface,
            packet_count=self.config.get('packet_count', 100)
        )
        self.loop_detector = LoopDetector(
            ttl_variance_threshold=self.config.get('ttl_variance_threshold', 3),
            circle_threshold=self.config.get('circle_threshold', 0.8)
        )
        self.loss_detector = PacketLossDetector(
            loss_threshold=self.config.get('loss_threshold', 5.0),
            sequence_window=self.config.get('sequence_window', 50)
        )
        self.latency_detector = LatencyDetector(
            latency_threshold_ms=self.config.get('latency_threshold_ms', 100),
            zscore_threshold=self.config.get('zscore_threshold', 2.5)
        )
        
        self.results = {}
    
    def analyze(self, timeout=10):
        """
        Run full anomaly detection analysis.
        
        Args:
            timeout: Capture timeout in seconds
            
        Returns:
            Dictionary with all detection results
        """
        print("Starting network anomaly detection...")
        print("=" * 60)
        
        # On Windows, use pure Python monitor (no Npcap required)
        if PlatformInfo.is_windows():
            print("🪟 Windows Detected - Using Pure Python Network Monitor")
            print("   (No external tools or dependencies required)")
            print()
            
            detector = WindowsAnomalyDetector(
                interface=self.interface,
                config=self.config
            )
            return detector.analyze(timeout)
        
        # On Linux/macOS, try Scapy first, with fallback to pure Python
        print(f"🐧 {PlatformInfo.get_system()} Detected - Attempting Scapy Packet Analysis")
        print()
        
        # Step 1: Try to capture packets with Scapy
        if not self.packet_analyzer.capture_packets(timeout=timeout):
            print("\n⚠️  WARNING: Scapy packet capture failed")
            print("   Falling back to Pure Python Network Monitor...")
            print("   (This provides basic statistics instead of detailed packet analysis)\n")
            
            detector = WindowsAnomalyDetector(
                interface=self.interface,
                config=self.config
            )
            results = detector.analyze(timeout)
            if results:
                results['analysis_mode'] = 'fallback'
            return results
        
        packets = self.packet_analyzer.get_packets()
        print("\nPacket Statistics:")
        for key, value in self.packet_analyzer.get_packet_stats().items():
            print(f"  {key}: {value}")
        
        # Step 2: Run detectors
        print("\nAnalyzing packets for anomalies...")
        print("-" * 60)
        
        # Loop detection
        print("\n[1] Running loop detection...")
        loops = self.loop_detector.detect_loops(packets)
        self.results['loops'] = loops
        print(self.loop_detector.get_loop_summary())
        
        # Packet loss detection
        print("\n[2] Running packet loss detection...")
        losses = self.loss_detector.detect_loss(packets)
        self.results['losses'] = losses
        print(self.loss_detector.get_loss_summary())
        
        # Latency detection
        print("\n[3] Running latency analysis...")
        latencies = self.latency_detector.detect_latency_anomalies(packets)
        self.results['latencies'] = latencies
        print(self.latency_detector.get_latency_summary())
        
        # Step 3: Generate report
        print("\n" + "=" * 60)
        self._print_summary()
        
        # Mark as native Scapy analysis
        self.results['analysis_mode'] = 'scapy'
        
        return self.results
    
    def _print_summary(self):
        """Print final anomaly summary."""
        total_anomalies = sum(len(v) for v in self.results.values() if isinstance(v, list))
        
        print(f"FINAL REPORT: {total_anomalies} total anomalies detected\n")
        
        severity_count = {'CRITICAL': 0, 'HIGH': 0, 'MEDIUM': 0}
        
        for anomaly_list in self.results.values():
            if isinstance(anomaly_list, list):
                for anomaly in anomaly_list:
                    if 'severity' in anomaly:
                        severity_count[anomaly['severity']] = severity_count.get(anomaly['severity'], 0) + 1
        
        print(f"Severity Breakdown:")
        print(f"  🔴 CRITICAL: {severity_count['CRITICAL']}")
        print(f"  🟠 HIGH: {severity_count['HIGH']}")
        print(f"  🟡 MEDIUM: {severity_count['MEDIUM']}")
        
        print("\nRecommendations:")
        if severity_count['CRITICAL'] > 0:
            print("  - Immediate investigation required for critical anomalies")
        if len(self.results.get('loops', [])) > 0:
            print("  - Check network topology for routing loops")
        if len(self.results.get('losses', [])) > 0:
            print("  - Check link quality and network congestion")
        if len(self.results.get('latencies', [])) > 0:
            print("  - Investigate path quality and network load")
    
    def get_results(self):
        """Get detailed analysis results."""
        return self.results
