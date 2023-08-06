# Copyright (C) 2022 Cochise Ruhulessin
#
# All rights reserved. No warranty, explicit or implicit, provided. In
# no event shall the author(s) be liable for any claim or damages.
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
import pytest

from canonical import ISO3166Alpha2


@pytest.mark.parametrize("value", [
    "NL",
    "BE",
    "DE"
])
def test_valid_codes(value: str):
    ISO3166Alpha2.validate(value)


@pytest.mark.parametrize("value", [
    "B1",
])
def test_invalid_codes(value: str):
    with pytest.raises(ValueError):
        ISO3166Alpha2.validate(value)