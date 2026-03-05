"""Pure Python network monitoring - no external dependencies required."""

import psutil
import socket
import threading
import time
from datetime import datetime
from collections import defaultdict
import statistics


class PurePythonMonitor:
    """
    Monitor network using only pure Python libraries (psutil, socket, etc).
    Works on Windows, Linux, and macOS without any external tools.
    """
    
    def __init__(self, interface=None):
        """
        Initialize pure Python network monitor.
        
        Args:
            interface: Network interface to monitor (optional)
        """
        self.interface = interface
        self.stats = []
        self.connections = []
        self.baseline = {}
        self.monitoring = False
    
    def get_available_interfaces(self):
        """Get list of available network interfaces."""
        try:
            interfaces = psutil.net_if_stats()
            return list(interfaces.keys())
        except Exception as e:
            print(f"Error getting interfaces: {e}")
            return []
    
    def get_interface_stats(self, interface=None):
        """
        Get statistics for a specific interface or all interfaces.
        
        Returns:
            Dictionary with interface statistics
        """
        try:
            if_name = interface or self.interface
            stats = psutil.net_if_stats()
            
            if if_name and if_name in stats:
                return {if_name: stats[if_name]}
            elif if_name is None:
                return stats
            else:
                return {}
        except Exception as e:
            print(f"Error getting interface stats: {e}")
            return {}
    
    def get_io_counters(self, interface=None):
        """
        Get I/O counters (bytes sent/received, packets, errors, dropped).
        
        Returns:
            Dictionary with counters
        """
        try:
            if_name = interface or self.interface
            
            # pernic=True gets per-interface stats
            counters = psutil.net_io_counters(pernic=True)
            
            if if_name and if_name in counters:
                return {if_name: counters[if_name]}
            elif if_name is None:
                return counters
            else:
                return {}
        except Exception as e:
            print(f"Error getting I/O counters: {e}")
            return {}
    
    def get_connections(self):
        """
        Get all network connections.
        
        Returns:
            List of connection objects
        """
        try:
            return psutil.net_connections()
        except Exception as e:
            print(f"Error getting connections: {e}")
            return []
    
    def monitor_interface(self, duration=10, interval=1):
        """
        Monitor an interface for packet loss and latency issues.
        
        Args:
            duration: Monitoring duration in seconds
            interval: Check interval in seconds
            
        Returns:
            Dictionary with monitoring results
        """
        if_name = self.interface
        if not if_name:
            # Use first active interface
            interfaces = [i for i, s in self.get_interface_stats().items() if s.isup]
            if interfaces:
                if_name = interfaces[0]
            else:
                print("No active interfaces found")
                return {}
        
        # Get initial counters
        initial = self.get_io_counters(if_name)
        if not initial:
            return {"error": f"Interface {if_name} not found"}
        
        initial_counter = initial[if_name]
        measurements = []
        errors = []
        dropped = []
        
        print(f"Monitoring {if_name} for {duration} seconds...")
        start_time = time.time()
        
        while time.time() - start_time < duration:
            current = self.get_io_counters(if_name)
            current_counter = current[if_name]
            
            # Record errors and dropped packets
            if current_counter.errin > initial_counter.errin:
                errors.append({
                    'timestamp': datetime.now(),
                    'errors': current_counter.errin - initial_counter.errin
                })
            
            if current_counter.dropin > initial_counter.dropin or \
               current_counter.dropout > initial_counter.dropout:
                dropped.append({
                    'timestamp': datetime.now(),
                    'dropped_in': current_counter.dropin - initial_counter.dropin,
                    'dropped_out': current_counter.dropout - initial_counter.dropout
                })
            
            measurements.append({
                'timestamp': datetime.now(),
                'bytes_in': current_counter.bytes_recv,
                'bytes_out': current_counter.bytes_sent,
                'packets_in': current_counter.packets_recv,
                'packets_out': current_counter.packets_sent
            })
            
            time.sleep(interval)
        
        # Get final counters
        final = self.get_io_counters(if_name)
        final_counter = final[if_name]
        
        # Calculate statistics
        total_packets = (final_counter.packets_recv - initial_counter.packets_recv) + \
                       (final_counter.packets_sent - initial_counter.packets_sent)
        
        total_errors = final_counter.errin - initial_counter.errin + \
                      final_counter.errout - initial_counter.errout
        
        total_dropped = final_counter.dropin - initial_counter.dropin + \
                       final_counter.dropout - initial_counter.dropout
        
        loss_percentage = 0
        if total_packets > 0:
            loss_percentage = ((total_errors + total_dropped) / total_packets) * 100
        
        return {
            'interface': if_name,
            'duration': duration,
            'total_packets': total_packets,
            'total_errors': total_errors,
            'total_dropped': total_dropped,
            'loss_percentage': loss_percentage,
            'bytes_sent': final_counter.bytes_sent - initial_counter.bytes_sent,
            'bytes_received': final_counter.bytes_recv - initial_counter.bytes_recv,
            'error_events': errors,
            'drop_events': dropped,
            'measurements': measurements,
            'severity': self._calculate_severity(loss_percentage)
        }
    
    def _calculate_severity(self, loss_percentage):
        """Calculate severity based on packet loss percentage."""
        if loss_percentage >= 30:
            return 'CRITICAL'
        elif loss_percentage >= 10:
            return 'HIGH'
        elif loss_percentage >= 5:
            return 'MEDIUM'
        else:
            return 'LOW'
    
    def detect_bandwidth_anomalies(self, interface=None, normal_range=None):
        """
        Detect unusual bandwidth usage.
        
        Args:
            interface: Interface to monitor
            normal_range: Tuple of (min_bps, max_bps) for normal usage
            
        Returns:
            List of anomalies detected
        """
        if_name = interface or self.interface
        io = self.get_io_counters(if_name)
        
        if not io:
            return []
        
        anomalies = []
        counter = io[if_name]
        
        # Current bandwidth
        current_bps = (counter.bytes_sent + counter.bytes_recv) * 8
        
        if normal_range:
            min_bps, max_bps = normal_range
            if current_bps < min_bps or current_bps > max_bps:
                anomalies.append({
                    'type': 'BANDWIDTH_ANOMALY',
                    'interface': if_name,
                    'current_bps': current_bps,
                    'expected_range': normal_range,
                    'severity': 'MEDIUM'
                })
        
        return anomalies
    
    def check_connection_anomalies(self):
        """
        Check for unusual connection patterns.
        
        Returns:
            List of detected anomalies
        """
        anomalies = []
        
        try:
            connections = psutil.net_connections()
            
            # Count connections by state
            state_count = defaultdict(int)
            for conn in connections:
                state_count[conn.status] += 1
            
            # Check for unusual states
            if state_count['TIME_WAIT'] > 100:
                anomalies.append({
                    'type': 'HIGH_TIME_WAIT_CONNECTIONS',
                    'count': state_count['TIME_WAIT'],
                    'severity': 'MEDIUM',
                    'description': 'Too many connections in TIME_WAIT state'
                })
            
            if state_count['CLOSE_WAIT'] > 50:
                anomalies.append({
                    'type': 'HIGH_CLOSE_WAIT_CONNECTIONS',
                    'count': state_count['CLOSE_WAIT'],
                    'severity': 'HIGH',
                    'description': 'Too many connections in CLOSE_WAIT state (resource leak?)'
                })
            
            # Check for established connections
            established = state_count['ESTABLISHED']
            if established > 1000:
                anomalies.append({
                    'type': 'MANY_ESTABLISHED_CONNECTIONS',
                    'count': established,
                    'severity': 'MEDIUM',
                    'description': f'{established} established connections detected'
                })
        
        except Exception as e:
            print(f"Error checking connections: {e}")
        
        return anomalies
    
    def get_system_network_info(self):
        """Get comprehensive network system information."""
        try:
            return {
                'interfaces': self.get_available_interfaces(),
                'interface_stats': self.get_interface_stats(),
                'io_counters': self.get_io_counters(),
                'connections': len(psutil.net_connections()),
                'connection_states': self._get_connection_states(),
            }
        except Exception as e:
            print(f"Error getting system info: {e}")
            return {}
    
    def _get_connection_states(self):
        """Get count of connections by state."""
        state_count = defaultdict(int)
        try:
            for conn in psutil.net_connections():
                state_count[conn.status] += 1
        except Exception:
            pass
        return dict(state_count)
    
    def test_dns(self, hostname='8.8.8.8'):
        """
        Test DNS/connectivity to a hostname.
        
        Returns:
            Latency in milliseconds or None if failed
        """
        try:
            start = time.time()
            socket.gethostbyname(hostname)
            latency = (time.time() - start) * 1000
            return latency
        except Exception as e:
            print(f"DNS test failed: {e}")
            return None
    
    def test_connectivity(self, host='8.8.8.8', port=53, timeout=2):
        """
        Test connectivity to a remote host:port.
        
        Returns:
            Latency in milliseconds or None if failed
        """
        try:
            start = time.time()
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.settimeout(timeout)
            sock.connect((host, port))
            sock.close()
            latency = (time.time() - start) * 1000
            return latency
        except Exception as e:
            return None
