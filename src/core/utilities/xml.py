"""
Copyright (c) Cutleast
"""

import logging
import re
from typing import Optional

from lxml import etree

from .web_utils import get_raw_web_content

log: logging.Logger = logging.getLogger("Utilities.XML")


XML_DECLARATION_PATTERN: re.Pattern[bytes] = re.compile(rb"^<\?xml.*\?>")


def validate_against_schema(schema_url: str, xml_text: bytes | str) -> None:
    """
    Validates the given XML text against the schema at the specified URL.

    Raises:
        DocumentInvalid: When the XML text is not valid against the schema.
        ValueError: When the schema could not be fetched.

    Args:
        schema_url (str): URL to the XSD schema file.
        xml_text (bytes | str): XML text to validate.
    """

    log.info(f"Fetching schema from '{schema_url}'...")
    schema_xml: Optional[bytes] = get_raw_web_content(schema_url)

    if schema_xml is None:
        raise ValueError(f"Failed to fetch schema from '{schema_url}'!")

    log.info("Validating XML against schema...")
    schema = etree.XMLSchema(etree.fromstring(schema_xml))
    schema.assertValid(etree.fromstring(xml_text))

    log.info("XML is valid against schema.")


if __name__ == "__main__":
    import sys
    from pathlib import Path

    validate_against_schema(sys.argv[1], Path(sys.argv[2]).read_bytes())
