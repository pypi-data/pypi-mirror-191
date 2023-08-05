from unittest.mock import patch
import os
import json
import pandas as pd
from tests.utils import fixtures_path
from hestia_earth.distribution.utils.priors import read_prior_stats

from hestia_earth.distribution.utils.posterior import (
    INDEX_COLUMN, MULTI_INDEX_COLUMNS, update_all_post_data, get_post_data, get_post_ensemble_data, _post_filename
)


class_path = 'hestia_earth.distribution.utils.posterior'


def fake_generate_prior_file(folder: str):
    def run(*args):
        return read_prior_stats(os.path.join(fixtures_path, folder, 'prior.csv'))
    return run


def fake_generate_likl_file(folder: str):
    def run(country_id, product_id, *args):
        likl_file = os.path.join(fixtures_path, folder, 'likelihood', f"{'-'.join([country_id, product_id])}.csv")
        return pd.read_csv(likl_file) if os.path.exists(likl_file) else pd.DataFrame()
    return run


def read_posterior_file(folder: str):
    def run(*args):
        with open(os.path.join(fixtures_path, folder, 'result.csv'), 'rb') as f:
            return f.read()
    return run


@patch(f"{class_path}.load_from_storage", side_effect=read_posterior_file('posterior_yield'))
def test_get_post_yield(*args):
    mu, sd = get_post_data('GADM-COL', 'bananaFruit', '')
    assert mu == 2716
    assert sd == 486


@patch(f"{class_path}.load_from_storage", side_effect=read_posterior_file('posterior_yield'))
def test_get_post_yield_missing(*args):
    mu, sd = get_post_data('GADM-FRA', 'wheatGrain', '')
    assert mu is None
    assert sd is None


@patch(f"{class_path}.load_from_storage", side_effect=read_posterior_file('posterior_yield'))
def test_get_post_yield_empty(*args):
    mu, sd = get_post_data('GADM-COL', 'wheatGrain', '')
    assert mu is None
    assert sd is None


@patch(f"{class_path}.load_from_storage", side_effect=read_posterior_file('posterior_fert'))
def test_get_post_fert(*args):
    mu, sd = get_post_data('GADM-ALB', ('wheatGrain', 'inorganicPotassiumFertiliserUnspecifiedKgK2O'), '')
    assert mu == 2.6290606152464733
    assert sd == 5.785971787572081


@patch(f"{class_path}.load_from_storage", side_effect=read_posterior_file('posterior_fert'))
def test_get_post_fert_missing(*args):
    mu, sd = get_post_data('GADM-FRA', ('wheatGrain', 'inorganicPotassiumFertiliserUnspecifiedKgK2O'), '')
    assert mu is None
    assert sd is None


@patch(f"{class_path}.load_from_storage", side_effect=read_posterior_file('posterior_fert'))
def test_get_post_fert_empty(*args):
    mu, sd = get_post_data('GADM-AUT', ('wheatGrain', 'inorganicPotassiumFertiliserUnspecifiedKgK2O'), '')
    assert mu is None
    assert sd is None


def read_posterior_json(folder: str):
    def read_posterior(filename: str):
        file = filename.split('/')[1]
        with open(os.path.join(fixtures_path, folder, file), 'rb') as f:
            return f.read()
    return read_posterior


@patch(f"{class_path}.load_from_storage", side_effect=read_posterior_json('posterior_yield'))
@patch(f"{class_path}.file_exists", return_value=True)
def test_get_post_ensemble_data_yield(*args):
    mu_ensemble, sd_ensemble = get_post_ensemble_data('GADM-COL', 'bananaFruit')
    assert len(mu_ensemble) == 4
    assert len(sd_ensemble) == 4


@patch(f"{class_path}.generate_likl_file", side_effect=fake_generate_likl_file('posterior_yield'))
@patch(f"{class_path}.write_to_storage")
@patch(f"{class_path}.file_exists", return_value=False)
def test_get_post_ensemble_data_yield_missing(*args):
    mu_ensemble, sd_ensemble = get_post_ensemble_data('GADM-CHE', 'appleFruit',
                                                      generate_prior=fake_generate_prior_file('posterior_yield'))
    assert len(mu_ensemble) == 0
    assert len(sd_ensemble) == 0


