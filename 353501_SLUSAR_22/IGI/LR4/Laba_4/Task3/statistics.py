"""
Module for calculation statistics
"""

import statistics
from typing import Dict, List

def calculate_stats(results: List[Dict]) -> Dict[str, float]:
    """
    Calculate statistics for the results.
    """
    values = [r['result'] for r in results]
    iterations = [r['iterations'] for r in results]
    
    stats = {
        'mean': statistics.mean(values),
        'median': statistics.median(values),
        'variance': statistics.variance(values) if len(values) > 1 else 0,
        'stdev': statistics.stdev(values) if len(values) > 1 else 0,
        'avg_iterations': statistics.mean(iterations)
    }
    
    try:
        stats['mode'] = statistics.mode(values)
    except statistics.StatisticsError:
        stats['mode'] = values[0] if values else 0
        
    return stats