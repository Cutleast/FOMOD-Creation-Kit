"""
Copyright (c) Cutleast
"""

from __future__ import annotations

from typing import Optional

from lxml import etree
from pydantic_xml import BaseXmlModel


class FomodModel(BaseXmlModel):
    """
    Base class for models representing the XML files of a FOMOD installer.
    """

    @classmethod
    def get_schema_url(cls) -> Optional[str]:
        """
        Returns:
            Optional[str]: URL to the XSD schema file matching this model.
        """

    @classmethod
    def load[T: FomodModel](cls: type[T], xml_text: bytes) -> T:
        """
        Loads this model from the given XML text.

        Args:
            xml_text (bytes): XML text to load from.

        Returns:
            T: Deserialized model
        """

        return cls.from_xml(xml_text)

    def dump(self) -> bytes:
        """
        Dumps this model to an XML text.

        Returns:
            bytes: Serialized XML text
        """

        raw_xml: bytes = super().to_xml(  # type: ignore
            pretty_print=True, skip_empty=True
        )
        root = etree.fromstring(raw_xml)  # type: ignore

        schema_url: Optional[str] = self.get_schema_url()
        if schema_url is not None:
            xsi = "http://www.w3.org/2001/XMLSchema-instance"
            root.set("xsi", xsi)
            root.set("{%s}noNamespaceSchemaLocation" % xsi, schema_url)

        return etree.tostring(
            root,
            pretty_print=True,  # type: ignore
            encoding="UTF-8",  # type: ignore
            standalone=True,  # type: ignore
        )
