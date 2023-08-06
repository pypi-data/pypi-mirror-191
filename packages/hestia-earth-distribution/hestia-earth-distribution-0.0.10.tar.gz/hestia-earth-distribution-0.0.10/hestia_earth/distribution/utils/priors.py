import os
from io import BytesIO
import pandas as pd

from hestia_earth.distribution.log import logger
from . import is_nonempty_str
from .storage import load_from_storage, write_to_storage

FOLDER = 'prior_files'
READ_BY_TYPE = {
    '.pkl': lambda x: pd.read_pickle(x),
    '.csv': lambda x: pd.read_csv(x, na_values='-', index_col=['term.id']),
    None: lambda *args: logger.error('Unsupported file type.')
}
WRITE_BY_TYPE = {
    '.pkl': lambda df, buffer: df.to_pickle(buffer),
    '.csv': lambda df, buffer: df.to_csv(buffer, na_rep='-', index=True, index_label='term.id'),
    None: lambda *args: logger.error('Unsupported file type.')
}


def read_prior_stats(filepath: str):
    logger.info(f'Reading existing file {filepath}')
    filename, file_ext = os.path.splitext(filepath)
    data = load_from_storage(filepath)
    return READ_BY_TYPE.get(file_ext)(BytesIO(data))


def generate_and_save_priors(filepath: str, func):
    """
    Return all prior statistics (means, std and n_years) of FAO fertiliser use from a CSV file.
    If prior file exisits, prior data will be read in; otherwise, generate priors and store into filepath path.

    Parameters
    ----------
    filepath: str
        Output csv file of FAO prior data, if it doesn't exist yet. Otherwise, read in from it.
    func: function
        Prior function to use.

    Returns
    -------
    pd.DataFrame
        DataFrame storing the prior of the means.
    """
    logger.info(f'Generating prior file to {filepath}.')
    filename, file_ext = os.path.splitext(filepath)
    result = func()
    buffer = BytesIO()
    WRITE_BY_TYPE.get(file_ext)(result, buffer)
    write_to_storage(filepath, buffer.getvalue())
    return result


def get_prior_by_country_by_product(filepath: str, country_id: str, product_id: str):
    """
    Return prior statistics (means, std and n_years) of FAO yield for one product for one country.

    Parameters
    ----------
    filepath: str
        Existing .pkl or .csv file of yield prior data.
    country_id: str
        Region `@id` from Hestia glossary, e.g. 'GADM-GBR', or 'region-south-america'.
    product_id: str
        Crop product term `@id` from Hestia glossary, e.g. 'wheatGrain'.

    Returns
    -------
    list or None
        list of four values: mu, sigma, n_years and -999 (placeholder for sigma_of_mu)), or None if unsuccssful.
    """
    df_stats = read_prior_stats(filepath)

    country_name = ' '.join(country_id.split('-')[1:])
    vals = df_stats.loc[product_id, country_id]

    if type(vals) == float:
        logger.error(f'No result of {product_id} from {country_name}')
        return None

    return [float(v) for v in vals.strip('()').split(',')] if is_nonempty_str(vals) else vals
