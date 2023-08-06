# Copyright (C) 2022 Cochise Ruhulessin
#
# All rights reserved. No warranty, explicit or implicit, provided. In
# no event shall the author(s) be liable for any claim or damages.
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
from typing import Any
from typing import Literal

import pydantic

from .commondeliverypoint import DeliveryPoint


class BillingDetails(pydantic.BaseModel):
    version: Literal['v1'] = 'v1'
    organization_name: str | None = None
    contact_name: str | None = None
    address: DeliveryPoint

    @pydantic.root_validator
    def preprocess(
        cls,
        values: dict[str, Any]
    ) -> dict[str, Any]:
        if not values.get('organization_name')\
        and not values.get('contact_name'):
            raise ValueError(
                "At least one of `organization_name` or "
                "`contact_name` must be provided."
            )
        return values