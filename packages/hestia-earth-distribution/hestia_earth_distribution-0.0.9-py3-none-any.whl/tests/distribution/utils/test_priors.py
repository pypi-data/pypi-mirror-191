import os
from tests.utils import fixtures_path

from hestia_earth.distribution.utils.priors import get_prior_by_country_by_product


def test_get_prior_by_country_by_product_yield():
    country_id = 'GADM-CRI'
    product_id = 'abacaLeafStalk'
    prior_filename = os.path.join(fixtures_path, 'prior_yield', 'result.csv')
    vals = get_prior_by_country_by_product(prior_filename, country_id, product_id)
    assert [round(v) for v in vals] == [1157, 18, 10, 6]


def test_get_prior_by_country_by_product_fert():
    country_id = 'GADM-AFG'
    product_id = 'inorganicNitrogenFertiliserUnspecifiedKgN'
    prior_filename = os.path.join(fixtures_path, 'prior_fert', 'result.csv')
    vals = get_prior_by_country_by_product(prior_filename, country_id, product_id)
    assert [round(v) for v in vals] == [8, 14, 10, 5]
