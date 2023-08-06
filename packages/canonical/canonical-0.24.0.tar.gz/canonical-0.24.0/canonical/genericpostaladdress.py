# Copyright (C) 2022 Cochise Ruhulessin
#
# All rights reserved. No warranty, explicit or implicit, provided. In
# no event shall the author(s) be liable for any claim or damages.
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
import pydantic

from .iso3166 import ISO3166Alpha2


class GenericPostalAddress(pydantic.BaseModel):
    """A generic postal address. It is assumed that further validation
    is done upstream.
    """
    addressee: str = pydantic.Field(
        default=...,
        title='Address',
        description=(
            "The addressee line of the address. If the receiver is a person, "
            "this field contains its name. For organizations, the receiver may "
            "be further specified using the `contact_name` field."
        )
    )

    contact_name: str = pydantic.Field(
        default='',
        title='Contact name',
        alias='contactName',
        description=(
            "The name of the receiver. Use this field when sending, for example, "
            "to an organization with a specific person."
        )
    )

    address1: str = pydantic.Field(
        default=...,
        title='Address #1',
        description=(
            "First line of the address, usually the street/thoroughfare "
            "name. May also be a mailbox name/number."
        )
    )

    address2: str = pydantic.Field(
        default="",
        title='Address #2',
        description=(
            "Second line of the address."
        )
    )

    postal_code: str = pydantic.Field(
        default=...,
        alias='postalCode',
        title='Postal code'
    )

    city: str = pydantic.Field(
        default=...,
        title='City'
    )

    region: str = pydantic.Field(
        default='',
        title='Region',
        description=(
            "The first-order administrative division in which the address "
            "is located, such as a state in the United States."
        )
    )

    country: ISO3166Alpha2 = pydantic.Field(
        default=...,
        title='Country',
        description="The country represented as an ISO 3166 country code."
    )

    class Config:
        allow_population_by_field_name: bool = True