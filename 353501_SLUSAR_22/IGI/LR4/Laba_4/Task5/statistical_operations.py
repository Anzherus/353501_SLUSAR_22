import numpy as np

def calculate_variance_standard(data):
    """Вычисление дисперсии стандартной функцией"""
    return np.var(data)

def calculate_variance_manual(data):
    """Вычисление дисперсии по формуле"""
    mean = np.mean(data)
    squared_diff = [(x - mean) ** 2 for x in data]
    return sum(squared_diff) / len(data)

def calculate_statistics(data):
    """Вычисление основных статистических показателей"""
    stats = {
        'mean': np.mean(data),
        'median': np.median(data),
        'std': np.std(data),
        'corrcoef': np.corrcoef(data) if len(data) > 1 else None
    }
    return stats