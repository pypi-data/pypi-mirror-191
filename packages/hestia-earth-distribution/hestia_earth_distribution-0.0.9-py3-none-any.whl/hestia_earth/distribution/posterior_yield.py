import pandas as pd

from .utils.posterior import update_all_post_data, get_post_data, get_post_ensemble_data
from .prior_yield import generate_prior_yield_file

POSTERIOR_YIELD_FILENAME = 'posterior_crop_yield.csv'


def get_post_ensemble(country_id: str, product_id: str, overwrite=False, df_prior: pd.DataFrame = None):
    """
    Return posterior data for a given country and a given product.
    If posterior file exisits, data will be read in; otherwise, generate posterior data and store
    into a pickle or json file.

    Parameters
    ----------
    country_id: str
        Region `@id` from Hestia glossary, e.g. 'GADM-GBR', or 'region-south-america'.
    product_id: str
        Product term `@id` from Hestia glossary, e.g. 'wheatGrain'.
    overwrite: bool
        Whether to overwrite existing posterior file or not. Defaults to `False`.
    df_prior: pd.DataFrame
        Optional - if prior file is already loaded, pass it here.

    Returns
    -------
    tuple(mu, sd)
        List of float storing the posterior mu and sd ensembles.
    """
    return get_post_ensemble_data(country_id, product_id,
                                  overwrite=overwrite, df_prior=df_prior, generate_prior=generate_prior_yield_file)


def update_all_post(rows: list = None, cols: list = None, overwrite=True):
    """
    Update crop posterior data for all countries and all products.
    It creates or re-write json files to store posterior data for each country and each product.
    It also writes all distribution stats (mu, sigma) into one csv file.

    Parameters
    ----------
    rows: list of int
        Rows (products) to be updated. Default None to include all products.
    cols: list of int
        Columns (countries) to be updated. Default None to include all countries.
    overwrite: bool
        Whether to overwrite the posterior json files. Defaults to `True`.

    Returns
    -------
    DataFrame
        A DataFrame storing all posterior data.
    """
    df_prior = generate_prior_yield_file()
    return update_all_post_data(df_prior, POSTERIOR_YIELD_FILENAME, rows, cols, overwrite=overwrite)


def get_post(country_id: str, product_id: str):
    """
    Return posterior data for a given country and a given product.
    Data is read from the file containing all posterior data.
    Cannot use this function to generate new post files.

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
    return get_post_data(country_id, product_id, POSTERIOR_YIELD_FILENAME)
