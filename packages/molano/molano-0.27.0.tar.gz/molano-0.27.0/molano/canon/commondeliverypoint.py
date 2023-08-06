# Copyright (C) 2022 Cochise Ruhulessin
#
# All rights reserved. No warranty, explicit or implicit, provided. In
# no event shall the author(s) be liable for any claim or damages.
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
from typing import Literal

import pydantic


class DeliveryPoint(pydantic.BaseModel):
    """A physical location recognized by a postal operator at which the
    delivery of a postal item may occur.
    """
    kind: Literal['common'] = 'common'
    line1: str
    line2: str | None = None
    postal_code: str
    city: str
    country_code: str