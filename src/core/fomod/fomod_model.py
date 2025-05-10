"""
Copyright (c) Cutleast
"""

from __future__ import annotations

from typing import Optional

from lxml import etree
from pydantic_xml import BaseXmlModel

from core.utilities.xml import validate_against_schema


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

    def dump(self, validate: bool = True) -> bytes:
        """
        Dumps this model to an XML text.

        Args:
            validate (bool, optional):
                Whether to validate the XML text against the schema if one is available.
                Defaults to True.

        Returns:
            bytes: Serialized XML text
        """

        xml_text: bytes = super().to_xml(  # type: ignore
            pretty_print=True, skip_empty=True
        )
        root = etree.fromstring(xml_text)

        schema_url: Optional[str] = self.get_schema_url()
        if schema_url is not None:
            xsi = "http://www.w3.org/2001/XMLSchema-instance"
            root.nsmap["xsi"] = xsi
            root.set("{%s}noNamespaceSchemaLocation" % xsi, schema_url)

        xml_text = etree.tostring(
            root, pretty_print=True, encoding="UTF-8", standalone=True
        )

        if schema_url is not None and validate:
            validate_against_schema(schema_url, xml_text)

        return xml_text
