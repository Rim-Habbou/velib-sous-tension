import pandas as pd


def load_and_clean(filepath: str) -> pd.DataFrame:
    """Charge le fichier brut, convertit les dates en Europe/Paris et trie par station."""
    df = pd.read_csv(filepath)

    df['collected_at_utc'] = pd.to_datetime(df['collected_at_utc'], utc=True)
    df['collected_at_paris'] = df['collected_at_utc'].dt.tz_convert('Europe/Paris')
    df['source_updated_at_paris'] = (
        pd.to_datetime(df['source_updated_at'], utc=True)
        .dt.tz_convert('Europe/Paris')
    )

    return df.sort_values(['station_code', 'collected_at_paris']).reset_index(drop=True)


def filter_and_split(df: pd.DataFrame) -> tuple[pd.DataFrame, pd.DataFrame, pd.DataFrame]:
    """
    Crée la cible à t+30 min et la baseline de persistance, filtre les trous de collecte
    et retourne le découpage chronologique (train_df, val_df, test_df) avec embargo.
    """
    g = df.groupby('station_code')
    bikes_futur = g['bikes_available'].shift(-2)
    time_futur = g['collected_at_utc'].shift(-2)
    delta_futur = (time_futur - df['collected_at_utc']).dt.total_seconds() / 60

    df_clean = df[delta_futur.between(29, 31)].copy()
    df_clean['cible'] = (bikes_futur.loc[df_clean.index] < 2).astype(int)
    df_clean['pred_persistance'] = (df_clean['bikes_available'] < 2).astype(int)

    tz = df_clean['collected_at_paris'].dt.tz
    cutoff_val = pd.Timestamp('2026-09-26 00:00:00', tz=tz)
    cutoff_test = pd.Timestamp('2026-10-02 00:00:00', tz=tz)
    embargo = pd.Timedelta(minutes=30)

    train_df = df_clean[df_clean['collected_at_paris'] < (cutoff_val - embargo)].copy()
    val_df = df_clean[
        (df_clean['collected_at_paris'] >= cutoff_val) &
        (df_clean['collected_at_paris'] < (cutoff_test - embargo))
    ].copy()
    test_df = df_clean[df_clean['collected_at_paris'] >= cutoff_test].copy()

    return train_df, val_df, test_df