import pandas as pd
import numpy as np

def generate_bottleneck_labels(df: pd.DataFrame, time_col: str = "remaining_time", threshold_factor: float = 1.5):
    """
    Erzeugt binäre Engpass-Labels basierend auf der verbleibenden Zeit.

    Parameters
    ----------
    df : pd.DataFrame
        Eventlog mit Spalte für verbleibende Zeit.
    time_col : str
        Name der Spalte mit verbleibender Zeit.
    threshold_factor : float
        Faktor für Schwellwert (z.B. Median * 1.5).

    Returns
    -------
    pd.Series
        0 = kein Engpass, 1 = Engpass
    """
    median_time = df[time_col].median()
    threshold = median_time * threshold_factor
    return (df[time_col] > threshold).astype(int)

def add_bottleneck_labels(df: pd.DataFrame, time_col: str = "remaining_time"):
    """
    Fügt dem DataFrame eine neue Spalte 'bottleneck_label' hinzu.
    """
    df['bottleneck_label'] = generate_bottleneck_labels(df, time_col)
    return df
