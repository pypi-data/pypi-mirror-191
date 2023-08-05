import pandas as pd
import numpy as np
from hestia_earth.utils.lookup import download_lookup

from .log import logger
from .utils import SIGMA_SCALER, get_stats_from_df
from .utils.storage import file_exists
from .utils.fao import LOOKUP_YIELD, get_fao_yield, create_df_fao, get_mean_std_per_country_per_product
from .utils.priors import FOLDER, read_prior_stats, generate_and_save_priors

PRIOR_YIELD_FILENAME = 'FAO_Yield_prior_per_product_per_country.csv'


def calculate_worldwide_mean_sigma(product_id: str):
    """
    Calculate the means and sigmas for worldwide means and standard deviations of FAO yield for a specific product.

    Parameters
    ----------
    product_id: str
        Crop product term ID from Hestia glossary, e.g. 'wheatGrain'.

    Returns
    -------
    list of values:
        Means of worldwide means, std of worldwide means, mean of worldwide std, std of worldwide std.
    """
    df_fao = create_df_fao()
    world_means = []
    world_sigmas = []
    for gadm_code, row in df_fao.iterrows():
        stats = get_mean_std_per_country_per_product(product_id, gadm_code, get_fao_yield)
        if None not in stats:
            world_means.append(stats[0])
            world_sigmas.append(stats[1])
    world_means = np.array(world_means)
    world_sigmas = np.array(world_sigmas)
    return [world_means.mean(), world_means.std(), world_sigmas.mean(), world_sigmas.std()]


def _get_yield_priors(n_rows=10000):
    product_ids = download_lookup('crop.csv')[:n_rows]['termid']
    yield_lookup = download_lookup(LOOKUP_YIELD)

    df = pd.DataFrame(columns=yield_lookup['termid'], index=product_ids)

    for product_id in product_ids:
        logger.info(f'Processing {product_id}...')
        for gadm_code in yield_lookup['termid']:
            stats = get_mean_std_per_country_per_product(product_id, gadm_code, get_fao_yield)
            if None not in stats:
                df.loc[product_id, gadm_code] = stats[0], stats[1]*SIGMA_SCALER, stats[2], stats[1]

    df.index.rename('term.id', inplace=True)
    logger.info('Processing finished.')
    return df.dropna(axis=1, how='all').dropna(axis=0, how='all')


def generate_prior_yield_file(n: int = 2000, overwrite=False):
    """
    Return all prior statistics (means, std and n_years) of FAO yield from a CSV file.
    If prior file exisits, prior data will be read in; otherwise, generate priors and store into prior_file path.

    Parameters
    ----------
    n: int
        Optional - number of rows to return. Defaults to `2000`.
    overwrite: bool
        Optional - whether to overwrite existing prior file or not. Defaults to `False`.

    Returns
    -------
    pd.DataFrame
        DataFrame storing the prior of the means.
    """
    filepath = f"{FOLDER}/{PRIOR_YIELD_FILENAME}"
    read_existing = file_exists(filepath) and not overwrite
    return read_prior_stats(filepath) if read_existing else generate_and_save_priors(filepath, _get_yield_priors, n)


def get_prior(country_id: str, product_id: str):
    """
    Return prior data for a given country and a given product.
    Data is read from the file containing all prior data.

    Parameters
    ----------
    country_id: str
        Region `@id` from Hestia glossary, e.g. 'GADM-GBR', or 'region-south-america'.
    product_id: str
        Product term `@id` from Hestia glossary, e.g. 'wheatGrain'.

    Returns
    -------
    tuple(mu, sd)
        Mean values of mu and sd.
    """
    df = read_prior_stats(f"{FOLDER}/{PRIOR_YIELD_FILENAME}")
    return get_stats_from_df(df, country_id, product_id)
