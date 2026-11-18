import numpy as np
import pandas as pd


def build_features(df: pd.DataFrame) -> pd.DataFrame:
    """Ajoute les features de dynamique passée, de tension et de temporalité."""
    df = df.copy()
    g = df.groupby('station_code')

    # Dynamique passée (vérification stricte de l'intervalle temporel)
    for lag_steps, minutes in [(1, 15), (2, 30), (4, 60)]:
        past_time = g['collected_at_utc'].shift(lag_steps)
        dt_past = (df['collected_at_utc'] - past_time).dt.total_seconds() / 60
        valid_lag = dt_past.between(minutes - 1.5, minutes + 1.5)

        past_bikes = g['bikes_available'].shift(lag_steps).where(valid_lag)
        df[f'bikes_lag_{minutes}m'] = past_bikes
        df[f'diff_bikes_{minutes}m'] = df['bikes_available'] - past_bikes

    # Tension relative, répartition du parc et fraîcheur de la borne
    df['fill_rate'] = df['bikes_available'] / df['capacity'].replace(0, np.nan)
    df['elec_ratio'] = df['electric_bikes'] / (df['bikes_available'] + 1e-5)
    df['meca_ratio'] = df['mechanical_bikes'] / (df['bikes_available'] + 1e-5)
    df['freshness_min'] = (
        (df['collected_at_paris'] - df['source_updated_at_paris'])
        .dt.total_seconds() / 60
    )

    for col in ['is_installed', 'is_renting', 'is_returning']:
        df[col] = df[col].astype(int)

    # Variables calendaires et cycliques
    hour_float = (
        df['collected_at_paris'].dt.hour
        + df['collected_at_paris'].dt.minute / 60.0
    )
    df['hour_float'] = hour_float
    df['hour_sin'] = np.sin(2 * np.pi * hour_float / 24.0)
    df['hour_cos'] = np.cos(2 * np.pi * hour_float / 24.0)
    df['dayofweek'] = df['collected_at_paris'].dt.dayofweek
    df['is_weekend'] = (df['dayofweek'] >= 5).astype(int)

    return df