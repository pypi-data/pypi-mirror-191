import pytest

from pythonpoet import ImportBuilder


class TestImport:
    def test_import_deserialization(self):
        builder = (
            ImportBuilder().set_class_name("dataclass").set_module_name("dataclasses")
        )
        result = builder.build()
        assert result.to_string() == "from dataclasses import dataclass\n"

    def test_import_builder_build_exception(self):
        builder = ImportBuilder().set_class_name("dataclass")
        with pytest.raises(ValueError):
            builder.build()
