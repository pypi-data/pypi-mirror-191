from hestia_earth.utils.api import search, download_hestia
from hestia_earth.utils.tools import non_empty_list

from ..log import logger

_FERT_GROUPS = {
    'N': 'inorganicNitrogenFertiliserUnspecifiedKgN',
    'P2O5': 'inorganicPhosphorusFertiliserUnspecifiedKgP2O5',
    'K2O': 'inorganicPotassiumFertiliserUnspecifiedKgK2O'
}


def _get_fert_group_name(fert_id: str): return fert_id.split('Kg')[-1]


def get_fert_group_id(term_id: str):
    """
    Look up the fertiliser group (N, P2O5, K2O) of a Hestia fertliser term.

    Parameters
    ----------
    term_id: str
        Inorganic or organic fertiliser term `@id` from Hestia glossary, e.g. 'ammoniumNitrateKgN'.

    Returns
    -------
    str
        Fertiliser group '@id', e.g. 'inorganicNitrogenFertiliserUnspecifiedKgN'.
    """
    return _FERT_GROUPS.get(_get_fert_group_name(term_id))


def get_input_ids():
    """
    Get a list of '@id' of the Input that can be used to get data.
    """
    return list(_FERT_GROUPS.values())


def find_cycles(country_id: str, product_id: str, limit: int, recalculated: bool = False):
    country_name = download_hestia(country_id).get('name')
    product_name = download_hestia(product_id).get('name')

    cycles = search({
        'bool': {
            'must': [
                {
                    'match': {'@type': 'Cycle'}
                },
                {
                    'nested': {
                        'path': 'products',
                        'query': {
                            'bool': {
                                'must': [
                                    {'match': {'products.term.name.keyword': product_name}},
                                    {'match': {'products.primary': 'true'}}
                                ]
                            }
                        }
                    }
                },
                {
                    'match': {
                        'site.country.name.keyword': country_name
                    }
                }
            ],
            'must_not': [{'match': {'aggregated': True}}]
        }
    }, limit=limit)
    logger.info(f"Found {len(cycles)} non-aggregated cycles with product '{product_id}' in '{country_name}'.")
    cycles = [download_hestia(c['@id'], 'Cycle', 'recalculated' if recalculated else None) for c in cycles]
    return non_empty_list(cycles)
