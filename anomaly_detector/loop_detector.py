"""Detect routing loops in network traffic."""

from collections import defaultdict
import numpy as np


class LoopDetector:
    """Detects network loops by analyzing TTL patterns and source routing."""
    
    def __init__(self, ttl_variance_threshold=3, circle_threshold=0.8):
        """
        Initialize loop detector.
        
        Args:
            ttl_variance_threshold: Variance threshold for TTL anomaly (hops)
            circle_threshold: Threshold for circular routing detection (0-1)
        """
        self.ttl_variance_threshold = ttl_variance_threshold
        self.circle_threshold = circle_threshold
        self.loops_detected = []
    
    def detect_loops(self, packets):
        """
        Detect potential routing loops in packet data.
        
        Loops are detected by:
        1. Analyzing TTL inconsistencies for same src-dst pairs
        2. Detecting circular routing patterns
        """
        if not packets:
            return []
        
        # Group packets by source-destination pair
        src_dst_pairs = defaultdict(list)
        for packet in packets:
            pair = (packet['src'], packet['dst'])
            src_dst_pairs[pair].append(packet)
        
        self.loops_detected = []
        
        # Check each src-dst pair for loop indicators
        for (src, dst), pair_packets in src_dst_pairs.items():
            ttl_values = [p['ttl'] for p in pair_packets]
            
            if len(ttl_values) < 3:
                continue
            
            # Check for TTL variance - loops cause inconsistent TTL decrements
            ttl_variance = np.var(ttl_values)
            ttl_mean = np.mean(ttl_values)
            ttl_std = np.std(ttl_values)
            
            # Anomaly: high variance in TTL for same route
            if ttl_std > self.ttl_variance_threshold:
                self.loops_detected.append({
                    'type': 'TTL_VARIANCE',
                    'source': src,
                    'destination': dst,
                    'ttl_mean': ttl_mean,
                    'ttl_std': ttl_std,
                    'ttl_values': ttl_values,
                    'severity': 'HIGH' if ttl_std > self.ttl_variance_threshold * 2 else 'MEDIUM',
                    'description': f"Inconsistent TTL values detected between {src} and {dst}"
                })
        
        # Check for circular routing patterns
        self._detect_circular_routing(packets)
        
        return self.loops_detected
    
    def _detect_circular_routing(self, packets):
        """Detect if packets are being routed in circles."""
        # Build a routing graph
        routing_paths = defaultdict(set)
        
        for packet in packets:
            src = packet['src']
            dst = packet['dst']
            # In a real scenario, we'd parse traceroute data or IPOP headers
            routing_paths[src].add(dst)
        
        # Check for bidirectional flows that might indicate loops
        for src, dsts in routing_paths.items():
            for dst in dsts:
                if dst in routing_paths and src in routing_paths[dst]:
                    # Bidirectional flow - check intensity
                    flow_count = sum(
                        1 for p in packets 
                        if (p['src'] == src and p['dst'] == dst) or 
                           (p['src'] == dst and p['dst'] == src)
                    )
                    
                    if flow_count > len(packets) * 0.3:  # More than 30% of traffic
                        self.loops_detected.append({
                            'type': 'CIRCULAR_ROUTING',
                            'node_a': src,
                            'node_b': dst,
                            'flow_frequency': flow_count / len(packets),
                            'severity': 'HIGH',
                            'description': f"Circular routing detected between {src} and {dst}"
                        })
    
    def get_loop_summary(self):
        """Get summary of detected loops."""
        if not self.loops_detected:
            return "No loops detected"
        
        summary = f"Found {len(self.loops_detected)} potential loop(s):\n"
        for i, loop in enumerate(self.loops_detected, 1):
            summary += f"{i}. {loop['type']}: {loop['description']} [Severity: {loop['severity']}]\n"
        
        return summary
