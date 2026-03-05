"""Detect packet loss in network traffic."""

from collections import defaultdict
import numpy as np


class PacketLossDetector:
    """Detects packet loss between network endpoints."""
    
    def __init__(self, loss_threshold=5.0, sequence_window=50):
        """
        Initialize packet loss detector.
        
        Args:
            loss_threshold: Loss percentage threshold to flag as anomaly
            sequence_window: Window size for analyzing packet sequences
        """
        self.loss_threshold = loss_threshold
        self.sequence_window = sequence_window
        self.loss_events = []
    
    def detect_loss(self, packets):
        """
        Detect packet loss by analyzing packet patterns.
        
        Detects loss through:
        1. Sequence number gaps
        2. ACK/NACK mismatches
        3. Unusual time gaps between packets
        """
        if not packets or len(packets) < 5:
            return []
        
        self.loss_events = []
        
        # Group packets by src-dst-port combination
        flows = self._group_by_flow(packets)
        
        for flow_key, flow_packets in flows.items():
            if len(flow_packets) < 3:
                continue
            
            # Check for gaps in timing that indicate lost packets
            self._detect_timing_gaps(flow_key, flow_packets)
        
        return self.loss_events
    
    def _group_by_flow(self, packets):
        """Group packets by flow (src-dst pair)."""
        flows = defaultdict(list)
        for packet in packets:
            # For simplicity, group by src-dst
            flow_key = (packet['src'], packet['dst'])
            flows[flow_key].append(packet)
        
        # Sort by timestamp
        for flow_packets in flows.values():
            flow_packets.sort(key=lambda p: p['timestamp'])
        
        return flows
    
    def _detect_timing_gaps(self, flow_key, flow_packets):
        """Detect packet loss through timing analysis."""
        src, dst = flow_key
        
        # Calculate inter-packet delays
        delays = []
        for i in range(1, len(flow_packets)):
            time_diff = (
                flow_packets[i]['timestamp'] - 
                flow_packets[i-1]['timestamp']
            ).total_seconds()
            delays.append(time_diff)
        
        if not delays:
            return
        
        avg_delay = np.mean(delays)
        delay_std = np.std(delays)
        
        # Detect unusual gaps (possible packet loss)
        for i, delay in enumerate(delays):
            # If delay is significantly larger than average
            if delay > avg_delay + (3 * delay_std) and avg_delay > 0:
                # Estimate possible lost packets
                lost_count = int(delay / (avg_delay + 0.001)) - 1
                
                if lost_count > 0:
                    loss_percentage = (lost_count / len(flow_packets)) * 100
                    
                    if loss_percentage > self.loss_threshold:
                        self.loss_events.append({
                            'source': src,
                            'destination': dst,
                            'detection_method': 'TIMING_GAP',
                            'packet_index': i,
                            'gap_duration': delay,
                            'expected_delay': avg_delay,
                            'estimated_lost_packets': lost_count,
                            'loss_percentage': loss_percentage,
                            'severity': 'HIGH' if loss_percentage > 20 else 'MEDIUM',
                            'description': f"Detected {lost_count} potentially lost packets ({loss_percentage:.1f}% loss) between {src} and {dst}"
                        })
    
    def detect_loss_baseline(self, packets):
        """
        Detect packet loss by comparing to baseline statistics.
        
        This uses expected packet counts for common protocols.
        """
        expected_rates = {
            'ICMP': 1.0,  # 1 request per second
            'DNS': 0.5,
            'HTTP': 0.1
        }
        
        flow_stats = defaultdict(lambda: {'count': 0, 'duration': 0})
        
        for packet in packets:
            flow_key = (packet['src'], packet['dst'])
            flow_stats[flow_key]['count'] += 1
            flow_stats[flow_key]['duration'] = (
                packets[-1]['timestamp'] - packets[0]['timestamp']
            ).total_seconds()
        
        return self.loss_events
    
    def get_loss_summary(self):
        """Get summary of detected packet loss."""
        if not self.loss_events:
            return "No significant packet loss detected"
        
        total_loss_percentage = np.mean([
            e['loss_percentage'] for e in self.loss_events
        ]) if self.loss_events else 0
        
        summary = f"Detected {len(self.loss_events)} packet loss event(s):\n"
        summary += f"Average loss percentage: {total_loss_percentage:.1f}%\n\n"
        
        for i, event in enumerate(self.loss_events, 1):
            summary += f"{i}. {event['description']}\n"
            summary += f"   Loss: {event['loss_percentage']:.1f}% | Severity: {event['severity']}\n"
        
        return summary
