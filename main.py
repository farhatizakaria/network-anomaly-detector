"""
Network Anomaly Detector - Command line interface.

Detects network anomalies including loops, packet loss, and latency issues.
Requires root/admin privileges for packet capture.

Usage:
    python main.py [--interface eth0] [--timeout 10] [--packets 100]
"""

import argparse
import sys
import os
from anomaly_detector import AnomalyDetector
from anomaly_detector.platform_utils import PlatformInfo


def main():
    """Main entry point."""
    parser = argparse.ArgumentParser(
        description='Network Anomaly Detector - Detect loops, packet loss, and latency issues',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Monitor default interface for 10 seconds
  python main.py --timeout 10
  
  # Monitor specific interface
  python main.py --interface eth0 --timeout 15
  
  # Increase packet sample size
  python main.py --packets 200 --timeout 20
        """
    )
    
    parser.add_argument(
        '--interface', '-i',
        help='Network interface to monitor (e.g., eth0, en0). If not specified, uses default.',
        default=None
    )
    
    parser.add_argument(
        '--timeout', '-t',
        type=int,
        help='Capture timeout in seconds',
        default=10
    )
    
    parser.add_argument(
        '--packets', '-p',
        type=int,
        help='Number of packets to capture',
        default=100
    )
    
    parser.add_argument(
        '--latency-threshold',
        type=int,
        help='Latency threshold in milliseconds (default: 100)',
        default=100
    )
    
    parser.add_argument(
        '--loss-threshold',
        type=float,
        help='Packet loss threshold percentage (default: 5.0)',
        default=5.0
    )
    
    args = parser.parse_args()
    
    # Create configuration
    config = {
        'packet_count': args.packets,
        'latency_threshold_ms': args.latency_threshold,
        'loss_threshold': args.loss_threshold,
    }
    
    try:
        # Initialize detector
        system = PlatformInfo.get_system()
        is_admin = PlatformInfo.require_admin()
        
        print("Network Anomaly Detector v1.0")
        print(f"[{system} - {'Admin/Root' if is_admin else 'Standard User'}]")
        print("=" * 60)
        
        # Check for privilege requirements
        if not is_admin:
            print("⚠️  WARNING: Running without admin/root privileges")
            print("   Packet capture may fail or be limited")
            if system == "Windows":
                print("   On Windows: Right-click cmd/PowerShell and 'Run as administrator'")
            else:
                print("   On Linux/macOS: Use 'sudo python main.py' or enable capabilities")
            print()
        
        print(f"Interface: {args.interface or 'auto-detect'}")
        print(f"Timeout: {args.timeout}s")
        print(f"Packet count: {args.packets}")
        print()
        
        detector = AnomalyDetector(interface=args.interface, config=config)
        
        # Run analysis
        results = detector.analyze(timeout=args.timeout)
        
        if results is None:
            sys.exit(1)
        
        return 0
    
    except KeyboardInterrupt:
        print("\n\nAnalysis interrupted by user")
        return 130
    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
        return 1


if __name__ == '__main__':
    sys.exit(main())
