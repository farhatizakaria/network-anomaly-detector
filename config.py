"""Configuration defaults for anomaly detection."""

# Packet capture settings
PACKET_CAPTURE = {
    'default_count': 100,
    'timeout_seconds': 10,
}

# Loop detection settings
LOOP_DETECTION = {
    'ttl_variance_threshold': 3,          # Max acceptable TTL std dev
    'circle_threshold': 0.8,              # Circular routing intensity threshold
}

# Packet loss detection settings
LOSS_DETECTION = {
    'loss_threshold': 5.0,                 # Loss percentage to flag
    'sequence_window': 50,                 # Packet window for analysis
}

# Latency detection settings
LATENCY_DETECTION = {
    'threshold_ms': 100,                   # High latency threshold
    'zscore_threshold': 2.5,               # Z-score for spike detection
    'jitter_threshold_ratio': 0.5,         # Jitter to latency ratio
}

# Output settings
OUTPUT = {
    'verbose': True,
    'save_report': False,
    'report_format': 'text',  # 'text', 'json', 'csv'
}

# Alert thresholds
ALERT_LEVELS = {
    'CRITICAL': {
        'loop': True,
        'loss_percentage': 30,
        'latency_ms': 500,
    },
    'HIGH': {
        'loss_percentage': 10,
        'latency_ms': 200,
        'jitter_ratio': 1.0,
    },
    'MEDIUM': {
        'loss_percentage': 5,
        'latency_ms': 100,
    },
}
