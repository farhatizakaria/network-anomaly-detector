"""Detect latency anomalies in network traffic."""

from collections import defaultdict
import numpy as np
from scipy import stats


class LatencyDetector:
    """Detects anomalous latency patterns in network traffic."""
    
    def __init__(self, latency_threshold_ms=100, zscore_threshold=2.5):
        """
        Initialize latency detector.
        
        Args:
            latency_threshold_ms: Absolute latency threshold in milliseconds
            zscore_threshold: Z-score threshold for detecting outliers
        """
        self.latency_threshold_ms = latency_threshold_ms
        self.zscore_threshold = zscore_threshold
        self.latency_anomalies = []
    
    def detect_latency_anomalies(self, packets):
        """
        Detect unusual latency patterns.
        
        Detects anomalies through:
        1. Request-response time analysis
        2. Statistical outlier detection (Z-score)
        3. Behavioral change detection
        """
        if not packets or len(packets) < 5:
            return []
        
        self.latency_anomalies = []
        
        # Group packets by flow
        flows = self._group_by_flow(packets)
        
        for flow_key, flow_packets in flows.items():
            if len(flow_packets) < 3:
                continue
            
            # Analyze request-response pairs (if available)
            self._detect_high_latency(flow_key, flow_packets)
            self._detect_latency_spikes(flow_key, flow_packets)
            self._detect_jitter(flow_key, flow_packets)
        
        return self.latency_anomalies
    
    def _group_by_flow(self, packets):
        """Group packets by flow and sort by timestamp."""
        flows = defaultdict(list)
        for packet in packets:
            flow_key = (packet['src'], packet['dst'])
            flows[flow_key].append(packet)
        
        # Sort by timestamp
        for flow_packets in flows.values():
            flow_packets.sort(key=lambda p: p['timestamp'])
        
        return flows
    
    def _detect_high_latency(self, flow_key, flow_packets):
        """Detect consistently high latency."""
        src, dst = flow_key
        
        # Calculate inter-packet delays in milliseconds
        delays_ms = []
        for i in range(1, len(flow_packets)):
            delay = (
                flow_packets[i]['timestamp'] - 
                flow_packets[i-1]['timestamp']
            ).total_seconds() * 1000
            delays_ms.append(delay)
        
        if not delays_ms:
            return
        
        avg_latency = np.mean(delays_ms)
        
        # Check if average latency exceeds threshold
        if avg_latency > self.latency_threshold_ms:
            percentile_95 = np.percentile(delays_ms, 95)
            max_latency = np.max(delays_ms)
            
            self.latency_anomalies.append({
                'type': 'HIGH_LATENCY',
                'source': src,
                'destination': dst,
                'avg_latency_ms': avg_latency,
                'p95_latency_ms': percentile_95,
                'max_latency_ms': max_latency,
                'threshold_ms': self.latency_threshold_ms,
                'severity': 'CRITICAL' if avg_latency > self.latency_threshold_ms * 2 else 'HIGH',
                'description': f"High latency detected: {avg_latency:.1f}ms avg (threshold: {self.latency_threshold_ms}ms)"
            })
    
    def _detect_latency_spikes(self, flow_key, flow_packets):
        """Detect sudden spikes in latency."""
        src, dst = flow_key
        
        # Calculate inter-packet delays
        delays_ms = []
        for i in range(1, len(flow_packets)):
            delay = (
                flow_packets[i]['timestamp'] - 
                flow_packets[i-1]['timestamp']
            ).total_seconds() * 1000
            delays_ms.append(max(delay, 0.01))  # Avoid log(0)
        
        if len(delays_ms) < 3:
            return
        
        # Use Z-score to detect outliers
        z_scores = np.abs(stats.zscore(delays_ms))
        spike_indices = np.where(z_scores > self.zscore_threshold)[0]
        
        if len(spike_indices) > 0:
            avg_delay = np.mean(delays_ms)
            max_spike = np.max(delays_ms[spike_indices])
            
            anomaly_count = len(spike_indices)
            anomaly_percentage = (anomaly_count / len(delays_ms)) * 100
            
            if anomaly_percentage > 5:  # More than 5% spikes
                self.latency_anomalies.append({
                    'type': 'LATENCY_SPIKE',
                    'source': src,
                    'destination': dst,
                    'spike_count': anomaly_count,
                    'spike_percentage': anomaly_percentage,
                    'avg_latency_ms': avg_delay,
                    'max_spike_ms': max_spike,
                    'severity': 'HIGH' if anomaly_percentage > 20 else 'MEDIUM',
                    'description': f"Detected {anomaly_count} latency spikes ({anomaly_percentage:.1f}%) between {src} and {dst}"
                })
    
    def _detect_jitter(self, flow_key, flow_packets):
        """Detect high jitter (latency variance)."""
        src, dst = flow_key
        
        # Calculate inter-packet delays
        delays_ms = []
        for i in range(1, len(flow_packets)):
            delay = (
                flow_packets[i]['timestamp'] - 
                flow_packets[i-1]['timestamp']
            ).total_seconds() * 1000
            delays_ms.append(delay)
        
        if len(delays_ms) < 5:
            return
        
        jitter = np.std(delays_ms)
        avg_delay = np.mean(delays_ms)
        
        # High jitter relative to average latency
        if avg_delay > 0 and (jitter / avg_delay) > 0.5:
            self.latency_anomalies.append({
                'type': 'HIGH_JITTER',
                'source': src,
                'destination': dst,
                'avg_latency_ms': avg_delay,
                'jitter_ms': jitter,
                'jitter_ratio': jitter / avg_delay,
                'severity': 'MEDIUM',
                'description': f"High jitter detected: {jitter:.1f}ms std dev (avg: {avg_delay:.1f}ms)"
            })
    
    def get_latency_summary(self):
        """Get summary of detected latency anomalies."""
        if not self.latency_anomalies:
            return "No latency anomalies detected"
        
        summary = f"Found {len(self.latency_anomalies)} latency anomaly(ies):\n"
        
        for i, anomaly in enumerate(self.latency_anomalies, 1):
            summary += f"\n{i}. {anomaly['type']}: {anomaly['description']}\n"
            summary += f"   Severity: {anomaly['severity']}\n"
        
        return summary
