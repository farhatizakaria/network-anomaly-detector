"""Example usage of the Network Anomaly Detector."""

import sys
from anomaly_detector import AnomalyDetector


def example_basic_detection():
    """Basic anomaly detection example."""
    print("Example 1: Basic Anomaly Detection")
    print("=" * 60)
    
    detector = AnomalyDetector()
    results = detector.analyze(timeout=5)
    
    if results:
        print(f"\nDetected {len(results['loops'])} routing loop(s)")
        print(f"Detected {len(results['losses'])} packet loss event(s)")
        print(f"Detected {len(results['latencies'])} latency anomaly(ies)")


def example_custom_interface():
    """Use specific network interface."""
    print("Example 2: Custom Interface")
    print("=" * 60)
    
    detector = AnomalyDetector(interface='eth0')
    results = detector.analyze(timeout=10)


def example_custom_thresholds():
    """Use custom detection thresholds."""
    print("Example 3: Custom Thresholds")
    print("=" * 60)
    
    config = {
        'packet_count': 200,                    # Capture 200 packets
        'latency_threshold_ms': 150,           # Flag if avg latency > 150ms
        'loss_threshold': 3.0,                 # Flag if loss > 3%
        'ttl_variance_threshold': 2,           # TTL variance threshold
        'zscore_threshold': 2.0,               # Spike detection sensitivity
    }
    
    detector = AnomalyDetector(config=config)
    results = detector.analyze(timeout=15)
    
    # Process specific results
    for latency in results['latencies']:
        print(f"\nLatency anomaly: {latency['description']}")


def example_detailed_analysis():
    """Analyze results in detail."""
    print("Example 4: Detailed Analysis")
    print("=" * 60)
    
    detector = AnomalyDetector()
    results = detector.analyze(timeout=10)
    
    # Analyze loops
    print("\n--- Routing Loops ---")
    if results['loops']:
        for loop in results['loops']:
            print(f"Type: {loop['type']}")
            print(f"Source: {loop.get('source', 'N/A')}")
            print(f"Destination: {loop.get('destination', 'N/A')}")
            print(f"Severity: {loop['severity']}")
            print(f"Description: {loop['description']}\n")
    else:
        print("No loops detected\n")
    
    # Analyze packet loss
    print("--- Packet Loss ---")
    if results['losses']:
        for loss in results['losses']:
            print(f"Route: {loss['source']} -> {loss['destination']}")
            print(f"Loss: {loss['loss_percentage']:.1f}%")
            print(f"Estimated lost packets: {loss['estimated_lost_packets']}")
            print(f"Severity: {loss['severity']}\n")
    else:
        print("No packet loss detected\n")
    
    # Analyze latency
    print("--- Latency Issues ---")
    if results['latencies']:
        for latency in results['latencies']:
            print(f"Type: {latency['type']}")
            print(f"Route: {latency['source']} -> {latency['destination']}")
            if 'avg_latency_ms' in latency:
                print(f"Avg Latency: {latency['avg_latency_ms']:.1f}ms")
            if 'jitter_ms' in latency:
                print(f"Jitter: {latency['jitter_ms']:.1f}ms")
            print(f"Severity: {latency['severity']}\n")
    else:
        print("No latency anomalies detected\n")


def example_monitoring_loop():
    """Continuous monitoring example."""
    print("Example 5: Continuous Monitoring")
    print("=" * 60)
    
    import time
    
    print("Running 3 cycles of detection...\n")
    
    for cycle in range(3):
        print(f"--- Cycle {cycle + 1} ---")
        detector = AnomalyDetector()
        results = detector.analyze(timeout=5)
        
        total_anomalies = (
            len(results['loops']) + 
            len(results['losses']) + 
            len(results['latencies'])
        )
        print(f"Total anomalies found: {total_anomalies}\n")
        
        if cycle < 2:
            print("Waiting 5 seconds before next cycle...\n")
            time.sleep(5)


def example_severity_filtering():
    """Filter and report by severity."""
    print("Example 6: Severity Filtering")
    print("=" * 60)
    
    detector = AnomalyDetector()
    results = detector.analyze(timeout=10)
    
    all_anomalies = []
    
    # Collect all anomalies
    for anomaly_list in results.values():
        if isinstance(anomaly_list, list):
            all_anomalies.extend(anomaly_list)
    
    # Group by severity
    by_severity = {}
    for anomaly in all_anomalies:
        severity = anomaly.get('severity', 'UNKNOWN')
        if severity not in by_severity:
            by_severity[severity] = []
        by_severity[severity].append(anomaly)
    
    # Report by severity
    for severity in ['CRITICAL', 'HIGH', 'MEDIUM']:
        count = len(by_severity.get(severity, []))
        print(f"{severity}: {count} anomaly(ies)")
        for anomaly in by_severity.get(severity, []):
            print(f"  - {anomaly.get('description', 'Unknown')}")


if __name__ == '__main__':
    print("Network Anomaly Detector - Usage Examples")
    print("=" * 60)
    print()
    
    if len(sys.argv) > 1:
        example_num = sys.argv[1]
        
        examples = {
            '1': example_basic_detection,
            '2': example_custom_interface,
            '3': example_custom_thresholds,
            '4': example_detailed_analysis,
            '5': example_monitoring_loop,
            '6': example_severity_filtering,
        }
        
        if example_num in examples:
            try:
                examples[example_num]()
            except Exception as e:
                print(f"Error: {e}")
                print("Note: Requires root/admin privileges and proper network interface")
        else:
            print(f"Unknown example: {example_num}")
            print(f"Available examples: {', '.join(sorted(examples.keys()))}")
    else:
        print("Usage: python examples.py <example_number>")
        print()
        print("Available examples:")
        print("  1 - Basic anomaly detection")
        print("  2 - Use custom network interface")
        print("  3 - Custom detection thresholds")
        print("  4 - Detailed analysis of results")
        print("  5 - Continuous monitoring loop")
        print("  6 - Filter and report by severity")
        print()
        print("Example: python examples.py 1")