@patch(f"{class_path}.load_from_storage", side_effect=read_posterior_json('posterior_yield'))
@patch(f"{class_path}.file_exists", return_value=True)
def test_get_post_ensemble_data_yield_empty(*args):
    mu_ensemble, sd_ensemble = get_post_ensemble_data('GADM-AFG', 'wheatGrain')
    assert len(mu_ensemble) == 0
    assert len(sd_ensemble) == 0


@patch(f"{class_path}.load_from_storage", side_effect=read_posterior_json('posterior_fert'))
@patch(f"{class_path}.file_exists", return_value=True)
def test_get_post_ensemble_data_fert(*args):
    mu_ensemble, sd_ensemble = get_post_ensemble_data('GADM-ALB', 'wheatGrain',
                                                      'inorganicPotassiumFertiliserUnspecifiedKgK2O',
                                                      generate_prior=fake_generate_prior_file('posterior_fert'))
    assert len(mu_ensemble) == 4
    assert len(sd_ensemble) == 4


@patch(f"{class_path}.generate_likl_file", side_effect=fake_generate_likl_file('posterior_fert'))
@patch(f"{class_path}.write_to_storage")
@patch(f"{class_path}.file_exists", return_value=False)
def test_get_post_ensemble_data_fert_missing(*args):
    mu_ensemble, sd_ensemble = get_post_ensemble_data('GADM-ALB', 'wheatGrain',
                                                      'inorganicPotassiumFertiliserUnspecifiedKgK2O',
                                                      generate_prior=fake_generate_prior_file('posterior_fert'))
    assert len(mu_ensemble) == 4
    assert len(sd_ensemble) == 4


@patch(f"{class_path}.load_from_storage", side_effect=read_posterior_json('posterior_fert'))
@patch(f"{class_path}.file_exists", return_value=True)
def test_get_post_ensemble_data_fert_empty(*args):
    mu_ensemble, sd_ensemble = get_post_ensemble_data('GADM-AUT', 'wheatGrain',
                                                      'inorganicPotassiumFertiliserUnspecifiedKgK2O',
                                                      generate_prior=fake_generate_prior_file('posterior_fert'))
    assert len(mu_ensemble) == 0
    assert len(sd_ensemble) == 0


def fake_get_post_ensemble(folder: str):
    def run(country_id, product_id, term_id='', **kwargs):
        filepath = os.path.join(fixtures_path, folder, _post_filename(country_id, product_id, term_id))
        data = {}
        if os.path.exists(filepath):
            with open(filepath, 'r') as f:
                data = json.load(f)
        return data.get('posterior', {}).get('mu', []), data.get('posterior', {}).get('sd', [])
    return run


@patch(f"{class_path}.get_post_ensemble_data", side_effect=fake_get_post_ensemble('posterior_yield'))
@patch(f"{class_path}.write_to_storage")
def test_update_all_post_data_yield(*args):
    df_prior = read_prior_stats(os.path.join(fixtures_path, 'posterior_yield', 'prior.csv'))
    result = update_all_post_data(df_prior, '')
    expected_file = os.path.join(fixtures_path, 'posterior_yield', 'result.csv')
    expected = pd.read_csv(expected_file, na_values='-', index_col=INDEX_COLUMN)
    assert (result.columns == expected.columns).all() and (result.index == expected.index).all()


@patch(f"{class_path}.get_post_ensemble_data", side_effect=fake_get_post_ensemble('posterior_fert'))
@patch(f"{class_path}.write_to_storage")
def test_update_all_post_data_fert(*args):
    df_prior = read_prior_stats(os.path.join(fixtures_path, 'posterior_fert', 'prior.csv'))
    result = update_all_post_data(df_prior, '', input_ids=['inorganicPotassiumFertiliserUnspecifiedKgK2O'])
    expected_file = os.path.join(fixtures_path, 'posterior_fert', 'result.csv')
    expected = pd.read_csv(expected_file, na_values='-', index_col=MULTI_INDEX_COLUMNS)
    assert (result.columns == expected.columns).all() and (result.index == expected.index).all()
