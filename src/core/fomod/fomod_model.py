"""
Copyright (c) Cutleast
"""

from __future__ import annotations

import logging
from typing import Optional

from lxml import etree
from pydantic_xml import BaseXmlModel

from core.utilities.cache import cache
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

    @classmethod
    @cache
    def __get_logger(cls) -> logging.Logger:
        return logging.getLogger(cls.__name__)

    def dump(self, validate: bool = True, encoding: str = "utf-8") -> bytes:
        """
        Dumps this model to an XML text.

        Args:
            validate (bool, optional):
                Whether to validate the XML text against the schema if one is available.
                Defaults to True.
            encoding (str, optional):
                The encoding to use for the XML text. Defaults to "utf-8".

        Raises:
            DocumentInvalid: when `validate` is True and the dumped xml is invalid

        Returns:
            bytes: Serialized XML text
        """

        log: logging.Logger = self.__get_logger()

        xml_text: bytes = super().to_xml(  # type: ignore
            pretty_print=True, skip_empty=True, exclude_unset=True
        )
        root = etree.fromstring(xml_text)

        schema_url: Optional[str] = self.get_schema_url()
        if schema_url is not None:
            xsi = "http://www.w3.org/2001/XMLSchema-instance"
            root.nsmap["xsi"] = xsi
            root.set("{%s}noNamespaceSchemaLocation" % xsi, schema_url)

        etree.indent(root, space="\t")
        xml_text = etree.tostring(
            root, pretty_print=True, encoding=encoding, standalone=True
        )

        if schema_url is not None and validate:
            try:
                validate_against_schema(schema_url, xml_text)
            except etree.DocumentInvalid as ex:
                log.debug("XML text:\n" + xml_text.decode(encoding))
                raise ex
            except Exception as ex:
                log.warning(
                    f"An error occured during XML validation: {ex}", exc_info=ex
                )

        return xml_text
