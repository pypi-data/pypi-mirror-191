from unittest.mock import patch
import os
import numpy as np
from tests.utils import fixtures_path
from hestia_earth.distribution.utils.priors import read_prior_stats

from hestia_earth.distribution.prior_fert import (
    generate_prior_fert_file, get_fao_fert, get_prior
)

fixtures_folder = os.path.join(fixtures_path, 'prior_fert')


def test_get_fao_fert():
    val1 = get_fao_fert('GADM-GBR', 'inorganicNitrogenFertiliserUnspecifiedKgN')
    val2 = get_fao_fert('GADM-GBR', 'manureDryKgN')
    assert (val1 == val2).all() == np.True_


@patch('hestia_earth.distribution.utils.priors.write_to_storage')
def test_generate_prior_fert_file(*args):
    result = generate_prior_fert_file(overwrite=True)
    expected = read_prior_stats(os.path.join(fixtures_folder, 'result.csv'))
    assert result.to_csv() == expected.to_csv()


def read_prior_file(*args):
    with open(os.path.join(fixtures_folder, 'result.csv'), 'rb') as f:
        return f.read()


@patch('hestia_earth.distribution.utils.priors.load_from_storage', side_effect=read_prior_file)
def test_get_prior(*args):
    mu, sd = get_prior('GADM-GBR', 'manureDryKgN')
    assert mu == 166.57699890136718
    assert sd == 14.47130123217229


@patch('hestia_earth.distribution.utils.priors.load_from_storage', side_effect=read_prior_file)
def test_get_prior_missing(*args):
    # data is not present
    mu, sd = get_prior('GADM-GBR', 'inorganicMagnesiumFertiliserUnspecifiedKgMg')
    assert mu is None
    assert sd is None
