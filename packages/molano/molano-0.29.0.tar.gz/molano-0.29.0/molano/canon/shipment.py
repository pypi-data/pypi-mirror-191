# Copyright (C) 2022 Cochise Ruhulessin
#
# All rights reserved. No warranty, explicit or implicit, provided. In
# no event shall the author(s) be liable for any claim or damages.
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
import pydantic

from .shipmentitem import ShipmentItem


class Shipment(pydantic.BaseModel):
    carrier: str
    items: list[ShipmentItem]
    order_id: int
    picklist_id: int
    shipment_id: int
    trackingcode: str
    trackingurl: str | None = None