"""Packet capture and analysis utilities."""

from scapy.all import sniff, IP, ICMP, TCP, UDP
from collections import defaultdict
import time
import socket
from datetime import datetime
from .platform_utils import PlatformInfo


class PacketAnalyzer:
    """Captures and analyzes network packets."""
    
    def __init__(self, interface=None, packet_count=100):
        self.interface = interface
        self.packet_count = packet_count
        self.packets = []
        self.ttl_map = defaultdict(list)  # Track TTL values for loop detection
        self.src_dst_pairs = defaultdict(list)  # Track source-destination pairs
        self.timestamps = defaultdict(list)  # Track packet timestamps
        
    def capture_packets(self, timeout=10):
        """Capture packets from the network."""
        print(f"Capturing {self.packet_count} packets (timeout: {timeout}s)...")
        
        def packet_callback(packet):
            if IP in packet:
                self.packets.append({
                    'packet': packet,
                    'timestamp': datetime.now(),
                    'src': packet[IP].src,
                    'dst': packet[IP].dst,
                    'ttl': packet[IP].ttl,
                    'proto': packet[IP].proto
                })
                
                # Track for anomaly detection
                pair = (packet[IP].src, packet[IP].dst)
                self.src_dst_pairs[pair].append(packet[IP].ttl)
                self.timestamps[pair].append(datetime.now())
        
        try:
            # Adjust sniff parameters based on platform
            sniff_kwargs = {
                'prn': packet_callback,
                'count': self.packet_count,
                'timeout': timeout,
                'store': False,
                'filter': None  # Start with no filter
            }
            
            # On Windows, interface parameter might need to be the IP address
            if self.interface and PlatformInfo.is_windows():
                sniff_kwargs['iface'] = self.interface
            elif self.interface:
                # Linux/macOS: use iface parameter
                sniff_kwargs['iface'] = self.interface
            
            # Try to sniff with these parameters
            sniff(**sniff_kwargs)
            print(f"Captured {len(self.packets)} packets")
            
        except PermissionError as e:
            print("❌ Error: Admin/Root privileges required for packet capture")
            if PlatformInfo.is_windows():
                print("   Solution: Run command prompt/PowerShell as Administrator")
            else:
                print("   Solution: Use 'sudo python main.py' or check sudo permissions")
                print("   Or install with capabilities: sudo setcap cap_net_raw=ep /usr/bin/python3")
            return False
            
        except (OSError, socket.error) as e:
            error_str = str(e)
            print(f"❌ Socket Error: {e}")
            
            # Suggest solutions based on error type
            if "Address family not supported" in error_str:
                print("   The system might not support raw packet capture in this environment")
                print("   (This can happen in containers, VMs, or restricted networks)")
            elif "No such device" in error_str:
                print("   Network interface not found or not accessible")
                print("   Solution: Check interface with 'ip link show'")
            else:
                print("   This might be a network interface or socket issue")
                
            if not PlatformInfo.is_windows():
                print("   Try running with: sudo python main.py")
                print("   Or check if libpcap is installed")
                
            return False
            
        except Exception as e:
            print(f"❌ Capture error: {type(e).__name__}: {e}")
            if "No module named 'pcap'" in str(e):
                if PlatformInfo.is_windows():
                    print("   Install Npcap from: https://npcap.com/")
                else:
                    print("   Install required: sudo apt-get install libpcap-dev")
            return False
        
        return True
    
    def get_packets(self):
        """Return captured packets."""
        return self.packets
    
    def get_packet_stats(self):
        """Get statistics about captured packets."""
        if not self.packets:
            return {}
        
        total = len(self.packets)
        src_ips = set(p['src'] for p in self.packets)
        dst_ips = set(p['dst'] for p in self.packets)
        
        return {
            'total_packets': total,
            'unique_sources': len(src_ips),
            'unique_destinations': len(dst_ips),
            'src_dst_pairs': len(self.src_dst_pairs)
        }
