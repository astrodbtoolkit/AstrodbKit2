# Testing for utils

import pytest
import json
from datetime import datetime
from decimal import Decimal
from io import StringIO
from astropy.table import Table
from astrodbkit2.utils import json_serializer, get_simbad_names, _name_formatter
try:
    import mock
except ImportError:
    from unittest import mock


@pytest.mark.parametrize('test_input, expected', [
    ('TWA  27', 'TWA 27'),
    ('HIDDEN A', None),
    ('V* V4046 Sgr', 'V4046 Sgr'),
    ('** CVN   12A', 'CVN 12A')
])
def test_name_formatter(test_input, expected):
    assert _name_formatter(test_input) == expected


def test_json_serializer():
    data = {'date': datetime(2018, 12, 6, 12, 30, 0),
            'value': Decimal(2.3),
            'integer': 4}

    json_text = json.dumps(data, indent=4, default=json_serializer)
    with StringIO(json_text) as f:
        new_data = json.load(f)

    assert new_data['date'] == '2018-12-06T12:30:00'
    assert new_data['value'] == pytest.approx(2.3)
    assert new_data['integer'] == 4


@mock.patch('astrodbkit2.utils.Simbad.query_objectids')
def test_get_simbad_names(mock_simbad):
    mock_simbad.return_value = Table({'ID': ['name 1', 'name 2', 'V* name 3', 'HIDDEN name']})
    t = get_simbad_names('twa 27')
    assert len(t) == 3
    assert t[2] == 'name 3'
