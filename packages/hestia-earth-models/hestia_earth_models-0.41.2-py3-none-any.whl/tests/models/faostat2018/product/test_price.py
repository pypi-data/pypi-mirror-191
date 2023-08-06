import json
from unittest.mock import patch
from tests.utils import fixtures_path

from hestia_earth.models.faostat2018.product.price import MODEL, MODEL_KEY, run, _should_run

class_path = f"hestia_earth.models.{MODEL}.product.{MODEL_KEY}"
fixtures_folder = f"{fixtures_path}/{MODEL}/product/{MODEL_KEY}"

ANIMAL_PRODUCT = {
  "@id": "meatChickenLiveweight",
  "@type": "Term",
  "name": "Meat, chicken (liveweight)",
  "units": "kg liveweight",
  "defaultProperties": [
    {
      "term": {
        "@type": "Term",
        "termType": "property",
        "@id": "processingConversionLiveweightToColdCarcassWeight",
        "units": "%"
      },
      "value": 72.30401869158878,
      "sd": 1.8045100716897102,
      "@type": "Property"
    }
  ],
  "termType": "animalProduct"
}


def test_should_run():
    cycle = {'endDate': '2020-01'}
    should_run, *_ = _should_run(cycle)
    assert not should_run

    cycle['site'] = {'country': {'@id': 'GADM-GBR'}}
    should_run, *_ = _should_run(cycle)
    assert should_run is True


@patch(f"{class_path}.download_hestia", return_value={})
def test_run_crop(*args):
    with open(f"{fixtures_folder}/crop/cycle.jsonld", encoding='utf-8') as f:
        cycle = json.load(f)

    with open(f"{fixtures_folder}/crop/result.jsonld", encoding='utf-8') as f:
        expected = json.load(f)

    value = run(cycle)
    assert value == expected


@patch(f"{class_path}.download_hestia", return_value={})
def test_run_animalProduct(*args):
    with open(f"{fixtures_folder}/animalProduct/cycle.jsonld", encoding='utf-8') as f:
        cycle = json.load(f)

    with open(f"{fixtures_folder}/animalProduct/result.jsonld", encoding='utf-8') as f:
        expected = json.load(f)

    value = run(cycle)
    assert value == expected


@patch(f"{class_path}.download_hestia", return_value=ANIMAL_PRODUCT)
def test_run_liveAnimal(*args):
    with open(f"{fixtures_folder}/liveAnimal/cycle.jsonld", encoding='utf-8') as f:
        cycle = json.load(f)

    with open(f"{fixtures_folder}/liveAnimal/result.jsonld", encoding='utf-8') as f:
        expected = json.load(f)

    value = run(cycle)
    assert value == expected
