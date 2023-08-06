# Copyright (C) 2022 Cochise Ruhulessin
#
# All rights reserved. No warranty, explicit or implicit, provided. In
# no event shall the author(s) be liable for any claim or damages.
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
import asyncio
import functools
import inspect
from typing import Any
from typing import Callable
from typing import TypeVar

from cbra.ext import ioc
from pydantic import BaseModel
from google.cloud.datastore import Client
from google.cloud.datastore import Entity
from google.cloud.datastore import Key
from google.cloud.datastore import Query


T = TypeVar("T")
M = TypeVar("M")


class GoogleDatastoreRepositoryMetaclass(type):

    def __new__(
        cls,
        name: str,
        bases: tuple[type, ...],
        namespace: dict[str, Any],
        **params: Any
    ):
        if not namespace.pop('__abstract__', False):
            Model: type[BaseModel] = params['model']
            namespace.update({
                'kind': getattr(Model.Config, 'kind', Model.__name__),
                'model': Model,
                'id_attr': getattr(Model.Config, 'id_attr', None)
            })
        return super().__new__(cls, name, bases, namespace, **params)


class GoogleDatastoreRepository(metaclass=GoogleDatastoreRepositoryMetaclass):
    __module__: str = 'login.infra.repo'
    __abstract__: bool = True
    client: Client
    exclude: set[str] = set()
    kind: str
    model: type[BaseModel]
    id_attr: str

    def __init_subclass__(
        cls,
        model: type[BaseModel]
    ):
        super().__init_subclass__()

    @staticmethod
    async def run_in_executor(
        func: Callable[..., Any],
        *args: Any,
        **kwargs: Any
    ) -> Any:
        loop = asyncio.get_running_loop()
        return await loop.run_in_executor(None, func, *args, **kwargs)

    def __init__(
        self,
        client: Client = ioc.inject('DatastoreClient')
    ):
        super().__init__()
        self.client = client

    async def allocate(self, base: Key | None = None, kind: str | None = None) -> int:
        if base is None:
            base = self.storage_key(kind=kind)
        key, *_ = await self.run_in_executor(
            functools.partial( # type: ignore
                self.client.allocate_ids, # type: ignore
                incomplete_key=base,
                num_ids=1
            )
        )
        return key.id

    async def delete_key(self, key: Key) -> None:
        await self.run_in_executor(self.client.delete, key) # type: ignore

    def entity_factory(
        self,
        id: int | str | None = None,
        key: Key | None = None,
        kind: str | None = None,
        parent: Key | None = None
    ) -> Entity:
        return Entity(key=key or self.storage_key(kind=kind, id=id, parent=parent))

    def restore(self, entity: Entity | None) -> Any:
        if entity is None:
            return None
        assert isinstance(self.id_attr, str) # nosec
        instance = self.model.parse_obj({
            **entity,
            self.id_attr: entity.key.id or entity.key.name # type: ignore
        })
        return instance

    def storage_key(
        self,
        id: int | str | None = None,
        kind: str | None = None,
        parent: Key | None = None
    ) -> Key:
        return (
            self.client.key(kind or self.kind, id, parent=parent) # type: ignore
            if id is not None
            else self.client.key(kind or self.kind, parent=parent) # type: ignore
        )

    async def delete(self, entity_id: int):
        assert entity_id is not None # nosec
        await self.run_in_executor(
            self.client.delete, # type: ignore
            self.storage_key(entity_id)
        )

    async def get_entity_by_id(
        self,
        entity_id: int | str,
        kind: str | None = None,
        parent: Key | None = None
    ) -> Entity | None:
        return await self.run_in_executor(
            functools.partial(
                self.client.get, # type: ignore
                key=self.client.key(kind or self.kind, entity_id, parent=parent) # type: ignore
            )
        )

    async def get_model(self, id: Any, kind: str | None = None) -> Any | None:
        entity = await self.get_entity_by_id(id, kind=kind)
        obj: Any | None = None
        if entity is not None:
            obj = self.restore(entity)
            if inspect.isawaitable(obj):
                obj = await obj
            setattr(obj, self.id_attr, entity.key.id or entity.key.name) # type: ignore
        return obj

    async def one(self, query: Query):
        """Run a query that is expected to yield exactly one result."""
        result = None
        for entity in await self.run_in_executor(query.fetch): # type: ignore
            if result is not None: # multiple objects returned
                raise Exception("Multiple entities returned")
            result = entity
        return result

    async def first(self, query: Query):
        """Run a query that is expected to yield at least one result."""
        result = None
        for entity in await self.run_in_executor(query.fetch): # type: ignore
            result = entity
            break
        return result

    async def persist_model(self, obj: T, kind: str | None = None) -> T:
        entity = self.entity_factory(id=getattr(obj, self.id_attr), kind=kind)
        entity.update(obj.dict(exclude=self.exclude | {self.id_attr})) # type: ignore
        await self.put(entity)
        return self.model.parse_obj({ # type: ignore
            **entity,
            self.id_attr: entity.key.id or entity.key.name # type: ignore
        })

    async def put(self, entity: Entity) -> Entity:
        await self.run_in_executor(self.client.put, entity) # type: ignore
        assert (entity.key.id or entity.key.name) is not None # type: ignore # nosec
        return entity

    def query(self, kind: str | None = None, ancestor: Key | None = None) -> Query:
        return self.client.query(kind=kind or self.kind, ancestor=ancestor) # type: ignore