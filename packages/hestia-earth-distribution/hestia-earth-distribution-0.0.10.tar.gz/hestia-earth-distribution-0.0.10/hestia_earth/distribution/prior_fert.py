import pandas as pd

from .log import logger
from .utils import SIGMA_SCALER, get_stats_from_df, get_country_ids
from .utils.storage import file_exists
from .utils.fao import get_fao_fertuse, get_mean_std_per_country_per_product
from .utils.cycle import get_fert_group_id, get_input_ids
from .utils.priors import FOLDER, read_prior_stats, generate_and_save_priors

PRIOR_FERT_FILENAME = 'FAO_Fert_prior_per_input_per_country.csv'


def get_fao_fert(country_id: str, input_id: str, n_years: int = 10):
    """
    Look up the FAO yield per country per product from the glossary.

    Parameters
    ----------
    country_id: str
        Region `@id` from Hestia glossary, e.g. 'GADM-GBR', or 'region-south-america'.
    fert_id: str
        Inorganic or organic fertiliser term ID from Hestia glossary, e.g. 'ammoniumNitrateKgN'.
    n_years: int
        Number of years (in reverse chronological order) of FAO data record to get. Defaults to `10` years.

    Returns
    -------
    nunpy.array or None
        A 2-D array with years and yield values from FAO yield record, if successful.
    """
    fert_id = get_fert_group_id(input_id)
    return get_fao_fertuse(country_id, fert_id, n_years=n_years)


def _get_fert_priors():
    input_ids = get_input_ids()
    country_ids = get_country_ids()
    df_stats = pd.DataFrame(columns=country_ids, index=input_ids)

    for input_id in input_ids:
        logger.info(f'Processing {input_id}...')
        for country_id in country_ids:
            stats = get_mean_std_per_country_per_product(input_id, country_id, get_fao_fertuse)
            if None not in stats:
                df_stats.loc[input_id, country_id] = stats[0], stats[1]*SIGMA_SCALER, stats[2], stats[1]

    df_stats.index.rename('term.id', inplace=True)
    logger.info('Processing finished.')
    return df_stats


def generate_prior_fert_file(overwrite=False):
    """
    Return all prior statistics (means, std and n_years) of FAO fertiliser use from a CSV file.
    If prior file exisits, prior data will be read in; otherwise, generate priors and stores it on disk.

    Parameters
    ----------
    overwrite: bool
        Optional - whether to overwrite existing prior file or not.

    Returns
    -------
    pd.DataFrame
        The prior of the means.
    """
    filepath = f"{FOLDER}/{PRIOR_FERT_FILENAME}"
    read_existing = file_exists(filepath) and not overwrite
    return read_prior_stats(filepath) if read_existing else generate_and_save_priors(filepath, _get_fert_priors)


def get_prior(country_id: str, input_id: str):
    """
    Return prior data for a given country and a given input.
    Data is read from the file containing all prior data.

    Parameters
    ----------
    country_id: str
        Region `@id` from Hestia glossary, e.g. 'GADM-GBR', or 'region-south-america'.
    input_id: str
        Product term `@id` from Hestia glossary, e.g. 'wheatGrain'.

    Returns
    -------
    tuple(mu, sd)
        Mean values of mu and sd.
    """
    df = read_prior_stats(f"{FOLDER}/{PRIOR_FERT_FILENAME}")
    fert_id = get_fert_group_id(input_id)
    return get_stats_from_df(df, country_id, fert_id)
