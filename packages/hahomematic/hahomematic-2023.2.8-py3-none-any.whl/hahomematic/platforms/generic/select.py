"""
Module for entities implemented using the select platform.

See https://www.home-assistant.io/integrations/select/.
"""
from __future__ import annotations

import logging

from hahomematic.const import HmPlatform
from hahomematic.platforms.entity import CallParameterCollector
from hahomematic.platforms.generic.entity import GenericEntity
from hahomematic.platforms.support import value_property

_LOGGER = logging.getLogger(__name__)


class HmSelect(GenericEntity[int | str]):
    """
    Implementation of a select entity.

    This is a default platform that gets automatically generated.
    """

    _attr_platform = HmPlatform.SELECT

    @value_property
    def value(self) -> str | None:  # type: ignore[override]
        """Get the value of the entity."""
        if self._attr_value is not None and self._attr_value_list is not None:
            return self._attr_value_list[int(self._attr_value)]
        return str(self._attr_default)

    async def send_value(
        self, value: int | str, collector: CallParameterCollector | None = None
    ) -> None:
        """Set the value of the entity."""
        # We allow setting the value via index as well, just in case.
        if isinstance(value, int) and self._attr_value_list:
            if 0 <= value < len(self._attr_value_list):
                await super().send_value(value=value, collector=collector)
        elif self._attr_value_list:
            if value in self._attr_value_list:
                await super().send_value(
                    value=self._attr_value_list.index(value), collector=collector
                )
        else:
            _LOGGER.warning(
                "Value not in value_list for %s/%s",
                self.name,
                self.unique_identifier,
            )
