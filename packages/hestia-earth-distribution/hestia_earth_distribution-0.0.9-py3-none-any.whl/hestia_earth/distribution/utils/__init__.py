from io import BytesIO
import pandas as pd
import numpy as np

SIGMA_SCALER = 3.0  # Scaler (for standard deviation) value of the prior


def is_nonempty_str(value): return (type(value) in [str, np.str_, np.string_]) and value != ''


def get_stats_from_df(df, country_id: str, term_id: str):
    try:
        yield_stats = df.loc[term_id][country_id]
        # this happens when read priors in from a CSV file
        vals = [float(v) for v in yield_stats.strip('()').split(',')] if type(yield_stats) == str else yield_stats
        return vals[0], vals[1]  # mu, sigma
    except Exception:
        return None, None  # data could not be parsed


def df_to_csv_buffer(df: pd.DataFrame):
    buffer = BytesIO()
    df.to_csv(buffer)
    return buffer.getvalue()
