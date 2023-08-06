"""Declares :class:`YAMLRenderer`."""
import datetime
import enum
import typing
from typing import Any

import pydantic
import yaml
from yaml.dumper import SafeDumper
from yaml.representer import SafeRepresenter

from .json import JSONRenderer


class YAMLRenderer(JSONRenderer):
    """
    Renderer which serializes to YAML.
    """
    __module__: str = 'cbra.renderers'
    format: str = 'yaml'
    media_type: str = 'application/yaml'
    response_media_type: str = "application/yaml"
    #encoder_class = encoders.JSONEncoder

    @staticmethod
    def represent(
        dumper: SafeDumper,
        value: Any
    ) -> Any:
        if isinstance(value, datetime.datetime):
            value = dumper.represent_str(value.isoformat()) # type: ignore
        elif issubclass(type(value), str):
            if isinstance(value, enum.Enum):
                value = value.value
            value = dumper.represent_str(str(value)) # type: ignore
        else:
            raise NotImplementedError(type(value))
        return value

    @classmethod
    def openapi_example(cls, model: type[pydantic.BaseModel] | None) -> dict[str, Any]:
        schema: dict[str, Any] = {}
        if isinstance(model, pydantic.main.ModelMetaclass):
            if hasattr(model.Config, 'schema_extra')\
            and isinstance(model.Config.schema_extra, dict)\
            and isinstance(model.Config.schema_extra.get('example'), dict):
                assert hasattr(model.Config, 'schema_extra')
                example = model.Config.schema_extra['example'] # type: ignore
                schema['example'] = yaml.safe_dump(example) # type: ignore
        return schema

    def has_content(self) -> bool:
        return True

    def render(
        self,
        data: dict[str, typing.Any] | pydantic.BaseModel,
        renderer_context: dict[str, typing.Any] | None = None
    ) -> bytes:
        """Render `data` into YAML, returning a bytestring."""
        if data is None:
            return b''
        assert data is not None # nosec
        renderer_context = renderer_context or {}
        if isinstance(data, pydantic.BaseModel):
            data = data.dict(
                by_alias=bool(renderer_context.get('by_alias')),
            )
        serialized = yaml.safe_dump( # type: ignore
            data,
            indent=self.get_indent(self.accepted, renderer_context or {}),
            default_flow_style=False,
        )
        return '---\n' + serialized # type: ignore


SafeRepresenter.add_representer(None, YAMLRenderer.represent) # type: ignore