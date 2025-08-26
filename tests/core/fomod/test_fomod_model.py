"""
Copyright (c) Cutleast
"""

from typing import Optional

import pytest

from core.fomod.fomod_model import FomodModel
from tests.base_test import BaseTest


class TestFomodModel(BaseTest):
    """
    Tests `core.fomod.fomod_model.FomodModel`.
    """

    TEST_LOAD_DATA: list[tuple[bytes, Optional[str]]] = [
        (
            """<?xml version="1.0" encoding="UTF-8"?><FomodModel />""".encode(),
            "utf-8",
        ),
        (
            """<?xml version="1.0" encoding="UTF-8"?><FomodModel />""".encode(),
            None,
        ),
        (
            """<?xml version="1.0" encoding="UTF-16LE"?><FomodModel />""".encode(
                "utf-16le"
            ),
            "utf-16le",
        ),
        (
            """<?xml version="1.0" encoding="UTF-16LE"?><FomodModel />""".encode(
                "utf-16le"
            ),
            None,
        ),
    ]

    @pytest.mark.parametrize("xml_data, used_encoding", TEST_LOAD_DATA)
    def test_load(self, xml_data: bytes, used_encoding: Optional[str]) -> None:
        """
        Tests the `core.fomod.fomod_model.FomodModel.load` method with different
        encodings.
        """

        FomodModel.load(xml_data, used_encoding)
