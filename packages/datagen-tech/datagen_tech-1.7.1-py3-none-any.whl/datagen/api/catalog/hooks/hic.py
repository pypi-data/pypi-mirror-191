from typing import Dict, List

from datagen_protocol.schema import DataSequence
from pydantic.config import Extra
from pydantic.main import BaseModel

from datagen.api.assets import ExtrinsicParams
from datagen.api.catalog.impl import InitParametersHook


class HICPresetsHook(InitParametersHook[DataSequence]):
    def __init__(self, asset_id_to_asset_presets: dict):
        self._asset_id_to_asset_presets = asset_id_to_asset_presets

    def __call__(self, asset_id: str) -> dict:
        return dict(presets=self._asset_id_to_asset_presets[asset_id])

