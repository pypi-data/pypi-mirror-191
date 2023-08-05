import pandas as pd
import numpy as np
from hestia_earth.utils.lookup import download_lookup, get_table_value, column_name

from . import is_nonempty_str

LOOKUP_YIELD = 'region-crop-cropGroupingFaostatProduction-yield.csv'
LOOKUP_FERTUSE = 'region-inorganicFertiliser-fertilisersUsage.csv'


def create_df_fao():
    """
    Create a DataFrame to store all FAO crop yield data.
    This DataFrame can be used by plotting functions, especially with multiple subplots.

    Returns
    -------
    pd.DataFrame
        A DataFrame to store all FAO crop yield data, with index of country codes and column names of FAO crop terms.
    """
    lookup = download_lookup(LOOKUP_YIELD)
    fao_products = lookup.dtype.names[1:]

    df_fao = pd.DataFrame(index=lookup['termid'], columns=fao_products)

    for country_id in lookup['termid']:
        for product_name in fao_products:
            fao_yields = get_table_value(lookup, 'termid', country_id, column_name(product_name))
            df_fao.loc[country_id, product_name] = fao_yields
    return df_fao


def get_FAO_crop_name(product_id: str):
    """
    Look up the FAO term from Hestia crop term.

    Parameters
    ----------
    product_id: str
        Crop product term `@id` from Hestia glossary, e.g. 'wheatGrain'.

    Returns
    -------
    str
        FAO Crop product term, e.g. 'Wheat'.
    """
    lookup = download_lookup('crop.csv')
    return get_table_value(lookup, 'termid', product_id, column_name('cropGroupingFaostatProduction'))


def fao_str_record_to_array(fao_str: str, output_type=np.float32, n_years: int = 10, scaler: int = 1):
    """
    Converts FAO string records to np.array, and rescale if needed.

    Parameters
    ----------
    fao_str: str
        A string with time-series data read from FAO lookup file.
    output_type: dtype
        Output data type, default `np.float32`.
    n_years: int
        Only fecth the latest N year of data, it will be restricted to any integer between 0 and 70.
    scaler: int
        Scaler for converting FAO units to Hestia units, defaults to `1`.
        Use `10` for converting from hg/ha to kg/ha, when reading FAO yield strings.
        This scaler will only be applied to the data array, not the year array.

    Returns
    -------
    np.array
        FAO Crop product term, e.g. 'Wheat'.
    """
    values = [r.split(":") for r in [r for r in fao_str.split(";")]]

    for val in values[::-1]:
        if '-' == val[1]:
            values.pop(values.index(val))

    n_years = min(max(0, n_years), 70)

    vals = np.array(values).transpose().astype(output_type)

    years_sorted = vals[0][np.argsort(vals[0])].astype(np.int32)
    vals_sorted = vals[1][np.argsort(vals[0])] / scaler

    gap = int(max(vals_sorted) - min(vals_sorted) + 1)
    return np.vstack([years_sorted[-min(n_years, gap):], vals_sorted[-min(n_years, gap):]])


def get_fao_yield(country_id: str, product_id: str, n_years: int = 10):
    """
    Look up the FAO yield per country per product from the glossary.

    Parameters
    ----------
    country_id: str
        Region `@id` from Hestia glossary, e.g. 'GADM-GBR', or 'region-south-america'.
    product_id: str
        Crop product term `@id` from Hestia glossary, e.g. 'wheatGrain'.
    n_years: int
        Only fecth the latest N year of data, it will be restricted to any integer between 0 and 70.

    Returns
    -------
    nunpy.array or None
        A 2-D array with years and yield values from FAO yield record, if successful.
    """
    lookup = download_lookup(LOOKUP_YIELD)
    product_name = get_FAO_crop_name(product_id)
    yield_str = get_table_value(lookup, 'termid', country_id, column_name(product_name))
    return fao_str_record_to_array(yield_str, n_years=n_years, scaler=10) if is_nonempty_str(yield_str) else None


def get_fao_fertuse(country_id: str, fert_id: str, n_years: int = 10):
    """
    Look up the FAO yield per country per product from the glossary.

    Parameters
    ----------
    country_id: str
        Region `@id` from Hestia glossary, e.g. 'GADM-GBR', or 'region-south-america'.
    fert_id: str
        Fertiliser term `@id` from Hestia glossary, restricted to the three options availible from FAO:
        'inorganicNitrogenFertiliserUnspecifiedKgN', 'inorganicPhosphorusFertiliserUnspecifiedKgP2O5',
        or 'inorganicPotassiumFertiliserUnspecifiedKgK2O'.
    n_years: int
        Only fecth the latest N year of data, it will be restricted to any integer between 0 and 70.

    Returns
    -------
    nunpy.array or None
        A 2-D array with years and yield values from FAO yield record, if successful.
    """
    lookup = download_lookup(LOOKUP_FERTUSE)
    yield_str = get_table_value(lookup, 'termid', country_id, column_name(fert_id))
    return fao_str_record_to_array(yield_str, np.single, n_years, 1) if is_nonempty_str(yield_str) else None


def get_mean_std_per_country_per_product(term_id: str, country_id: str, func1):
    """
    Get the means and standard deviations of FAO yield for a specific country/region for a specific product.

    Parameters
    ----------
    term_id: str
        Ferteliser term `@id` or crop product term `@id` from Hestia glossary, e.g. 'ammoniumNitrateKgN', 'wheatGrain'.
    country_id: str
        Region `@id` from Hestia glossary, e.g. 'GADM-GBR', or 'region-south-america'.
    func1: Function
        Function being used to get FAO time-series values.

    Returns
    -------
    list or None
        A list of [mu, sigma, n_years] values, if successful. Otherwise, return `None`.
    """
    yields10yr = func1(country_id, term_id, n_years=10)
    value = yields10yr[1] if (yields10yr is not None) and len(yields10yr) > 0 else None
    return (value.mean(), value.std(), len(value)) if value is not None else (None, None, None)
