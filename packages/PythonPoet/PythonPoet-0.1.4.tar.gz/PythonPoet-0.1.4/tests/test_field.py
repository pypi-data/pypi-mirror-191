from dataclasses import Field

import pytest

from pythonpoet import ClassFieldBuilder, ImportBuilder


class TestField:
    def test_field_deserialization(self):
        builder = ClassFieldBuilder().set_name("success").set_type(bool.__name__)
        result = builder.build()

        assert result.deserialize() == "\tsuccess: bool\n\n"
        assert len(result.get_imports()) == 0

    def test_field_deserialization_import(self):
        builder = (
            ClassFieldBuilder()
            .set_name("success")
            .set_type(
                Field.__name__,
                ImportBuilder().set_class_name("Field").set_module_name("dataclasses"),
            )
        )
        result = builder.build()

        assert result.deserialize() == "\tsuccess: Field\n\n"
        assert len(result.get_imports()) == 30

    def test_field_deserialization_value(self):
        builder = (
            ClassFieldBuilder()
            .set_name("success")
            .set_type(bool.__name__)
            .set_value(
                "field(default=True)",
                ImportBuilder().set_class_name("field").set_module_name("dataclasses"),
            )
        )
        result = builder.build()

        assert result.deserialize() == "\tsuccess: bool = field(default=True)\n\n"
        assert len(result.get_imports()) == 30

    def test_field_builder_build_exception(self):
        builder = ClassFieldBuilder().set_name("success")
        with pytest.raises(ValueError):
            builder.build()
