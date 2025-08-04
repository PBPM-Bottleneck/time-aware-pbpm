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

def add_queue_length_feature(df, case_id_col='case_id', timestamp_col='timestamp'):
    """
    Fügt dem DataFrame eine Spalte 'queue_length' hinzu, die 
    die Anzahl paralleler, aktiver Fälle zum Zeitpunkt jedes Events zählt.
    
    Parameters
    ----------
    df : pd.DataFrame
        Eventlog mit Spalten für Case-ID und Zeitstempel.
    case_id_col : str
        Name der Spalte mit der Case-ID.
    timestamp_col : str
        Name der Spalte mit dem Zeitstempel.
        
    Returns
    -------
    pd.DataFrame
        Kopie des DataFrames mit neuer Spalte 'queue_length'.
    """
    df = df.copy()
    # Zähle pro Zeitstempel die Anzahl eindeutiger Fälle und ziehe den eigenen Fall ab
    concurrent = df.groupby(timestamp_col)[case_id_col].transform('nunique')
    df['queue_length'] = concurrent - 1
    return df
