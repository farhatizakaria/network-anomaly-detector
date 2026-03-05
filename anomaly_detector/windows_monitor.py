"""Windows-specific network anomaly detector using pure Python."""

from .pure_python_monitor import PurePythonMonitor
from datetime import datetime


class WindowsAnomalyDetector:
    """
    Windows-specific anomaly detector using only pure Python libraries.
    No external tools or dependencies required.
    """
    
    def __init__(self, interface=None, config=None):
        """
        Initialize Windows anomaly detector.
        
        Args:
            interface: Network interface to monitor
            config: Configuration dictionary
        """
        self.interface = interface
        self.config = config or {}
        self.monitor = PurePythonMonitor(interface=interface)
        self.results = {}
    
    def analyze(self, timeout=10):
        """
        Run network anomaly detection on Windows.
        
        Args:
            timeout: Monitoring duration in seconds
            
        Returns:
            Dictionary with detection results
        """
        print("Starting Windows Network Anomaly Detection (Pure Python)")
        print("=" * 60)
        print("Note: Using psutil for network monitoring (no Npcap required)")
        print()
        
        # Get available interfaces
        interfaces = self.monitor.get_available_interfaces()
        print(f"Available Network Interfaces: {', '.join(interfaces)}")
        
        if not interfaces:
            print("Error: No network interfaces found")
            return None
        
        # Use specified or first active interface
        target_interface = self.interface
        if not target_interface:
            # Find first active interface
            interface_stats = self.monitor.get_interface_stats()
            active = [name for name, stats in interface_stats.items() if stats.isup]
            target_interface = active[0] if active else interfaces[0]
        
        print(f"Monitoring Interface: {target_interface}")
        print()
        
        # Update monitor's interface before monitoring
        self.monitor.interface = target_interface
        
        # Run monitoring
        print("[1] Analyzing packet loss and connection quality...")
        monitor_results = self.monitor.monitor_interface(
            duration=timeout,
            interval=1
        )
        self.results['packet_loss'] = monitor_results
        
        # Check for bandwidth anomalies
        print("\n[2] Checking for bandwidth anomalies...")
        bandwidth_anomalies = self.monitor.detect_bandwidth_anomalies(target_interface)
        self.results['bandwidth_anomalies'] = bandwidth_anomalies
        
        # Check connection anomalies
        print("[3] Analyzing connection patterns...")
        connection_anomalies = self.monitor.check_connection_anomalies()
        self.results['connection_anomalies'] = connection_anomalies
        
        # Test connectivity
        print("[4] Testing DNS/Connectivity...")
        dns_latency = self.monitor.test_dns()
        self.results['dns_latency'] = dns_latency
        
        connectivity_latency = self.monitor.test_connectivity()
        self.results['connectivity_latency'] = connectivity_latency
        
        # Generate report
        print("\n" + "=" * 60)
        self._print_report(monitor_results, bandwidth_anomalies, connection_anomalies)
        
        return self.results
    
    def _print_report(self, monitor_results, bandwidth_anomalies, connection_anomalies):
        """Print comprehensive analysis report."""
        print("ANALYSIS REPORT")
        print()
        
        # Packet Loss Analysis
        print("1. PACKET LOSS ANALYSIS")
        print("-" * 40)
        if 'error' not in monitor_results:
            total_packets = monitor_results['total_packets']
            loss_pct = monitor_results['loss_percentage']
            severity = monitor_results['severity']
            
            print(f"   Total Packets: {total_packets}")
            print(f"   Errors: {monitor_results['total_errors']}")
            print(f"   Dropped: {monitor_results['total_dropped']}")
            print(f"   Loss Percentage: {loss_pct:.2f}%")
            print(f"   Severity: {severity}")
            
            if loss_pct > 0:
                print(f"   ⚠️  Packet loss detected!")
                if monitor_results['error_events']:
                    print(f"   {len(monitor_results['error_events'])} error event(s)")
                if monitor_results['drop_events']:
                    print(f"   {len(monitor_results['drop_events'])} drop event(s)")
            else:
                print(f"   ✓ No packet loss detected")
        else:
            print(f"   Error: {monitor_results.get('error')}")
        
        print()
        
        # Bandwidth Analysis
        print("2. BANDWIDTH ANOMALIES")
        print("-" * 40)
        if bandwidth_anomalies:
            for anomaly in bandwidth_anomalies:
                print(f"   {anomaly['type']}")
                print(f"   Current: {anomaly['current_bps']/1_000_000:.2f} Mbps")
                print(f"   Expected: {anomaly['expected_range'][0]/1_000_000:.2f} - {anomaly['expected_range'][1]/1_000_000:.2f} Mbps")
                print(f"   Severity: {anomaly['severity']}")
        else:
            print("   ✓ No bandwidth anomalies detected")
        
        print()
        
        # Connection Analysis
        print("3. CONNECTION ANOMALIES")
        print("-" * 40)
        if connection_anomalies:
            for anomaly in connection_anomalies:
                print(f"   {anomaly['type']}")
                print(f"   Issue: {anomaly['description']}")
                print(f"   Count: {anomaly['count']}")
                print(f"   Severity: {anomaly['severity']}")
        else:
            print("   ✓ No connection anomalies detected")
        
        print()
        
        # Connectivity Test
        print("4. CONNECTIVITY TESTS")
        print("-" * 40)
        dns_latency = self.results.get('dns_latency')
        conn_latency = self.results.get('connectivity_latency')
        
        if dns_latency is not None:
            print(f"   DNS Latency: {dns_latency:.2f} ms")
        else:
            print(f"   DNS Latency: Failed")
        
        if conn_latency is not None:
            print(f"   Connection Latency: {conn_latency:.2f} ms")
        else:
            print(f"   Connection Latency: Failed")
        
        print()
        
        # Summary
        print("=" * 60)
        total_issues = len(bandwidth_anomalies) + len(connection_anomalies)
        if monitor_results.get('loss_percentage', 0) > 0:
            total_issues += 1
        
        print(f"SUMMARY: {total_issues} issue(s) detected")
        print()
        
        # Recommendations
        print("RECOMMENDATIONS:")
        if monitor_results.get('loss_percentage', 0) > 5:
            print("   • Check network interface drivers")
            print("   • Verify network cable/WiFi connection")
            print("   • Monitor for latency spikes")
        
        if connection_anomalies:
            print("   • Review active network connections")
            print("   • Check for resource leaks")
            print("   • Consider restarting network services")
        
        if bandwidth_anomalies:
            print("   • Investigate bandwidth usage")
            print("   • Check for network congestion")
        
        if dns_latency is None or conn_latency is None:
            print("   • Check internet connectivity")
            print("   • Verify firewall rules")
            print("   • Check DNS configuration")
